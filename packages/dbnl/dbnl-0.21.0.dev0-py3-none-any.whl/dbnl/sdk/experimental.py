from __future__ import annotations

import time
from copy import deepcopy
from typing import Any, Literal, Optional, TypedDict

from typing_extensions import NotRequired

import dbnl.api
from dbnl.errors import DBNLDuplicateError, DBNLError, DBNLInputValidationError, DBNLResourceNotFoundError

from .core import handle_api_validation_error, validate_login
from .models import (
    AssertionDict,
    Project,
    Run,
    TestGenerationSession,
    TestRecalibrationSession,
    TestSession,
    TestSpecDict,
)


@validate_login
def get_tests(*, test_session_id: str) -> list[dict[str, Any]]:
    """
    Get all Tests for a Test Session

    :param test_session_id: Test Session ID
    :type test_session_id: str

    :return: List of tests
    :rtype: List[Dict[Any, Any]]

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    """
    all_tests: list[dict[Any, Any]] = []
    tests = dbnl.api.get_tests(test_session_id=test_session_id)
    all_tests += tests["data"]
    total_count = tests["total_count"]

    while len(all_tests) < total_count:
        cur_offset = len(all_tests)
        tests = dbnl.api.get_tests(test_session_id=test_session_id, offset=cur_offset)
        all_tests += tests["data"]

    return all_tests


@validate_login
def get_test_sessions(*, project: Project) -> list[TestSession]:
    """
    Get all Test Sessions for a Project

    :param project: Project from which to retrieve Test Sessions
    :type project: Project

    :return: List of test sessions
    :rtype: list[TestSession]

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    """
    all_test_sessions: list[dict[Any, Any]] = []
    test_sessions = dbnl.api.get_test_sessions(project_id=project.id)
    all_test_sessions += test_sessions["data"]
    total_count = test_sessions["total_count"]

    while len(all_test_sessions) < total_count:
        cur_offset = len(all_test_sessions)
        test_sessions = dbnl.api.get_test_sessions(project_id=project.id, offset=cur_offset)
        all_test_sessions += test_sessions["data"]

    return [TestSession.from_dict(ts) for ts in all_test_sessions]


@validate_login
def create_test_generation_session(
    *,
    run: Run,
    columns: Optional[list[str | dict[Literal["name"], str]]] = None,
) -> TestGenerationSession:
    """
    Create a Test Generation Session by redefining the expected output for tests in a Test Generation Session

    :param run: Run to generate tests from
    :type run: Run
    :param columns: List of columns in the Run to generate tests for. If None, all columns in the Run will be used, defaults to None. If a list of strings, each string is a column name. If a list of dictionaries, each dictionary must have a 'name' key, and the value is the column name.
    :type columns: Optional[List[Dict[Literal["name"], str]]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    :raises DBNLInputValidationError: arguments do not conform to expected format.

    :return: Test Generation Session
    :rtype: TestGenerationSession
    """
    _columns: Optional[list[dict[str, Any]]]
    if columns:
        if not all(isinstance(c, (dict, str)) for c in columns):
            raise DBNLInputValidationError("`columns` must be a list of strings or dictionaries with a 'name' key")
        if all(isinstance(c, str) for c in columns):
            _columns = [{"name": c} for c in columns]
        else:
            _columns = columns  # type: ignore
    else:
        _columns = None
    test_generation_session = dbnl.api.post_test_generation_session(
        project_id=run.project_id,
        run_id=run.id,
        columns=_columns,
    )
    return TestGenerationSession.from_dict(test_generation_session)


