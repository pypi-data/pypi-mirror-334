from __future__ import annotations

import json
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from functools import wraps
from http import HTTPStatus
from io import BytesIO
from typing import Any, Callable, Optional, TypeVar, Union

import pandas as pd
from typing_extensions import ParamSpec

import dbnl.api
from dbnl.config import CONFIG
from dbnl.errors import (
    DBNLAPIError,
    DBNLAPIValidationError,
    DBNLConflictingProjectError,
    DBNLDuplicateError,
    DBNLInputValidationError,
    DBNLNotLoggedInError,
    DBNLProjectNotFoundError,
    DBNLResourceNotFoundError,
    DBNLRunConfigNotFoundError,
    DBNLRunNotFoundError,
    DBNLRunQueryNotFoundError,
    DBNLTagNotFoundError,
)
from dbnl.print_logging import dbnl_logger

from .models import (
    ColumnSchemaDict,
    Project,
    ResultData,
    Run,
    RunConfig,
    RunQuery,
    ScalarSchemaDict,
    TestSession,
    TestSessionInput,
)
from .util import (
    get_column_schemas_from_dataframe,
    get_default_components_dag_from_column_schemas,
    get_scalar_schemas_from_dataframe,
    make_test_session_input,
)
from .validate import (
    validate_column_data_against_run_config,
    validate_project,
    validate_run,
    validate_run_config,
    validate_run_config_id,
    validate_run_id,
    validate_scalar_data_against_run_config,
    validate_tags,
    validate_test_session_inputs,
)

T = TypeVar("T")
P = ParamSpec("P")


@contextmanager
def handle_api_validation_error() -> Iterator[None]:
    """
    Context manager to handle API validation errors
    """
    try:
        yield
    except DBNLAPIError as e:
        if e.status_code == HTTPStatus.BAD_REQUEST:
            resp_data = json.loads(e.response.text)
            if not isinstance(resp_data, dict):
                raise
            if resp_data.get("code") != "invalid_data":
                raise
            message = resp_data.get("message")
            if not isinstance(message, dict):
                raise
            error_info = message.get("json")
            if not isinstance(error_info, dict):
                raise
            raise DBNLAPIValidationError(error_info)
        raise


def login(
    *,
    api_token: Optional[str] = None,
    namespace_id: Optional[str] = None,
    api_url: Optional[str] = None,
    app_url: Optional[str] = None,
) -> None:
    """
    Set up DBNL SDK to make authenticated requests
    Minimum state recorded to be able to issue secure and authenticated
    requests against hosted endpoints.

    :param api_token: DBNL API token for authentication; token can be found at /tokens page of the DBNL app.
                    If None is provided, the environment variable `DBNL_API_TOKEN` will be used by default.
    :type api_token: Optional[str], optional
    :param namespace_id: DBNL namespace ID to use for the session; available namespaces can be found with `get_my_namespaces()`.
    :type namespace_id: Optional[str], optional
    :param api_url: DBNL base API URL; if None is provided, the environment variable `DBNL_API_URL` will be used by default.
    :type api_url: Optional[str], optional
    :param app_url: DBNL base app URL; if None is provided, the environment variable `DBNL_APP_URL` will be used by default.
    :type app_url: Optional[str], optional
    """
    CONFIG.clear_mutable_config()
    if api_url:
        CONFIG.dbnl_api_url = api_url

    if app_url:
        CONFIG.dbnl_app_url = app_url

    if api_token:
        CONFIG.dbnl_api_token = api_token

    dbnl.api._ensure_valid_token()
    dbnl.api._maybe_warn_invalid_version()

    if namespace_id:
        CONFIG.dbnl_namespace_id = namespace_id
        dbnl.api._ensure_valid_namespace()

    # set config that login() was successful
    CONFIG.dbnl_logged_in = True


