from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd

from dbnl.sdk.models import PrimitiveColumnSchemaDict, PrimitiveTypeLiteral


class Metric(ABC):
    @abstractmethod
    def metric(self) -> str:
        """
        Returns the metric name (e.g. rouge1).
        :return: Metric name.
        """
        raise NotImplementedError()

    @abstractmethod
    def name(self) -> str:
        """
        Returns the fully qualified name of the metric (e.g. rouge1__prediction__target).

        :return: Metric name.
        """
        raise NotImplementedError()

    @abstractmethod
    def type(self) -> PrimitiveTypeLiteral:
        """
        Returns the type of the metric (e.g. float)

        :return: Metric type.
        """
        raise NotImplementedError()

    def description(self) -> Optional[str]:
        """
        Returns the description of the metric.

        :return: Description of the metric.
        """
        return None

    def greater_is_better(self) -> Optional[bool]:
        """
        If true, larger values are assumed to be directionally better than smaller once. If false,
        smaller values are assumged to be directionally better than larger one. If None, assumes
        nothing.

        :return: True if greater is better, False if smaller is better, otherwise None.
        """
        return None

    @abstractmethod
    def expression(self) -> str:
        """
        Returns the expression representing the metric (e.g. rouge1(prediction, target)).

        :return: Metric expression.
        """
        raise NotImplementedError()

    def column_schema(self) -> PrimitiveColumnSchemaDict:
        """
        Returns the column schema for the metric to be used in a run config.

        :return: _description_
        :rtype: PrimitiveColumnSchemaDict
        """
        rval = PrimitiveColumnSchemaDict(
            name=self.name(),
            type=self.type(),
        )
        description = self.description()
        if description is not None:
            rval["description"] = description
        component = self.component()
        if component is not None:
            rval["component"] = component
        greater_is_better = self.greater_is_better()
        if greater_is_better is not None:
            rval["greater_is_better"] = greater_is_better
        return rval

    @abstractmethod
    def evaluate(self, df: pd.DataFrame) -> pd.Series[Any]:
        """
        Evaluates the metric over the provided dataframe.

        :param df: Input data from which to compute metric.
        :return: Metric values.
        """
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"{self.type()}, Metric: {self.metric()}, Name: {self.name()}"

    def __repr__(self) -> str:
        return str(self)

    def component(self) -> Optional[str]:
        return None
