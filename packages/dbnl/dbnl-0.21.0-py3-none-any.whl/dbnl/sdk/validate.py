from typing import Any, Optional, Union

import pandas as pd
import pyarrow
from pyarrow import types as pa_types

from .models import (
    ContainerTypeLiteral,
    PrimitiveTypeLiteral,
    Project,
    Run,
    RunConfig,
    TestSessionInput,
)

MAX_CHAR_LENGTH = 100

DBNL_TYPE_TO_PYARROW_TYPE: dict[Union[PrimitiveTypeLiteral, ContainerTypeLiteral], Any] = {
    "string": pa_types.is_string,
    "float": pa_types.is_floating,
    "double": pa_types.is_floating,
    "int": pa_types.is_integer,
    "long": pa_types.is_integer,
    "boolean": pa_types.is_boolean,
    "category": pa_types.is_dictionary,
    "list": pa_types.is_list,
}


def is_string(input: str) -> bool:
    return isinstance(input, str)


def validate_string(resource_field_name: str, input: str, max_char: int = MAX_CHAR_LENGTH) -> None:
    if not is_string(input):
        raise ValueError(f"Expected {resource_field_name} to be a string, not {type(input).__name__}")
    if not input:
        raise ValueError(f"Expected {resource_field_name} to be a non-empty string")
    if len(input) > max_char:
        raise ValueError(f"Expected {resource_field_name} to be less than {max_char} characters")


def _validate_id(resource_field_name: str, resource_id: str, prefix: str) -> None:
    validate_string(resource_field_name, resource_id)
    if not resource_id.startswith(prefix):
        raise ValueError(f"Expected {resource_field_name} to start with `{prefix}`")
    if not resource_id[len(prefix) :].isalnum():
        raise ValueError(f"Expected {resource_field_name} to be alphanumeric after `{prefix}`")


def validate_project_id(project_id: str) -> None:
    _validate_id("Project id", project_id, "proj_")


def validate_run_id(run_id: str) -> None:
    _validate_id("Run id", run_id, "run_")


def validate_run_query_id(run_query_id: str) -> None:
    _validate_id("Run query id", run_query_id, "runqry_")


def validate_run_config_id(run_config_id: str) -> None:
    _validate_id("RunConfig id", run_config_id, "runcfg_")


def validate_project(project: Project) -> None:
    if not isinstance(project, Project):
        raise ValueError(f"Expected a Project, not {type(project).__name__}")


def validate_run(run: Run) -> None:
    if not isinstance(run, Run):
        raise ValueError(f"Expected a Run, not {type(run).__name__}")


def validate_run_config(run_config: RunConfig, project: Project) -> None:
    if not isinstance(run_config, RunConfig):
        raise ValueError(f"Expected a RunConfig, not {type(run_config).__name__}")

    if run_config.project_id != project.id:
        raise ValueError(f"Expected RunConfig project_id {run_config.project_id} to match Project id {project.id}")


def validate_column_data_against_run_config(run_config: RunConfig, data: pd.DataFrame) -> None:
    if not isinstance(data, pd.DataFrame):
        raise ValueError(f"Expected `data` to be a pandas DataFrame, not {type(data).__name__}")

    if data.shape[0] == 0:
        raise ValueError("Expected `data` to be a non-empty DataFrame")

    run_config_col_names = [col.name for col in run_config.columns]
    data_col_names = data.columns.values
    if not set(run_config_col_names) == set(data_col_names):
        raise ValueError("Expected data column names to match run_config column names")

    df_schema = {s.name: s.type for s in pyarrow.Schema.from_pandas(data)}
    for col in run_config.columns:
        col_name = col.name
        col_type = col.type
        if col_type not in DBNL_TYPE_TO_PYARROW_TYPE:
            raise ValueError(f"Unsupported data type: {col_type}")
        pyarrow_type = DBNL_TYPE_TO_PYARROW_TYPE[col_type]  # type: ignore[index]
        if not pyarrow_type(df_schema[col_name]):
            raise ValueError(
                f"Expected data column `{col_name}` to be of type `{col_type}`, not `{df_schema[col_name]}`"
            )
        if col_type in ["list", "category"]:
            value_type = df_schema[col_name].value_type
            if not pa_types.is_string(value_type):
                raise ValueError(
                    f"Expected data column `{col_name}` to be {col_type} of strings, not category of `{value_type}`"
                )

    if run_config.row_id is not None:
        if data.duplicated(subset=run_config.row_id).any():
            raise ValueError(
                f"Expected data columns {run_config.row_id} to be unique. Run `data.duplicated(subset=run_config.row_id)` to view the duplicated rows"
            )