def validate_login(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator to validate that the user has logged in before making a request
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        if not CONFIG.dbnl_logged_in:
            raise DBNLNotLoggedInError()
        return func(*args, **kwargs)

    return wrapper


@validate_login
def get_project(
    *,
    name: str,
) -> Project:
    """
    Retrieve a DBNL Project by name

    :param name: Name for the DBNL Project. Names for DBNL Projects must be unique.
    :type name: str

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLProjectNotFoundError: Project with the given name does not exist.

    :return: Project
    :rtype: Project
    """
    try:
        resp_dict = dbnl.api.get_project_by_name(name=name)
    except DBNLResourceNotFoundError:
        raise DBNLProjectNotFoundError(name)

    return Project.from_dict(resp_dict)


@validate_login
def create_project(
    *,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """
    Create a new DBNL Project

    :param name: Name for the DBNL Project
    :type name: str
    :param description: Description for the DBNL Project, defaults to None. Description is limited to 255 characters.
    :type description: Optional[str], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLAPIValidationError: DBNL API failed to validate the request
    :raises DBNLConflictingProjectError: Project with the same name already exists

    :return: Project
    :rtype: Project
    """
    try:
        with handle_api_validation_error():
            resp_dict = dbnl.api.post_projects(name=name, description=description)
    except DBNLDuplicateError:
        raise DBNLConflictingProjectError(name)

    namespace_param = f"ns/{CONFIG.dbnl_namespace_id}/" if CONFIG.dbnl_namespace_id else ""
    dbnl_logger.info(
        "View Project %s at: %s%sprojects/%s",
        name,
        CONFIG.dbnl_app_url,
        namespace_param,
        resp_dict["id"],
    )
    return Project.from_dict(resp_dict)


@validate_login
def get_or_create_project(
    *,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """
    Get the specified DBNL Project or create a new one if it does not exist

    :param name: Name for the DBNL Project
    :type name: str
    :param description: Description for the DBNL Project, defaults to None
    :type description: Optional[str], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLAPIValidationError: DBNL API failed to validate the request

    :return: Newly created or matching existing Project
    :rtype: Project
    """

    try:
        return get_project(name=name)
    except DBNLProjectNotFoundError:
        try:
            return create_project(name=name, description=description)
        except DBNLConflictingProjectError:
            return get_project(name=name)


@validate_login
def export_project_as_json(
    *,
    project: Project,
) -> dict[str, Any]:
    """
    Export a DBNL Project alongside its Test Specs and Tags as a JSON object

    :param project: DBNL Project to export.
    :type project: Project

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in

    :return: JSON object representing the Project. Example: {"project": {"name": "My Project",
             "description": "This is my project."}, "tags": [], "test_specs": []}
    :rtype: dict[str, Any]
    """
    try:
        return dbnl.api.get_project_export(project_id=project.id)
    except DBNLResourceNotFoundError:
        raise DBNLProjectNotFoundError(project.name)


@validate_login
def import_project_from_json(
    *,
    params: dict[str, Any],
) -> Project:
    """
    Create a new DBNL Project from a JSON object

    :param params: JSON object representing the Project, generally based on a Project exported via
                     `export_project_as_json()` or a similar structure. Example: {"project": {"name": "My Project",
                     "description": "This is my project."}, "tags": [], "test_specs": []}
    :type params: dict[str, Any]

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLAPIValidationError: DBNL API failed to validate the request
    :raises DBNLConflictingProjectError: Project with the same name already exists

    :return: Project created from the JSON object
    :rtype: Project
    """
    if not params.get("project"):
        raise DBNLInputValidationError("`project` is required in params")
    if not params["project"].get("name"):
        raise DBNLInputValidationError("`project.name` is required in params")

    try:
        with handle_api_validation_error():
            resp_dict = dbnl.api.post_project_import(params=params)
    except DBNLDuplicateError:
        raise DBNLConflictingProjectError(params["project"]["name"])

    project = Project.from_dict(resp_dict)

    namespace_param = f"ns/{CONFIG.dbnl_namespace_id}/" if CONFIG.dbnl_namespace_id else ""
    dbnl_logger.info(
        "View Project %s at: %s%sprojects/%s",
        project.name,
        CONFIG.dbnl_app_url,
        namespace_param,
        resp_dict["id"],
    )

    return project


@validate_login
def copy_project(
    *,
    project: Project,
    name: str,
    description: Optional[str] = None,
) -> Project:
    """
    Copy a DBNL Project; a convenience method wrapping exporting and importing a project with a new name and description

    :param project: DBNL Project to copy
    :type project: Project
    :param name: Name for the new DBNL Project
    :type name: str
    :param description: Description for the new DBNL Project, defaults to None. Description is limited to 255 characters.
    :type description: Optional[str], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    :raises DBNLConflictingProjectError: Project with the same name already exists

    :return: Copied Project
    :rtype: Project
    """
    if name == project.name:
        raise DBNLInputValidationError("New project name must be different from the original project name")

    params = export_project_as_json(project=project)
    params["project"]["name"] = name
    params["project"]["description"] = description
    return import_project_from_json(params=params)


@validate_login
def create_run_config(
    *,
    project: Project,
    columns: Sequence[ColumnSchemaDict],
    scalars: Optional[Sequence[ScalarSchemaDict]] = None,
    description: Optional[str] = None,
    display_name: Optional[str] = None,
    row_id: Optional[list[str]] = None,
    components_dag: Optional[dict[str, list[str]]] = None,
) -> RunConfig:
    """
    Create a new DBNL RunConfig

    :param project: DBNL Project this RunConfig is associated to
    :type project: Project
    :param columns: List of column schema specs for the uploaded data, required keys `name` and `type`, optional key `component`, `description` and `greater_is_better`.
                   `type` can be `int`, `float`, `category`, `boolean`, or `string`.
                   `component` is a string that indicates the source of the data. e.g. "component" : "sentiment-classifier" or "component" : "fraud-predictor".
                   Specified components must be present in the `components_dag` dictionary.
                   `greater_is_better` is a boolean that indicates if larger values are better than smaller ones. False indicates smaller values are better.
                   None indicates no preference.
                   An example RunConfig columns: columns=[{"name": "pred_proba", "type": "float", "component": "fraud-predictor"},
                   {"name": "decision", "type": "boolean", "component": "threshold-decision"}, {"name": "error_type", "type": "category"}]
    :type columns: list[ColumnSchemaDict]
    :param scalars: List of scalar schema specs for the uploaded data, required keys `name` and `type`, optional key `component`, `description` and `greater_is_better`.
                    `type` can be `int`, `float`, `category`, `boolean`, or `string`.
                    `component` is a string that indicates the source of the data. e.g. "component" : "sentiment-classifier" or "component" : "fraud-predictor".
                    Specified components must be present in the `components_dag` dictionary.
                   `greater_is_better` is a boolean that indicates if larger values are better than smaller ones. False indicates smaller values are better.
                   None indicates no preference.
                    An example RunConfig scalars: scalars=[{"name": "accuracy", "type": "float", "component": "fraud-predictor"},
                    {"name": "error_type", "type": "category"}]
    :type scalars: Optional[Sequence[ScalarSchemaDict]], optional
    :param description: Description for the DBNL RunConfig, defaults to None. Description is limited to 255 characters.
    :type description: Optional[str], optional
    :param display_name: Display name for the RunConfig, defaults to None. display_name does not have to be unique.
    :type display_name: Optional[str], optional
    :param row_id: List of column names that are the unique identifier, defaults to None.
    :type row_id: Optional[list[str]], optional
    :param components_dag: Optional dictionary representing the DAG of components, defaults to None.
                           eg : {"fraud-predictor": ['threshold-decision"], "threshold-decision": []},
    :type components_dag: Optional[dict[str, list[str]]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: RunConfig with the desired columns schema
    :rtype: RunConfig
    """
    try:
        validate_project(project)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))
    if components_dag is None:
        components_dag = get_default_components_dag_from_column_schemas(columns)

    with handle_api_validation_error():
        resp_dict = dbnl.api.post_run_configs(
            project_id=project.id,
            columns=[dict(c) for c in columns],
            scalars=[dict(s) for s in scalars or []],
            description=description,
            display_name=display_name,
            row_id=row_id,
            components_dag=components_dag,
        )
    return RunConfig.from_dict(resp_dict)


@validate_login
def get_run_config(
    *,
    run_config_id: str,
) -> RunConfig:
    """
    Reieve a DBNL RunConfig with the given ID

    :param run_config_id: The ID of the DBNL RunConfig to retrieve
    :type run_config_id: str

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: RunConfig with the given run_config_id
    :rtype: RunConfig
    """

    try:
        validate_run_config_id(run_config_id)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    try:
        resp_dict = dbnl.api.get_run_config_by_id(run_config_id=run_config_id)
    except DBNLResourceNotFoundError:
        raise DBNLRunConfigNotFoundError(run_config_id)

    return RunConfig.from_dict(resp_dict)


@validate_login
def create_run(
    *,
    project: Project,
    run_config: RunConfig,
    display_name: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> Run:
    """
    Create a new DBNL Run to test an app data

    :param project: DBNL Project this Run is associated to
    :type project: Project
    :param run_config: DBNL RunConfig to use for this Run
    :type run_config: RunConfig
    :param display_name: Display name for the Run, defaults to None. `display_name` does not have to be unique.
    :type display_name: Optional[str], optional
    :param metadata: Additional key:value pairs user wants to track, defaults to None
    :type metadata: Optional[dict[str, str]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Newly created Run
    :rtype: Run
    """

    try:
        validate_project(project)
        validate_run_config(run_config, project)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    with handle_api_validation_error():
        resp_dict = dbnl.api.post_runs(
            project_id=project.id,
            run_config_id=run_config.id,
            display_name=display_name,
            metadata=metadata,
        )
    if "run_config" not in resp_dict:
        resp_dict["run_config"] = run_config.to_dict()

    return Run.from_dict(resp_dict)


@validate_login
def report_column_results(
    *,
    run: Run,
    data: pd.DataFrame,
) -> None:
    """
    Report all results to DBNL

    :param run: DBNL Run the results will be reported to
    :type run: Run
    :param data: A pandas DataFrame with all the results to report to DBNL.
                 The columns of the DataFrame must match the columns of the RunConfig associated with the Run.
    :type data: pandas.DataFrame

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    """
    try:
        validate_run(run)
        if run.run_config is None:
            run_config = get_run_config(run_config_id=run.run_config_id)
        validate_column_data_against_run_config(run.run_config or run_config, data)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    dbnl.api.post_results(run_id=run.id, data=data, scalar=False)


@validate_login
def report_scalar_results(
    *,
    run: Run,
    data: Union[dict[str, Any], pd.DataFrame],
) -> None:
    """
    Report scalar results to DBNL

    :param run: DBNL Run the scalars will be reported to
    :type run: Run
    :param data: A dictionary or single-row pandas DataFrame with the scalar results to report to DBNL.
    :type data: Union[dict[str, Any], pd.DataFrame]

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    """
    if isinstance(data, dict):
        data = pd.DataFrame([data])
        run_config = run.run_config
        if run_config is None:
            run_config = get_run_config(run_config_id=run.run_config_id)
        if run_config.scalars is not None:
            for scalar_schema in run_config.scalars:
                if scalar_schema.type == "category":
                    data[scalar_schema.name] = data[scalar_schema.name].astype("category")

    try:
        validate_run(run)
        run_config = run.run_config
        if run_config is None:
            run_config = get_run_config(run_config_id=run.run_config_id)
        if run_config.scalars:
            validate_scalar_data_against_run_config(run_config, data)
        elif data.empty:
            pass  # if this is part of an automated workflow it would be better not to fail here
        else:
            raise DBNLInputValidationError("No scalars expected in run config")
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    if run_config.scalars:
        dbnl.api.post_results(run_id=run.id, data=data, scalar=True)


@validate_login
def report_results(
    *,
    run: Run,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
) -> None:
    """
    Report all results to DBNL

    :param run: DBNL Run the results will be reported to
    :type run: Run
    :param column_data: A pandas DataFrame with all the column results to report to DBNL.
                        The columns of the DataFrame must match the columns of the RunConfig associated with the Run.
    :type column_data: pandas.DataFrame
    :param scalar_data: A dictionary or single-row pandas DataFrame with the scalar results to report to DBNL, defaults to None.
    :type scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    """
    report_column_results(run=run, data=column_data)
    if scalar_data is not None:
        report_scalar_results(run=run, data=scalar_data)


@validate_login
def get_column_results(
    *,
    run: Run,
) -> pd.DataFrame:
    """
    Get all results for a Run

    :param run: DBNL Run to get results for
    :type run: Run

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: A pandas DataFrame with all the results for the Run
    :rtype: pandas.DataFrame
    """

    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    content = dbnl.api.get_results(run_id=run.id, scalar=False)
    return pd.read_parquet(BytesIO(content))


@validate_login
def get_scalar_results(
    *,
    run: Run,
) -> pd.DataFrame:
    """
    Get all scalar results for a Run

    :param run: DBNL Run to get scalar results for
    :type run: Run

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: A pandas DataFrame with all the scalar results for the Run
    :rtype: pandas.DataFrame
    """

    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    content = dbnl.api.get_results(run_id=run.id, scalar=True)
    return pd.read_parquet(BytesIO(content))


@validate_login
def get_results(
    *,
    run: Run,
) -> ResultData:
    """
    Get all results for a Run

    :param run: DBNL Run to get results for
    :type run: Run

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: ResultData object with all the results for the Run
    :rtype: ResultData
    """
    columns = get_column_results(run=run)
    if run.run_config is None:
        run_config = get_run_config(run_config_id=run.run_config_id)
        run.run_config = run_config
    scalars = get_scalar_results(run=run) if run.run_config.scalars else None
    return ResultData(columns=columns, scalars=scalars)


@validate_login
def get_run(
    *,
    run_id: str,
) -> Run:
    """
    Retrieve a DBNL Run with the given ID

    :param run_id: The ID of the DBNL Run to retrive
    :type run_id: str

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Run with the given run_id
    :rtype: Run
    """

    try:
        validate_run_id(run_id)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    try:
        resp_dict = dbnl.api.get_run_by_id(run_id=run_id)
    except DBNLResourceNotFoundError:
        raise DBNLRunNotFoundError(run_id)

    return Run.from_dict(resp_dict)


def _get_tag_id(
    *,
    project_id: str,
    name: str,
) -> str:
    """
    Retrieve a DBNL Tag ID by name

    :param project_id: The ID of the DBNL Project to search for the Tag
    :type project_id: str
    :param name: The unique name for the DBNL Test Tag.
    :type name: str

    :return: Tag ID
    :rtype: str
    """
    try:
        tag = dbnl.api.api_stubs.get_tag_by_name(project_id=project_id, name=name)
    except DBNLResourceNotFoundError:
        raise DBNLTagNotFoundError(tag_name=name, project_id=project_id)

    return str(tag["id"])


def _get_tag_ids(
    *,
    project_id: str,
    names: Optional[list[str]] = None,
) -> Optional[list[str]]:
    """
    Retrieve a list of DBNL Tag IDs by name

    :param project_id: The ID of the DBNL Project to search for the Tag
    :type project_id: str
    :param names: List of names for the DBNL Test Tags. Names for DBNL Tags must be unique.
    :type names: list[str]

    :return: List of Tag IDs
    :rtype: list[str]
    """
    if not names:
        return None
    return [_get_tag_id(project_id=project_id, name=tag_name) for tag_name in names]


@validate_login
def close_run(
    *,
    run: Run,
) -> None:
    """
    Finalize anything with the Run instance and mark it as completed.

    :param run: DBNL Run to be finalized
    :type run: Run

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format
    """

    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    dbnl.api.post_runs_close(run_id=run.id)

    namespace_param = f"ns/{CONFIG.dbnl_namespace_id}/" if CONFIG.dbnl_namespace_id else ""
    dbnl_logger.info(
        "Run closed. View results at: %s%sprojects/%s/runs/%s",
        CONFIG.dbnl_app_url,
        namespace_param,
        run.project_id,
        run.id,
    )


@validate_login
def get_my_namespaces() -> list[Any]:
    """
    Get all the namespaces that the user has access to

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in

    :return: List of namespaces
    :rtype: list[Any]
    """
    return dbnl.api.get_my_namespaces()


@validate_login
def get_latest_run_config(project: Project) -> RunConfig:
    """
    Get the latest RunConfig for a project

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLResourceNotFoundError: RunConfig not found

    :param project: DBNL Project to get the latest RunConfig for
    :type project: Project
    :return: Latest RunConfig
    :rtype: RunConfig
    """
    try:
        resp_dict = dbnl.api.get_latest_run_config(project_id=project.id)
    except DBNLResourceNotFoundError:
        raise DBNLRunConfigNotFoundError("latest")

    return RunConfig.from_dict(resp_dict)


@validate_login
def get_latest_run(project: Project) -> Run:
    """
    Get the latest Run for a project

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLResourceNotFoundError: Run not found

    :param project: DBNL Project to get the latest Run for
    :type project: Project
    :return: Latest Run
    :rtype: Run
    """
    try:
        resp_dict = dbnl.api.get_latest_run(project_id=project.id)
    except DBNLResourceNotFoundError:
        raise DBNLRunNotFoundError("latest")

    return Run.from_dict(resp_dict)


@validate_login
def get_run_config_from_latest_run(project: Project) -> RunConfig:
    """
    Get the RunConfig from the latest Run for a project

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLResourceNotFoundError: RunConfig not found

    :param project: DBNL Project to get the latest RunConfig for
    :type project: Project
    :return: RunConfig from the latest Run
    :rtype: RunConfig
    """
    latest_run = get_latest_run(project=project)
    if latest_run.run_config is None:
        raise DBNLRunConfigNotFoundError("latest")
    return latest_run.run_config


@validate_login
def create_run_config_from_results(
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    description: Optional[str] = None,
    display_name: Optional[str] = None,
    row_id: Optional[list[str]] = None,
) -> RunConfig:
    """
    Create a new RunConfig from the column results, and scalar results if provided

    :param project: DBNL Project to create the RunConfig for
    :type project: Project
    :param column_data: DataFrame with the results for the columns
    :type column_data: pd.DataFrame
    :param scalar_data: Dictionary or DataFrame with the results for the scalars, defaults to None
    :type scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]], optional
    :param description: Description for the RunConfig, defaults to None
    :type description: Optional[str], optional
    :param display_name: Display name for the RunConfig, defaults to None
    :type display_name: Optional[str], optional
    :param row_id: List of column names that are the unique identifier, defaults to None
    :type row_id: Optional[list[str]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: RunConfig with the desired schema for columns and scalars, if provided
    :rtype: RunConfig
    """
    columns = get_column_schemas_from_dataframe(column_data)
    if isinstance(scalar_data, dict):
        scalar_data = pd.DataFrame([scalar_data])
    scalars = get_scalar_schemas_from_dataframe(scalar_data) if scalar_data is not None else None

    return create_run_config(
        project=project,
        columns=columns,
        scalars=scalars,
        description=description,
        display_name=display_name,
        row_id=row_id,
    )


@validate_login
def report_run_with_results(
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    display_name: Optional[str] = None,
    row_id: Optional[list[str]] = None,
    run_config_id: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> Run:
    """
    Create a new Run, report results to it, and close it.

    Can derive a RunConfig from the results if not provided. If a RunConfig is provided, the results are validated against it.
    Can also skip automated tests after closing the Run, or include/exclude/require specific Test Tags.

    :param project: DBNL Project to create the Run for
    :type project: Project
    :param column_data: DataFrame with the results for the columns
    :type column_data: pd.DataFrame
    :param scalar_data: Dictionary or DataFrame with the results for the scalars, if any. Defaults to None
    :type scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]], optional
    :param display_name: Display name for the Run, defaults to None.
    :type display_name: Optional[str], optional
    :param row_id: List of column names that are the unique identifier, defaults to None. Only used if no `run_config_id` is provided.
    :type row_id: Optional[list[str]], optional
    :param run_config_id: ID of the RunConfig to use for the Run, defaults to None.
                          If provided, the RunConfig is used as is and the results are validated against it.
    :type run_config_id: Optional[str], optional
    :param metadata: Additional key:value pairs user wants to track, defaults to None
    :type metadata: Optional[dict[str, str]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Run, after reporting results and closing it
    :rtype: Run
    """
    if run_config_id:
        run_config = get_run_config(run_config_id=run_config_id)
        validate_column_data_against_run_config(run_config, column_data)
        if scalar_data is not None:
            if isinstance(scalar_data, dict):
                scalar_data = pd.DataFrame([scalar_data])
            validate_scalar_data_against_run_config(run_config, scalar_data)
            assert run_config.scalars is not None
            for scalar_schema in run_config.scalars:
                if scalar_schema.type == "category":
                    scalar_data[scalar_schema.name] = scalar_data[scalar_schema.name].astype("category")
    else:
        run_config = create_run_config_from_results(
            project=project,
            column_data=column_data,
            scalar_data=scalar_data,
            display_name=f"derived RunConfig for {display_name}",
            row_id=row_id,
        )
    run = create_run(project=project, run_config=run_config, display_name=display_name, metadata=metadata)
    report_results(run=run, column_data=column_data, scalar_data=scalar_data)
    close_run(run=run)
    return run


def _validate_run_query_query(query: dict[str, Any]) -> None:
    # currently, only 1 query is supported; we can iterate on how to support different queries in the future
    if (
        not isinstance(query, dict)
        or len(query) != 1
        or "offset_from_now" not in query
        or not isinstance(query["offset_from_now"], int)
        or query["offset_from_now"] < 1
    ):
        raise DBNLInputValidationError(
            "Query must be a dictionary, containing only 'offset_from_now' key with a positive integer value"
        )


@validate_login
def create_run_query(
    project: Project,
    name: str,
    query: dict[str, Any],
) -> RunQuery:
    """
    Create a new RunQuery for a project to use as a baseline Run.
    Currently supports key="offset_from_now" with value as a positive integer, representing
    the number of runs to go back for the baseline. For example, query={"offset_from_now": 1} will
    use the latest run as the baseline, so that each run compares against the previous run.

    :param project: DBNL Project to create the RunQuery for
    :type project: Project
    :param name: Name for the RunQuery
    :type name: str
    :param query: Query to use for the RunQuery
    :type query: dict[str, Any]

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: RunQuery
    :rtype: RunQuery
    """
    try:
        validate_project(project)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))
    _validate_run_query_query(query)

    with handle_api_validation_error():
        resp_dict = dbnl.api.post_run_query(project_id=project.id, name=name, query=query)
    return RunQuery.from_dict(resp_dict)


@validate_login
def get_run_query(
    project: Project,
    name: str,
) -> RunQuery:
    """
    Retrieve a DBNL RunQuery with the given name, unique to a project

    :param name: The name of the DBNL RunQuery to retrieve

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLRessourceNotFoundError: RunQuery not found

    :return: RunQuery with the given name
    :rtype: RunQuery
    """
    try:
        resp_dict = dbnl.api.get_run_query_by_name(project_id=project.id, name=name)
    except DBNLResourceNotFoundError:
        raise DBNLRunQueryNotFoundError(name)

    return RunQuery.from_dict(resp_dict)


@validate_login
def set_run_as_baseline(
    *,
    run: Run,
) -> None:
    """
    Set the given Run as the Baseline Run in the Project's Test Config

    :param run: The DBNL Run to set as the Baseline Run.
    :type run: Run

    :raises DBNLResourceNotFoundError: If the test configurations are not found for the project.
    """
    try:
        validate_run(run)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))
    try:
        test_config_dict = dbnl.api.get_test_configs(project_id=run.project_id)
    except DBNLResourceNotFoundError:
        raise DBNLResourceNotFoundError(f"Test Configs not found for Project {run.project_id}")

    test_config_id = test_config_dict["id"]
    dbnl.api.patch_test_configs(test_config_id=test_config_id, baseline_run_id=run.id)