@validate_login
def wait_for_test_generation_session(
    *,
    test_generation_session: TestGenerationSession,
    timeout_s: int = 180,
) -> TestGenerationSession:
    """
    Wait for a Test Generation Session to finish. Polls every 3 seconds until it is completed.

    :param test_generation_session: TestGenerationSession to wait for
    :type test_generation_session: TestGenerationSession
    :param timeout_s: Total wait time (in seconds) for Test Generation Session to complete, defaults to 180
    :type timeout_s: int, optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    :raises DBNLError: Test Generation Session did not complete after waiting for the `timeout_s` seconds

    :return: completed TestGenerationSession
    :rtype: TestGenerationSession
    """
    FINISHED_STATUSES = {"COMPLETED", "FAILED"}
    start = time.time()
    while test_generation_session.status not in FINISHED_STATUSES and (time.time() - start) < timeout_s:
        test_generation_session = TestGenerationSession.from_dict(
            dbnl.api.get_test_generation_session(test_generation_session_id=test_generation_session.id)
        )
        time.sleep(3)

    if test_generation_session.status not in FINISHED_STATUSES:
        raise DBNLError(
            f"Test Generation Session {test_generation_session} did not complete after waiting {timeout_s} seconds"
        )

    return test_generation_session


def create_test_recalibration_session(
    *,
    test_session: TestSession,
    feedback: str,
    test_ids: Optional[list[str]] = None,
) -> TestRecalibrationSession:
    """
    Create a Test Recalibration Session by redefining the expected output for tests in a Test Session

    :param test_session: Test Session to recalibrate
    :type test_session: TestSession
    :param feedback: Feedback for the recalibration. Can be 'PASS' or 'FAIL'
    :type feedback: str
    :param test_ids: List of test IDs to recalibrate, defaults to None. If None, all tests in the Test Session will be recalibrated.
    :type test_ids: Optional[List[str]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    :raises DBNLInputValidationError: arguments do not conform to expected format.

    :return: Test Recalibration Session
    :rtype: TestRecalibrationSession
    """
    if feedback not in {"PASS", "FAIL"}:
        raise DBNLInputValidationError("`feedback` must be 'PASS' or 'FAIL'")
    test_recalibration_session = dbnl.api.post_test_recalibration_session(
        project_id=test_session.project_id,
        test_session_id=test_session.id,
        feedback=feedback,
        test_ids=test_ids,
    )
    return TestRecalibrationSession.from_dict(test_recalibration_session)


@validate_login
def wait_for_test_recalibration_session(
    *,
    test_recalibration_session: TestRecalibrationSession,
    timeout_s: int = 180,
) -> TestRecalibrationSession:
    """
    Wait for a Test Recalibration Session to finish. Polls every 3 seconds until it is completed.

    :param test_recalibration_session: TestRecalibrationSession to wait for
    :type test_recalibration_session: TestRecalibrationSession
    :param timeout_s: Total wait time (in seconds) for Test Recalibration Session to complete, defaults to 180.0
    :type timeout_s: int, optional

    :return: completed TestRecalibrationSession
    :rtype: TestRecalibrationSession

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    :raises DBNLError: Test Recalibration Session did not complete after waiting for the `timeout_s` seconds
    """
    FINISHED_STATUSES = {"COMPLETED", "FAILED"}
    start = time.time()
    while test_recalibration_session.status not in FINISHED_STATUSES and (time.time() - start) < timeout_s:
        test_recalibration_session = TestRecalibrationSession.from_dict(
            dbnl.api.get_test_recalibration_session(test_recalibration_session_id=test_recalibration_session.id)
        )
        time.sleep(3)

    if test_recalibration_session.status not in FINISHED_STATUSES:
        raise DBNLError(
            f"Test Recalibration Session {test_recalibration_session} did not complete after waiting {timeout_s} seconds"
        )

    return test_recalibration_session


@validate_login
def wait_for_test_session(
    *,
    test_session: TestSession,
    timeout_s: int = 180,
) -> TestSession:
    """
    Wait for a Test Session to finish. Polls every 3 seconds until it is completed.

    :param test_session: TestSession to wait for
    :type test_session: TestSession
    :param timeout_s: Total wait time (in seconds) for Test Session to complete, defaults to 180.0
    :type timeout_s: int, optional

    :return: completed TestSession
    :rtype: TestSession

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    :raises DBNLError: Test Session did not complete after waiting for the `timeout_s` seconds
    """
    start = time.time()
    while test_session.status not in ["PASSED", "FAILED"] and (time.time() - start) < timeout_s:
        test_session = TestSession.from_dict(dbnl.api.get_test_session(test_session_id=test_session.id))
        time.sleep(3)

    if test_session.status not in ["PASSED", "FAILED"]:
        raise DBNLError(f"Test Session {test_session} did not complete after waiting {timeout_s} seconds")

    return test_session