def validate_scalar_data_against_run_config(run_config: RunConfig, scalars: pd.DataFrame) -> None:
    assert run_config.scalars, "Check that the RunConfig's scalars property is non-empty"
    if not isinstance(scalars, pd.DataFrame):
        raise ValueError(f"Expected `scalars` to be a pandas DataFrame, not {type(scalars).__name__}")
    if scalars.shape[0] != 1:
        raise ValueError("Expected `scalars` to have only one row")
    run_config_scalar_names = [scalar.name for scalar in run_config.scalars]
    scalar_names = scalars.columns.values
    if not set(run_config_scalar_names) == set(scalar_names):
        raise ValueError("Expected data scalars names to match run_config scalar names")

    df_schema = {s.name: s.type for s in pyarrow.Schema.from_pandas(scalars)}
    for scalar in run_config.scalars:
        scalar_name = scalar.name
        scalar_type = scalar.type
        if scalar_type not in DBNL_TYPE_TO_PYARROW_TYPE:
            raise ValueError(f"Unsupported data type: {scalar_type}")
        if scalar_type == "category" and pa_types.is_string(df_schema[scalar_name]):
            continue
        pyarrow_type = DBNL_TYPE_TO_PYARROW_TYPE[scalar_type]  # type: ignore[index]
        if not pyarrow_type(df_schema[scalar_name]):
            raise ValueError(
                f"Expected scalars column `{scalar_name}` to be of type `{scalar_type}`, not `{df_schema[scalar_name]}`"
            )


def validate_tags(
    include_tags: Optional[list[str]] = None,
    exclude_tags: Optional[list[str]] = None,
    require_tags: Optional[list[str]] = None,
) -> None:
    if include_tags is not None:
        if not isinstance(include_tags, list):
            raise ValueError(f"Expected `include_tags` to be a list of tag names, not {type(include_tags).__name__}")
        if len(set(include_tags)) != len(include_tags):
            raise ValueError("Expected `include_tags` to contain unique tags")
        for tag in include_tags:
            validate_string("Tag", tag)

    if exclude_tags is not None:
        if not isinstance(exclude_tags, list):
            raise ValueError(f"Expected `exclude_tags` to be a list of tag names, not {type(exclude_tags).__name__}")
        if len(set(exclude_tags)) != len(exclude_tags):
            raise ValueError("Expected `exclude_tags` to contain unique tags")
        for tag in exclude_tags:
            validate_string("Tag", tag)

    if require_tags is not None:
        if not isinstance(require_tags, list):
            raise ValueError(f"Expected `require_tags` to be a list of tag names, not {type(require_tags).__name__}")
        if len(set(require_tags)) != len(require_tags):
            raise ValueError("Expected `require_tags` to contain unique tags")
        for tag in require_tags:
            validate_string("Tag", tag)

    if include_tags is not None and exclude_tags is not None:
        if set(include_tags).intersection(set(exclude_tags)):
            raise ValueError(
                f"Expected `include_tags` and `exclude_tags` to be mutually exclusive. Overlapping tags: {set(include_tags).intersection(set(exclude_tags))}"
            )

    if require_tags is not None and exclude_tags is not None:
        if set(require_tags).intersection(set(exclude_tags)):
            raise ValueError(
                f"Expected `require_tags` and `exclude_tags` to be mutually exclusive. Overlapping tags: {set(require_tags).intersection(set(exclude_tags))}"
            )

    if require_tags is not None and include_tags is not None:
        if set(require_tags).intersection(set(include_tags)):
            raise ValueError(
                f"Expected `require_tags` and `include_tags` to be mutually exclusive. Overlapping tags: {set(require_tags).intersection(set(include_tags))}"
            )


def validate_test_session_input(input_: TestSessionInput) -> None:
    if not isinstance(input_, TestSessionInput):
        raise ValueError(f"Expected a TestSessionInput, not {type(input_).__name__}")

    if input_.run_alias not in ("EXPERIMENT", "BASELINE"):
        raise ValueError("Expected `run_alias` to be one of 'EXPERIMENT' or 'BASELINE'")

    if bool(input_.run_id) == bool(input_.run_query_id):
        raise ValueError("Expected exactly one of  `run_id` or `run_query_id`")

    if input_.run_id:
        validate_run_id(input_.run_id)

    if input_.run_query_id:
        validate_run_query_id(input_.run_query_id)


def validate_test_session_inputs(inputs: list[TestSessionInput]) -> None:
    if not isinstance(inputs, list):
        raise ValueError(f"Expected a list of TestSessionInput, not {type(inputs).__name__}")

    if len(inputs) != 2:
        raise ValueError("Expected exactly two inputs")

    for input_ in inputs:
        validate_test_session_input(input_)

    run_aliases = {input_.run_alias for input_ in inputs}
    if run_aliases != {"EXPERIMENT", "BASELINE"}:
        raise ValueError("Expected one input for 'EXPERIMENT' and one for 'BASELINE' in `run_alias`")