@validate_login
def set_run_query_as_baseline(
    *,
    run_query: RunQuery,
) -> None:
    """
    Set the given query as the query for the Run in the Project's Test Config

    :param run_query: The DBNL Run Query to set as the Baseline Run Query.
    :type run_query: RunQuery

    :raises DBNLResourceNotFoundError: If the test configurations are not found for the project.
    """
    try:
        test_config_dict = dbnl.api.get_test_configs(project_id=run_query.project_id)
    except DBNLResourceNotFoundError:
        raise DBNLResourceNotFoundError(f"Test Configs not found for Project {run_query.project_id}")

    test_config_id = test_config_dict["id"]
    dbnl.api.patch_test_configs(test_config_id=test_config_id, baseline_run_query_id=run_query.id)


@validate_login
def _get_default_baseline_input(project_id: str) -> TestSessionInput:
    test_config = dbnl.api.get_test_configs(project_id=project_id)
    if test_config["baseline_type"] == "RUN_ID":
        return TestSessionInput(
            run_alias="BASELINE",
            run_id=test_config["baseline_run_id"],
        )
    if test_config["baseline_type"] == "RUN_QUERY":
        return TestSessionInput(
            run_alias="BASELINE",
            run_query_id=test_config["baseline_run_query_id"],
        )
    raise ValueError(f"No baseline input found in test config: {test_config}.")


