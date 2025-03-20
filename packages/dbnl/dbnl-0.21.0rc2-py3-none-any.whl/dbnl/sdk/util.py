from collections.abc import Sequence
from typing import Optional, Union

import pandas as pd
import pyarrow as pa

from dbnl.errors import DBNLInputValidationError

from .models import (
    ColumnSchemaDict,
    ContainerColumnSchemaDict,
    ContainerScalarSchemaDict,
    PrimitiveColumnSchemaDict,
    PrimitiveScalarSchemaDict,
    Run,
    RunQuery,
    ScalarSchemaDict,
    TestSessionInput,
)


def _get_schemas_from_dataframe(
    df: pd.DataFrame,
    PrimitiveSchema: Union[type[PrimitiveColumnSchemaDict], type[PrimitiveScalarSchemaDict]],
    ContainerSchema: Union[type[ContainerColumnSchemaDict], type[ContainerScalarSchemaDict]],
) -> list[Union[ColumnSchemaDict, ScalarSchemaDict]]:
    """
    Get the column schemas for the columns in the provided dataframe.

    :param df: Dataframe from which to extract columns.
    :param PrimitiveSchema: Primitive schema class.
    :param ContainerSchema: Container schema class.
    :return: List of column schemas.
    """
    fields: list[Union[ColumnSchemaDict, ScalarSchemaDict]] = []
    schema = pa.Schema.from_pandas(df)
    for f in schema:
        if pa.types.is_integer(f.type):
            fields.append(
                PrimitiveSchema(
                    name=f.name,
                    type="int",
                )
            )
        elif pa.types.is_floating(f.type):
            fields.append(
                PrimitiveSchema(
                    name=f.name,
                    type="float",
                )
            )
        elif pa.types.is_boolean(f.type):
            fields.append(
                PrimitiveSchema(
                    name=f.name,
                    type="boolean",
                )
            )
        elif pa.types.is_string(f.type):
            fields.append(
                PrimitiveSchema(
                    name=f.name,
                    type="string",
                )
            )
        elif pa.types.is_list(f.type):
            value_type = f.type.value_type
            if not pa.types.is_string(value_type):
                raise ValueError(
                    f"Column '{f.name}' has unsupported list value type: {value_type}. Only string is supported."
                )
            fields.append(
                ContainerSchema(
                    name=f.name,
                    type="list",
                    value_type={"type": "string"},
                )
            )
        elif pa.types.is_dictionary(f.type):
            fields.append(
                PrimitiveSchema(
                    name=f.name,
                    type="category",
                )
            )
        else:
            raise ValueError(f"Field '{f.name}' has unsupported data type: {f.type}")
    return fields


def get_column_schemas_from_dataframe(df: pd.DataFrame) -> list[ColumnSchemaDict]:
    return _get_schemas_from_dataframe(df, PrimitiveColumnSchemaDict, ContainerColumnSchemaDict)


def get_scalar_schemas_from_dataframe(df: pd.DataFrame) -> list[ScalarSchemaDict]:
    return _get_schemas_from_dataframe(df, PrimitiveScalarSchemaDict, ContainerScalarSchemaDict)


def make_test_session_input(
    *,
    run: Optional[Run] = None,
    run_query: Optional[RunQuery] = None,
    run_alias: str = "EXPERIMENT",
) -> TestSessionInput:
    """
    Create a TestSessionInput object from a Run or a RunQuery. Useful for creating TestSessions right after closing a Run.

    :param run: The Run to create the TestSessionInput from
    :type run: Run
    :param run_query: The RunQuery to create the TestSessionInput from
    :type run_query: RunQuery
    :param run_alias: Alias for the Run, must be 'EXPERIMENT' or 'BASELINE', defaults to "EXPERIMENT"
    :type run_alias: str

    :raises DBNLInputValidationError: If both run and run_query are None

    :return: TestSessionInput object
    :rtype: TestSessionInput
    """
    if run_alias not in ["EXPERIMENT", "BASELINE"]:
        raise DBNLInputValidationError("run_alias must be 'EXPERIMENT' or 'BASELINE'")
    if bool(run) == bool(run_query):
        raise DBNLInputValidationError("Exactly one of `run` or `run_query` must be provided")
    if run:
        return TestSessionInput(run_alias=run_alias, run_id=run.id)
    assert run_query
    return TestSessionInput(run_alias=run_alias, run_query_id=run_query.id)


def get_default_components_dag_from_column_schemas(
    column_schemas: Sequence[ColumnSchemaDict],
) -> Optional[dict[str, list[str]]]:
    """
    Gets the unconnected components DAG from a list of column schemas. If there are no components, returns None.
    The default components dag is of the form
    {
        "component1": [],
        "component2": [],
        ...}

    :param column_schemas: list of column schemas
    :type column_schemas: list[ColumnSchemaDict]

    :return: dictionary of components DAG or None
    :rtype: dict[str, list[str]] | None
    """
    components_dag: dict[str, list[str]] = {
        c["component"]: [] for c in column_schemas if "component" in c and c["component"] is not None
    }
    if not components_dag:
        return None
    return components_dag
