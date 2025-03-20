from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from dbnl.print_logging import dbnl_logger

from .metrics.metric import Metric


def evaluate(df: pd.DataFrame, metrics: Sequence[Metric], inplace: bool = False) -> pd.DataFrame:
    """
    Evaluates a set of metrics on a dataframe, returning an augmented dataframe.

    :param df: input dataframe
    :param metrics: metrics to compute
    :param inplace: whether to modify the input dataframe in place
    :return: input dataframe augmented with metrics
    """

    items = {}
    dbnl_logger.info("Evaluating metrics:")
    for m in metrics:
        # how to make info end with space and not new line
        dbnl_logger.info(m.name())
        if m.name() in df:
            raise ValueError(f"Cannot add metric {m.name()}, column already exists in dataframe.")
        items[m.name()] = m.evaluate(df)
    dbnl_logger.info("Done evaluating metrics.")

    augmented_portion_df = pd.DataFrame(items)
    augmented_portion_df.index = df.index

    if inplace:
        df[augmented_portion_df.columns] = augmented_portion_df
        return df
    else:
        return pd.concat([df, augmented_portion_df], axis=1)