@validate_login
def create_test_session(
    *,
    experiment_run: Run,
    baseline: Optional[Union[Run, RunQuery]] = None,
    include_tags: Optional[list[str]] = None,
    exclude_tags: Optional[list[str]] = None,
    require_tags: Optional[list[str]] = None,
) -> TestSession:
    """
    Create a new TestSession with the given run as the experiment run.

    :param experiment_run: DBNL Run to create the TestSession for
    :type experiment_run: Run
    :param baseline: DBNL Run or RunQuery to use as the baseline run, defaults to None. If None, the baseline defined in the TestConfig is used.
    :type baseline: Optional[Union[Run, RunQuery]], optional
    :param include_tags: List of Test Tag names to include in the Test Session, defaults to None
    :type include_tags: Optional[list[str]], optional
    :param exclude_tags: List of Test Tag names to exclude in the Test Session, defaults to None
    :type exclude_tags: Optional[list[str]], optional
    :param require_tags: List of Test Tag names to require in the Test Session, defaults to None
    :type require_tags: Optional[list[str]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: TestSession
    :rtype: TestSession
    """
    test_session_inputs = [make_test_session_input(run=experiment_run)]
    if isinstance(baseline, Run):
        baseline_input = make_test_session_input(run=baseline, run_alias="BASELINE")
        test_session_inputs.append(baseline_input)
    elif isinstance(baseline, RunQuery):
        baseline_input = make_test_session_input(run_query=baseline, run_alias="BASELINE")
        test_session_inputs.append(baseline_input)
    else:
        baseline_input = _get_default_baseline_input(project_id=experiment_run.project_id)
        test_session_inputs.append(baseline_input)

    try:
        validate_tags(include_tags, exclude_tags, require_tags)
        validate_test_session_inputs(test_session_inputs)
    except ValueError as e:
        raise DBNLInputValidationError(str(e))

    include_tag_ids = _get_tag_ids(project_id=experiment_run.project_id, names=include_tags)
    exclude_tag_ids = _get_tag_ids(project_id=experiment_run.project_id, names=exclude_tags)
    require_tag_ids = _get_tag_ids(project_id=experiment_run.project_id, names=require_tags)

    with handle_api_validation_error():
        resp_dict = dbnl.api.post_test_session(
            project_id=experiment_run.project_id,
            inputs=[input_.to_dict() for input_ in test_session_inputs],
            include_tag_ids=include_tag_ids,
            exclude_tag_ids=exclude_tag_ids,
            require_tag_ids=require_tag_ids,
        )
    return TestSession.from_dict(resp_dict)


