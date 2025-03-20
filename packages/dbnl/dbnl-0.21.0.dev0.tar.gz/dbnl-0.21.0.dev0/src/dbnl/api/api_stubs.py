from __future__ import annotations

import json
import warnings
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from functools import lru_cache
from typing import Any, Optional
from urllib.parse import urlparse, urlunparse

import pandas as pd
import pyarrow
import requests

from dbnl import __version__ as sdk_version
from dbnl.api.version import check_version_compatibility
from dbnl.config import CONFIG
from dbnl.errors import (
    DBNLAPIError,
    DBNLAuthenticationError,
    DBNLConfigurationError,
    DBNLConnectionError,
    DBNLDownloadResultsError,
    DBNLDownloadRunNotClosedError,
    DBNLDuplicateError,
    DBNLResourceNotFoundError,
    DBNLUploadResultsError,
    DBNLUploadRunClosedError,
)
from dbnl.warnings import DBNLAPIIncompatibilityWarning

_NOT_NAMESPACED_RESOURCES = {
    "namespaces",
    "namespace_roles",
    "namespace_role_assignments",
    "org",
    "users",
}


def is_namespaced(resource_name: str) -> bool:
    resource_base = resource_name.split("/", 1)[0]
    return resource_base not in _NOT_NAMESPACED_RESOURCES


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        r.headers["authorization"] = "Bearer " + self.token
        return r


def _request(
    *,
    method: str,
    resource_name: str,
    query_params: Optional[dict[str, Any]] = None,
    json_payload: Optional[dict[str, Any]] = None,
) -> requests.Response:
    path = "/".join(["v0", resource_name])
    parsed = urlparse(CONFIG.dbnl_api_url)
    _url = urlunparse(parsed._replace(path=parsed.path + path))
    _query_params: Optional[dict[str, Any]] = {}
    if is_namespaced(resource_name) and CONFIG.dbnl_namespace_id:
        _query_params = {"namespace_id": CONFIG.dbnl_namespace_id}
    if query_params:
        assert _query_params is not None  # for type checker
        _query_params.update(query_params)
    if not _query_params:
        _query_params = None

    try:
        response = requests.request(
            method,
            url=_url,
            params=_query_params,
            auth=BearerAuth(CONFIG.dbnl_api_token),
            json=json_payload,
            headers={"User-Agent": f"dbnl/{sdk_version}"},
            timeout=10,
        )
    except requests.exceptions.RequestException as re:
        raise DBNLConnectionError(_url, str(re)) from re
    return response


def _parse_response(response: requests.Response) -> dict[str, Any]:
    if response.status_code == 200:
        return dict(json.loads(response.text))
    elif response.status_code == 400:
        error_dict = json.loads(response.text)
        if error_dict and error_dict.get("code", "").startswith("duplicate"):
            raise DBNLDuplicateError()
        else:
            raise DBNLAPIError(response)
    elif response.status_code == 404:
        raise DBNLResourceNotFoundError()
    else:
        raise DBNLAPIError(response)


def _parse_query_response(response: requests.Response) -> dict[str, Any]:
    parsed_response = _parse_response(response)
    if len(parsed_response["data"]) == 0:
        raise DBNLResourceNotFoundError()
    return dict(parsed_response["data"][0])


def get_project_by_name(
    *,
    name: str,
) -> dict[Any, Any]:
    _query_params = {"name": name}

    response = _request(method="GET", resource_name="projects", query_params=_query_params)
    return _parse_query_response(response)


def post_projects(
    *,
    name: str,
    description: Optional[str] = None,
) -> dict[str, Any]:
    json_payload = {"name": name}
    if description is not None:
        json_payload.update({"description": description})

    response = _request(method="POST", resource_name="projects", json_payload=json_payload)
    return _parse_response(response)


def get_project_export(
    *,
    project_id: str,
) -> dict[str, Any]:
    response = _request(method="GET", resource_name=f"projects/{project_id}/export")
    return _parse_response(response)


def post_project_import(
    *,
    params: dict[str, Any],
) -> dict[str, Any]:
    response = _request(method="POST", resource_name="projects/import", json_payload=params)
    return _parse_response(response)