@validate_login
def create_test(*, test_spec_dict: TestSpecDict) -> dict[str, Any]:
    """
    Create a new Test Spec in DBNL

    :param test_spec_dict: Dictionary containing the Test Spec schema
    :type test_spec_dict: TestSpecDict

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    :raises DBNLAPIValidationError: Test Spec does not conform to expected format.
    :raises DBNLDuplicateError: Test Spec with the same name already exists in the Project.
    """
    with handle_api_validation_error():
        try:
            test_spec = dbnl.api.post_test_specs(test_spec_dict=dict(test_spec_dict))
        except DBNLDuplicateError:
            raise DBNLDuplicateError(
                f"Test with the name {test_spec_dict['name']} already exists in Project {test_spec_dict['project_id']}"
            )

    return test_spec


class IncompleteTestSpecDict(TypedDict, total=False):
    project_id: NotRequired[str]
    name: str
    statistic_name: str
    statistic_params: dict[str, float | int | str]
    statistic_inputs: list[dict[str, Any]]
    assertion: AssertionDict
    description: NotRequired[str]
    tag_names: NotRequired[list[str]]
    tag_ids: NotRequired[list[str]]


def prepare_incomplete_test_spec_payload(
    *,
    test_spec_dict: IncompleteTestSpecDict,
    project_id: Optional[str] = None,
) -> TestSpecDict:
    """
    Prepare the test spec payload for the API. Add `project_id` if it is not present. Replace `tag_names` with `tag_ids`.

    :param test_spec_dict: Dictionary containing the test spec schema
    :type test_spec_dict: Dict[str, Any]
    :param project_id: Project ID, defaults to None. If `project_id` does not exist in `test_spec_dict`, it is required as an argument.
    :type project_id: Optional[str], optional

    :return: Dictionary containing the test spec payload
    :rtype: Dict[str, Any]

    :raises DBNLInputValidationError: Input does not conform to expected format
    """
    test_spec_dict = deepcopy(test_spec_dict)
    if "project_id" not in test_spec_dict:
        if project_id is None:
            raise DBNLInputValidationError("`project_id` is required in `test_spec_dict` or as an argument")
        test_spec_dict["project_id"] = project_id

    if "tag_ids" not in test_spec_dict and "tag_names" in test_spec_dict:
        tag_ids = []
        for tag_name in test_spec_dict["tag_names"]:
            tag = get_or_create_tag(project_id=test_spec_dict["project_id"], name=tag_name)
            tag_ids.append(tag["id"])
        test_spec_dict["tag_ids"] = tag_ids
        test_spec_dict.pop("tag_names")

    complete_test_spec = TestSpecDict(
        project_id=test_spec_dict["project_id"],
        name=test_spec_dict["name"],
        statistic_name=test_spec_dict["statistic_name"],
        statistic_params=test_spec_dict["statistic_params"],
        statistic_inputs=test_spec_dict["statistic_inputs"],
        assertion=test_spec_dict["assertion"],
    )
    if "description" in test_spec_dict:
        complete_test_spec["description"] = test_spec_dict["description"]
    if "tag_ids" in test_spec_dict:
        complete_test_spec["tag_ids"] = test_spec_dict["tag_ids"]
    return complete_test_spec


@validate_login
def get_or_create_tag(
    *,
    project_id: str,
    name: str,
    description: Optional[str] = None,
) -> dict[str, Any]:
    """
    Get or create a Test Tag in DBNL

    :param project_id: Project ID
    :type project_id: str
    :param name: Tag Name
    :type name: str
    :param description: Tag Description, defaults to None
    :type description: Optional[str], optional

    :return: Dictionary containing the tag
    :rtype: Dict[str, Any]

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in.
    """
    try:
        tag_dict = dbnl.api.api_stubs.get_tag_by_name(project_id=project_id, name=name)
    except DBNLResourceNotFoundError:
        tag_dict = dbnl.api.api_stubs.post_tags(project_id=project_id, name=name, description=description)
    return tag_dict