@validate_login
def report_run_with_results_and_start_test_session(
    *,
    project: Project,
    column_data: pd.DataFrame,
    scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]] = None,
    display_name: Optional[str] = None,
    row_id: Optional[list[str]] = None,
    run_config_id: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
    baseline: Optional[Union[Run, RunQuery]] = None,
    include_tags: Optional[list[str]] = None,
    exclude_tags: Optional[list[str]] = None,
    require_tags: Optional[list[str]] = None,
) -> Run:
    """
    Create a new Run, report results to it, and close it. Start a TestSession with the given inputs.

    :param project: DBNL Project to create the Run for
    :type project: Project
    :param column_data: DataFrame with the results for the columns
    :type column_data: pd.DataFrame
    :param scalar_data: Dictionary or DataFrame with the results for the scalars, if any. Defaults to None
    :type scalar_data: Optional[Union[dict[str, Any], pd.DataFrame]], optional
    :param display_name: Display name for the Run, defaults to None.
    :type display_name: Optional[str], optional
    :param row_id: List of column names that are the unique identifier, defaults to None. Only used if no `run_config_id` is provided.
    :type row_id: Optional[list[str]], optional
    :param run_config_id: ID of the RunConfig to use for the Run, defaults to None.
    :type run_config_id: Optional[str], optional
    :param metadata: Additional key:value pairs user wants to track, defaults to None
    :type metadata: Optional[Dict[str, str]], optional
    :param baseline: DBNL Run or RunQuery to use as the baseline run, defaults to None. If None, the baseline defined in the TestConfig is used.
    :type baseline: Optional[Union[Run, RunQuery]], optional
    :param include_tags: List of Test Tag names to include in the Test Session
    :type include_tags: Optional[list[str]], optional
    :param exclude_tags: List of Test Tag names to exclude in the Test Session
    :type exclude_tags: Optional[list[str]], optional
    :param require_tags: List of Test Tag names to require in the Test Session
    :type require_tags: Optional[list[str]], optional

    :raises DBNLNotLoggedInError: DBNL SDK is not logged in
    :raises DBNLInputValidationError: Input does not conform to expected format

    :return: Run, after reporting results and closing it
    :rtype: Run
    """
    run = report_run_with_results(
        project=project,
        column_data=column_data,
        scalar_data=scalar_data,
        display_name=display_name,
        row_id=row_id,
        run_config_id=run_config_id,
        metadata=metadata,
    )
    create_test_session(
        experiment_run=run,
        baseline=baseline,
        include_tags=include_tags,
        exclude_tags=exclude_tags,
        require_tags=require_tags,
    )
    return run
