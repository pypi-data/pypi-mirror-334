import base64
import logging
import os
import re
import time
import uuid
from time import sleep
from typing import Dict, Any, List
import hashlib

import requests
from requests.exceptions import RequestException, Timeout

from testbeds.schema import (
    EvaluationResult,
    CommandExecutionResponse,
    TestRunResponse,
    SWEbenchInstance,
    TestStatus,
)
from testbeds.swebench.constants import ResolvedStatus, APPLY_PATCH_FAIL, RUN_TESTS
from testbeds.swebench.log_parsers import parse_log
from testbeds.swebench.test_spec import TestSpec
from testbeds.swebench.utils import load_swebench_instance
from testbeds.sdk.exceptions import (
    TestbedAuthenticationError,
    TestbedError,
    TestbedConnectionError,
    TestbedTimeoutError,
)
from testbeds.sdk.base_client import BaseTestbedClient

logger = logging.getLogger(__name__)


class TestbedClient(BaseTestbedClient):
    def __enter__(self):
        self.wait_until_ready()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    def check_health(self, timeout: int = 30):
        """Check testbed health status."""
        try:
            response = self._request("GET", "health", operation_timeout=timeout)
            return response.get("status") == "OK"
        except TestbedError as e:
            if hasattr(e, "response") and e.response.status_code in [503, 504]:
                return False
            raise

    def _generate_traceparent(self):
        return f"00-{self.trace_id}-{self.current_span_id or uuid.uuid4().hex[:16]}-01"

    def _generate_headers(self):
        return {
            "X-API-Key": self.api_key,
            "traceparent": self._generate_traceparent(),
        }

    def _request(
        self,
        method: str,
        endpoint: str | None = None,
        max_retries: int = 3,
        initial_retry_delay: int = 1,
        max_retry_delay: int = 60,
        operation_timeout: int = 300,
        **kwargs,
    ) -> Dict[str, Any]:
        url = self._get_url(endpoint)
        headers = self._generate_headers()

        retries = 0
        retry_delay = initial_retry_delay
        start_time = time.time()

        while retries < max_retries:
            if time.time() - start_time > operation_timeout:
                raise TestbedTimeoutError(
                    f"Operation timed out after {operation_timeout} seconds"
                )

            try:
                logger.debug(
                    f"Attempting request to {url} (Attempt {retries + 1}/{max_retries})"
                )
                response = requests.request(
                    method, url, headers=headers, timeout=30, **kwargs
                )

                response.raise_for_status()
                logger.debug(f"Request to {url} successful")
                return response.json()
            except requests.exceptions.Timeout:
                retries += 1
                if retries == max_retries:
                    raise TestbedTimeoutError(
                        f"Request to {url} timed out after {max_retries} retries"
                    )
            except requests.exceptions.ConnectionError as e:
                retries += 1
                if retries == max_retries:
                    raise TestbedConnectionError(
                        f"Failed to connect to testbed after {max_retries} retries"
                    ) from e
            except requests.exceptions.HTTPError as e:
                error_message = str(e)
                error_code = None
                details = {}

                try:
                    error_data = e.response.json()
                    error_message = error_data.get("message")
                    error_code = error_data.get("error")
                    details = error_data
                except (ValueError, AttributeError):
                    error_message = e.response.text or str(e)

                if 400 <= e.response.status_code < 500:
                    if e.response.status_code == 401:
                        raise TestbedAuthenticationError(
                            error_message, error_code, details
                        ) from e
                    raise TestbedError(error_message, error_code, details) from e

                # Only retry on server errors (500+)
                retries += 1
                if retries == max_retries:
                    raise TestbedError(
                        f"Server error after {max_retries} retries: {error_message}",
                        error_code,
                        details,
                    ) from e

            logger.warning(
                f"Request failed, retrying in {retry_delay} seconds... ({retries}/{max_retries})"
            )
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)

        raise TestbedError(f"Max retries reached for {url}")

    def wait_until_ready(self, timeout: float = 600):
        """Wait until testbed is healthy and ready."""
        start_time = time.time()
        wait_time = 0
        while wait_time < timeout:
            wait_time = time.time() - start_time
            try:
                if self.check_health():
                    logger.debug(f"Testbed {self.testbed_id} is healthy and ready")
                    return True

                logger.debug(f"Testbed {self.testbed_id} not ready yet, waiting...")
                time.sleep(1)
            except Timeout as e:
                logger.warning(
                    f"Testbed {self.testbed_id} not ready yet, will retry (Tried for {wait_time} seconds)"
                )
                time.sleep(1)
            except RequestException as e:
                if isinstance(e, requests.exceptions.ConnectionError):
                    logger.warning(
                        f"Failed to connect to testbed {self.testbed_id}, will retry... (Tried for {wait_time} seconds)"
                    )
                    time.sleep(1)
                elif e.response and e.response.status_code in [503, 504]:
                    logger.warning(
                        f"Got response {e.response.status_code} indicating that the testbed {self.testbed_id} might not be ready yet, will retry...  (Tried for {wait_time} seconds)"
                    )
                    time.sleep(1)
                else:
                    logger.error(f"Health check failed. {str(e)} {e.response.text}")
                    raise e
            except Exception as e:
                logger.warning(
                    f"Health check failed: {str(e)}, retrying... (Tried for {wait_time} seconds)"
                )
                time.sleep(1)

        raise TimeoutError(
            f"Testbed {self.testbed_id} not ready within {wait_time} seconds"
        )

    def status(self):
        return self._request("GET", "status")

    def get_execution_status(self) -> CommandExecutionResponse:
        try:
            response = self._request("GET", "exec")
            return CommandExecutionResponse.model_validate(response)
        except requests.RequestException as e:
            logger.error(f"Error during get_execution_status: {str(e)}")
            raise e

    def get_diff(self) -> str:
        """Get the current git diff output."""
        try:
            response = self._request("GET", "diff")
            return response.get("diff", "")
        except requests.RequestException as e:
            logger.error(f"Error getting git diff: {str(e)}")
            raise e

    def apply_patch(self, patch: str) -> str:
        if not patch.endswith("\n"):
            patch += "\n"

        response = self._request("POST", "apply-patch", json={"patch": patch})

        if APPLY_PATCH_FAIL in response.get("output", ""):
            logger.error(
                f"Failed to apply patch: {patch}.\n\nOutput\n:{response.get('output', '')}"
            )
            raise RuntimeError(
                f"Failed to apply patch: {patch}.\n\nOutput\n:{response.get('output', '')}"
            )

        diff = self.get_diff()
        logger.debug(f"Diff after patch: \n{diff}")
        return diff

    def _generate_cache_key(
        self, test_files: list[str] | None, patch: str | None
    ) -> str:
        """Generate a unique cache key based on test files and patch content"""
        key_parts = []
        if test_files:
            key_parts.extend(sorted(test_files))
        if patch:
            key_parts.append(patch)
        if not key_parts:
            key_parts.append("all_tests_no_patch")

        combined = "|".join(key_parts)
        return hashlib.sha256(combined.encode()).hexdigest()

    def run_tests(
        self,
        test_files: list[str] | None = None,
        patch: str | None = None,
        timeout: int = 1200,
    ) -> TestRunResponse:
        logger.debug(
            f"Executing run_tests with test_files={test_files} and patch={patch}"
        )

        if self.test_cache is not None:
            cache_key = self._generate_cache_key(test_files, patch)
            cached_result = self.test_cache.get(cache_key)
            if cached_result:
                logger.info("Returning cached test results")
                return cached_result

        if patch:
            self.apply_patch(patch)

        test_results = []
        for test_file in test_files:
            data = {"test_files": [test_file]}
            self._request("POST", "run-tests", json=data)
            response = self.get_execution_status()

            start_time = time.time()
            while response.status == "running":
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"Execution timed out after {timeout} seconds")
                sleep(1.0)
                response = self.get_execution_status()

            if self.log_dir:
                datetime_str = time.strftime("%Y%m%d-%H%M%S")
                with open(f"{self.log_dir}/{datetime_str}_run_tests.log", "a") as f:
                    f.write(f"Response:\n{response.output}\n")

            log = response.output.split(f"{RUN_TESTS}\n")[-1]
            test_result = parse_log(log, self.test_spec.repo)

            if len(test_result) == 1 and test_result[0].status == TestStatus.ERROR:
                test_result[0].file_path = test_file

            filtered_test_result = []
            for test in test_result:
                if test.file_path != test_file:
                    logger.info(
                        f"Skipping test {test.method} in {test.file_path}. Expected {test_file}"
                    )
                else:
                    filtered_test_result.append(test)

            test_results.extend(filtered_test_result)
            logger.info(
                f"Finished running {test_file} tests. Got {len(filtered_test_result)} test results."
            )

        filtered_test_result = []

        statuses = {}
        tests_by_file = {}

        ignored_tests = 0
        for test in test_results:
            if test.method in self.ignored_tests.get(test.file_path, []):
                ignored_tests += 1
                continue

            filtered_test_result.append(test)

            # Track tests by file
            if test.file_path not in tests_by_file:
                tests_by_file[test.file_path] = {"count": 0, "statuses": {}}

            tests_by_file[test.file_path]["count"] += 1
            if test.status not in tests_by_file[test.file_path]["statuses"]:
                tests_by_file[test.file_path]["statuses"][test.status] = 0
            tests_by_file[test.file_path]["statuses"][test.status] += 1

        summary = [
            f"{file_path}: {stats['count']} tests. {stats['statuses']}"
            for file_path, stats in tests_by_file.items()
        ]
        logger.info(f"Test summary by file: {' | '.join(summary)}")

        result = TestRunResponse(test_results=filtered_test_result)

        if self.test_cache is not None:
            cache_key = self._generate_cache_key(test_files, patch)
            self.test_cache[cache_key] = result

        return result

    def run_evaluation(
        self, run_id: str | None = None, patch: str | None = None
    ) -> EvaluationResult:
        self.current_span_id = uuid.uuid4().hex[:16]
        if not self.instance:
            raise ValueError("SWE-bench instance not set")

        try:
            if not patch:
                logger.info(
                    f"Running evaluation for instance {self.instance.instance_id} with gold prediction"
                )
                patch = self.instance.patch
            else:
                logger.info(
                    f"Running evaluation for instance {self.instance.instance_id} with patch"
                )

            self.wait_until_ready()
            self.reset_testbed()

            self.apply_patch(patch)

            try:
                git_diff_output_before = self.get_diff().strip()
            except Exception as e:
                logger.warning(
                    f"Failed to get git diff before running eval script: {e}"
                )
                git_diff_output_before = None

            self._request("POST", "run-evaluation")

            response = self.get_execution_status()
            while response.status == "running":
                response = self.get_execution_status()
                sleep(1)

            if self.log_dir:
                datetime_str = time.strftime("%Y%m%d-%H%M%S")
                with open(f"{self.log_dir}/{datetime_str}_run_tests.log", "a") as f:
                    f.write(f"Response:\n{response.output}\n")

            if "APPLY_PATCH_FAIL" in response.output:
                logger.error("Failed to apply patch")
                return EvaluationResult(
                    status="error",
                    output=response.get("output", ""),
                )

            try:
                git_diff_output_after = self.get_diff().strip()

                if (
                    git_diff_output_before
                    and git_diff_output_after != git_diff_output_before
                ):
                    logger.info(f"Git diff changed after running eval script")
            except Exception as e:
                logger.warning(f"Failed to get git diff after running eval script: {e}")

            test_status = self.test_spec.get_pred_report(response.output)
            return EvaluationResult(
                run_id=run_id,
                resolved=test_status.status == ResolvedStatus.FULL,
                patch_applied=True,
                instance_id=self.instance.instance_id,
                output=response.output,
                tests_status=test_status,
            )
        finally:
            self.current_span_id = None

    def reset_testbed(self):
        try:
            response = self._request(
                "POST",
                "reset",
                json={"instance_id": self.instance.instance_id, "run_id": self.run_id},
            )
            logger.info(f"Reset testbed {self.testbed_id}: {response}")
            return response
        except requests.RequestException as e:
            logger.error(f"Error during reset: {str(e)}")
            raise e

    def execute(self, commands: List[str] | str):
        if isinstance(commands, str):
            commands = [commands]

        try:
            response = self._request("POST", "exec", json={"commands": commands})
            return CommandExecutionResponse.model_validate(response)
        except requests.RequestException as e:
            logger.error(f"Error during execute: {str(e)}")
            raise e

    def destroy(self):
        self._request("DELETE")

    def _load_instance(self, instance_id: str) -> SWEbenchInstance:
        """Load a SWEbench instance from the API."""
        try:
            url = f"{self.base_url}/instances/{instance_id}"
            response = requests.get(url, headers=self._generate_headers())
            response.raise_for_status()
            return SWEbenchInstance.model_validate(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to load instance {instance_id} from API: {e}")
            raise TestbedError(f"Failed to load instance {instance_id}") from e