def post_runs(
    *,
    project_id: str,
    run_config_id: str,
    display_name: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    json_payload: dict[str, Any] = {
        "project_id": project_id,
        "run_config_id": run_config_id,
    }
    if display_name is not None:
        json_payload.update({"display_name": display_name})
    if metadata is not None:
        json_payload.update({"metadata": metadata})

    response = _request(method="POST", resource_name="runs", json_payload=json_payload)
    return _parse_response(response)


def get_run_by_id(
    *,
    run_id: str,
) -> dict[Any, Any]:
    _query_params = {"expand": "run_config"}

    response = _request(method="GET", resource_name=f"runs/{run_id}", query_params=_query_params)
    return _parse_response(response)


def post_runs_generate_upload_url(
    *,
    run_id: str,
    scalar: bool,
) -> dict[str, Any]:
    response = _request(
        method="POST",
        resource_name=f"runs/{run_id}/generate_upload_url",
        query_params={"dimensionality": "SCALAR"} if scalar else {},
    )
    if response.status_code == 400 and json.loads(response.text).get("message").startswith("Run already closed"):
        raise DBNLUploadRunClosedError(run_id)

    return _parse_response(response)


def post_runs_close(
    *,
    run_id: str,
) -> None:
    response = _request(method="POST", resource_name=f"runs/{run_id}/close")
    _ = _parse_response(response)


@lru_cache(maxsize=32)
def get_tag_by_name(
    *,
    project_id: str,
    name: str,
) -> dict[str, Any]:
    response = _request(method="GET", resource_name="tags", query_params={"project_id": project_id, "name": name})
    return _parse_query_response(response)


def post_tags(
    *,
    project_id: str,
    name: str,
    description: Optional[str] = None,
) -> dict[str, Any]:
    json_payload = {"project_id": project_id, "name": name}
    if description is not None:
        json_payload.update({"description": description})

    response = _request(method="POST", resource_name="tags", json_payload=json_payload)
    return _parse_response(response)


def post_run_configs(
    *,
    project_id: str,
    columns: list[dict[str, Any]],
    scalars: Optional[list[dict[str, Any]]],
    description: Optional[str] = None,
    display_name: Optional[str] = None,
    row_id: Optional[list[str]] = None,
    components_dag: Optional[dict[str, list[str]]] = None,
) -> dict[str, Any]:
    json_payload: dict[str, Any] = {"project_id": project_id, "columns": columns, "scalars": scalars}
    if description is not None:
        json_payload.update({"description": description})
    if display_name is not None:
        json_payload.update({"display_name": display_name})
    if row_id is not None:
        json_payload.update({"row_id": row_id})
    if components_dag is not None:
        json_payload.update({"components_dag": components_dag})

    response = _request(method="POST", resource_name="run_configs", json_payload=json_payload)
    return _parse_response(response)


def get_run_config_by_id(
    *,
    run_config_id: str,
) -> dict[str, Any]:
    response = _request(method="GET", resource_name=f"run_configs/{run_config_id}")
    return _parse_response(response)


def _parse_error_from_xml(response: requests.Response) -> str | None:
    try:
        response_xml = ET.fromstring(response.text)
    except ET.ParseError:
        return None
    ecode_elem = response_xml.find(".//Code")
    emessage_elem = response_xml.find(".//Message")
    if ecode_elem is None or emessage_elem is None:
        response.raise_for_status()
    assert ecode_elem is not None  # for type checker
    assert emessage_elem is not None  # for type checker
    error_code = ecode_elem.text
    error_message = emessage_elem.text
    return f"{error_code}: {error_message}"


def post_results(
    *,
    run_id: str,
    data: pd.DataFrame,
    scalar: bool,
) -> None:
    upload_details = post_runs_generate_upload_url(run_id=run_id, scalar=scalar)
    # Write DataFrame to memory buffer as parquet
    data_buffer = pyarrow.BufferOutputStream()
    data.to_parquet(data_buffer, index=False)

    # TODO(ENG-673): Can this be done more clearly / robustly?
    # GCS requires PUT method and uploads raw data rather than POST + files
    files: Mapping[str, pyarrow.lib.Buffer] | None
    if upload_details["method"] == "PUT" and not upload_details["data"]:
        upload_details["data"] = data_buffer.getvalue()
        files = None
    else:
        files = {"file": data_buffer.getvalue()}

    response = requests.request(
        method=upload_details["method"],
        url=upload_details["url"],
        data=upload_details["data"],
        files=files,  # type: ignore[arg-type]
        # TODO(ENG-673): change from get() to required after backend update released
        headers=upload_details.get("headers"),
    )

    if response.status_code >= 400:
        error_detail = _parse_error_from_xml(response) or response.text

        raise DBNLUploadResultsError(
            run_id,
            error_detail,
            upload_details["url"],
        )


def _validate_authenticated_response(response: requests.Response) -> None:
    if response.status_code == 401 and json.loads(response.text).get("code") == "auth_error":
        raise DBNLAuthenticationError(app_url=CONFIG.dbnl_app_url)
    if response.status_code != 200:
        raise DBNLAPIError(response)


def _maybe_warn_invalid_version() -> None:
    response = _request(method="GET", resource_name="spec.json")

    if response.status_code != 200:
        warnings.warn(
            f"Failed to fetch OpenAPI spec: {response.status_code}. Cannot validate API version compatability with SDK.",
            DBNLAPIIncompatibilityWarning,
        )
        return

    try:
        spec = json.loads(response.text)
        api_version = spec.get("info", {}).get("version")
        check_version_compatibility(api_version)
    except json.JSONDecodeError:
        warnings.warn(
            "Failed to parse OpenAPI spec. Cannot validate API version compatability with SDK.",
            DBNLAPIIncompatibilityWarning,
        )


def _ensure_valid_token() -> None:
    response = _request(method="GET", resource_name="users/me")
    _validate_authenticated_response(response)
    try:
        # A bad DBNL_API_URL may still return a 200. Sanity check the response.
        me = json.loads(response.text)
        assert me.get("id", "").startswith("user_")
    except (json.JSONDecodeError, AttributeError, AssertionError):
        raise DBNLConfigurationError(
            "Failed to validate user token against the dbnl API. Likely your DBNL_API_URL is incorrect. "
            f"Current value is {CONFIG.dbnl_api_url}"
        )


def get_me() -> dict[str, Any]:
    response = _request(method="GET", resource_name="users/me")
    _validate_authenticated_response(response)
    return _parse_response(response)


def get_org() -> dict[str, Any]:
    response = _request(method="GET", resource_name="org")
    _validate_authenticated_response(response)
    return _parse_response(response)


def post_test_specs(
    *,
    test_spec_dict: dict[str, Any],
) -> dict[str, Any]:
    response = _request(method="POST", resource_name="test_specs", json_payload=test_spec_dict)
    return _parse_response(response)


def get_test_sessions(
    *,
    project_id: str,
    experiment_run_id: Optional[str] = None,
    offset: Optional[int] = 0,
) -> dict[str, Any]:
    _query_params = {
        "project_id": project_id,
        "expand": ["author", "inputs.run", "include_tags", "exclude_tags"],
        "offset": offset,
        "desc": True,
        "sort_by": "CREATED_AT",
    }
    # optionally add experiment_run_id to params
    if experiment_run_id:
        _query_params.update({"experiment_run_id": f"{experiment_run_id}"})

    response = _request(method="GET", resource_name="test_sessions", query_params=_query_params)
    return _parse_response(response)


def get_test_session(
    *,
    test_session_id: str,
) -> dict[str, Any]:
    response = _request(method="GET", resource_name=f"test_sessions/{test_session_id}")
    return _parse_response(response)


def post_test_generation_session(
    *,
    project_id: str,
    run_id: str,
    columns: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    json_payload: dict[str, Any] = {"project_id": project_id, "run_id": run_id}
    if columns:
        json_payload.update({"columns": columns})
    response = _request(method="POST", resource_name="test_generation_sessions", json_payload=json_payload)
    return _parse_response(response)


def get_test_generation_session(
    *,
    test_generation_session_id: str,
) -> dict[str, Any]:
    response = _request(method="GET", resource_name=f"test_generation_sessions/{test_generation_session_id}")
    return _parse_response(response)


def post_test_recalibration_session(
    *,
    project_id: str,
    test_session_id: str,
    feedback: str,
    test_ids: Optional[list[str]] = None,
) -> dict[str, Any]:
    json_payload: dict[str, Any] = {"project_id": project_id, "test_session_id": test_session_id, "feedback": feedback}
    if test_ids:
        json_payload.update({"test_ids": test_ids})
    response = _request(method="POST", resource_name="test_recalibration_sessions", json_payload=json_payload)
    return _parse_response(response)


def get_test_recalibration_session(
    *,
    test_recalibration_session_id: str,
) -> dict[str, Any]:
    response = _request(method="GET", resource_name=f"test_recalibration_sessions/{test_recalibration_session_id}")
    return _parse_response(response)


def get_tests(
    *,
    test_session_id: str,
    offset: Optional[int] = 0,
) -> dict[str, Any]:
    _query_params = {
        "test_session_id": f"{test_session_id}",
        "sort_by": "NAME",
        "offset": f"{offset}",
    }
    response = _request(method="GET", resource_name="tests", query_params=_query_params)
    return _parse_response(response)


def patch_test_configs(
    *,
    test_config_id: str,
    baseline_run_id: Optional[str] = None,
    baseline_run_query_id: Optional[str] = None,
) -> None:
    if bool(baseline_run_id) == bool(baseline_run_query_id):
        raise ValueError("Exactly one of baseline_run_id and baseline_run_query_id must be provided")
    if baseline_run_id:
        json_payload = {"baseline_run_id": baseline_run_id}
    else:
        assert baseline_run_query_id is not None  # for type checker
        json_payload = {"baseline_run_query_id": baseline_run_query_id}
    response = _request(method="PATCH", resource_name=f"test_configs/{test_config_id}", json_payload=json_payload)
    _parse_response(response)


def get_test_configs(
    *,
    project_id: str,
) -> dict[str, Any]:
    _query_params = {"project_id": project_id}
    response = _request(method="GET", resource_name="test_configs", query_params=_query_params)
    return _parse_query_response(response)


def post_runs_generate_download_url(
    *,
    run_id: str,
    scalar: bool,
) -> dict[str, Any]:
    query_params = {"dimensionality": "SCALAR"} if scalar else {}
    response = _request(method="POST", resource_name=f"runs/{run_id}/generate_download_url", query_params=query_params)
    if response.status_code == 400 and json.loads(response.text).get("message").startswith("Run not closed"):
        raise DBNLDownloadRunNotClosedError(run_id)

    return _parse_response(response)


def get_results(
    *,
    run_id: str,
    scalar: bool,
) -> Any:
    download_details = post_runs_generate_download_url(run_id=run_id, scalar=scalar)
    response = requests.request(
        method=download_details["method"],
        url=download_details["url"],
    )

    if response.status_code >= 400:
        error_detail = _parse_error_from_xml(response) or response.text

        raise DBNLDownloadResultsError(
            run_id,
            error_detail,
            download_details["url"],
        )

    return response.content


def get_namespaces() -> dict[str, Any]:
    response = _request(method="GET", resource_name="namespaces")
    return _parse_response(response)


def get_my_namespaces() -> list[Any]:
    # NOTE: could change to users/me/permissions or users/me/namespaces, once available
    me = get_me()
    namespace_role_assignments = _parse_response(
        _request(
            method="GET",
            resource_name="namespace_role_assignments",
            query_params={"user_id": me["id"]},
        )
    )
    my_namespace_ids = set(assignment["namespace_id"] for assignment in namespace_role_assignments["data"])

    all_namespaces = get_namespaces()["data"]
    my_namespaces = [namespace for namespace in all_namespaces if namespace["id"] in my_namespace_ids]
    return my_namespaces


def _ensure_valid_namespace() -> None:
    response = _request(method="GET", resource_name="projects")
    _validate_authenticated_response(response)


def get_latest_run_config(project_id: str) -> dict[str, Any]:
    response = _request(
        method="GET",
        resource_name="run_configs",
        query_params={"project_id": project_id, "sort_by": "CREATED_AT", "desc": True, "limit": 1},
    )
    return _parse_query_response(response)


def get_latest_run(project_id: str) -> dict[str, Any]:
    response = _request(
        method="GET",
        resource_name="runs",
        query_params={
            "project_id": project_id,
            "sort_by": "CREATED_AT",
            "desc": True,
            "limit": 1,
            "expand": "run_config",
        },
    )
    return _parse_query_response(response)


def post_run_query(
    *,
    project_id: str,
    name: str,
    query: dict[str, Any],
) -> dict[str, Any]:
    json_payload = {"project_id": project_id, "name": name, "query": query}
    response = _request(method="POST", resource_name="run_queries", json_payload=json_payload)
    return _parse_response(response)


def get_run_query_by_name(
    *,
    project_id: str,
    name: str,
) -> dict[str, Any]:
    response = _request(
        method="GET", resource_name="run_queries", query_params={"project_id": project_id, "name": name}
    )
    return _parse_query_response(response)


def post_test_session(
    *,
    project_id: str,
    inputs: list[dict[str, Any]],
    include_tag_ids: Optional[list[str]] = None,
    exclude_tag_ids: Optional[list[str]] = None,
    require_tag_ids: Optional[list[str]] = None,
) -> dict[str, Any]:
    json_payload: dict[str, Any] = {"project_id": project_id, "inputs": inputs}
    if include_tag_ids is not None:
        json_payload.update({"include_tag_ids": include_tag_ids})
    if exclude_tag_ids is not None:
        json_payload.update({"exclude_tag_ids": exclude_tag_ids})
    if require_tag_ids is not None:
        json_payload.update({"require_tag_ids": require_tag_ids})

    response = _request(method="POST", resource_name="test_sessions", json_payload=json_payload)
    return _parse_response(response)


def get_spec() -> dict[str, Any]:
    response = _request(method="GET", resource_name="spec.json")
    return _parse_response(response)
