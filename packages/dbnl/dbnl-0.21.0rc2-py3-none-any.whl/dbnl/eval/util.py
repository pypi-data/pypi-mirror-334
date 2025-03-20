from __future__ import annotations

import pandas as pd

from dbnl.sdk.models import ColumnSchemaDict
from dbnl.sdk.util import get_column_schemas_from_dataframe

from .metrics.metric import Metric


def get_column_schemas_from_dataframe_and_metrics(df: pd.DataFrame, metrics: list[Metric]) -> list[ColumnSchemaDict]:
    """
    Gets the run config column schemas for a dataframe that was augmented with a list of metrics.

    :param df: Dataframe to get column schemas from
    :param metrics: list of metrics added to the dataframe
    :return: list of columns schemas for dataframe and metrics
    """
    columns: list[ColumnSchemaDict] = []
    df_columns_by_name = {c["name"]: c for c in get_column_schemas_from_dataframe(df)}
    metrics_columns_by_name = {c["name"]: c for c in get_column_schemas_from_metrics(metrics)}
    component_names = {
        metric["component"] for metric in metrics_columns_by_name.values() if metric.get("component", None) is not None
    }
    # Check all provided metrics are in the dataframe.
    for name, _ in metrics_columns_by_name.items():
        if name not in df_columns_by_name:
            raise ValueError(f"Metric {name} was provided, but is missing from dataframe.")
    # Add columns from df, overwriting with metrics column if available.
    for name, df_column in df_columns_by_name.items():
        if name in metrics_columns_by_name:
            columns.append(metrics_columns_by_name[name])
        else:
            # link metric components to source columns
            if name in component_names and df_column.get("component", None) is None:
                df_column["component"] = name
            columns.append(df_column)
    return columns


def get_column_schemas_from_metrics(metrics: list[Metric]) -> list[ColumnSchemaDict]:
    """
    Gets the run config column schemas from a list of metrics.

    :param metrics: list of metrics to get column schemas from
    :return: list of column schemas for metrics
    """
    return [m.column_schema() for m in metrics]
