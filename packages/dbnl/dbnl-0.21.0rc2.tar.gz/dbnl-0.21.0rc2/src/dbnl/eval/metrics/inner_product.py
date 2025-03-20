from __future__ import annotations

import time
from abc import ABC
from typing import Literal, Optional

import numpy as np
import pandas as pd
from typing_extensions import override

from dbnl.eval.embedding_clients import EmbeddingClient

from .metric import Metric


class InnerProductMetric(Metric, ABC):
    def __init__(
        self,
        left_column_name: str,
        right_column_name: str,
        embedding_client: EmbeddingClient,
    ):
        """
        Initializes a InnerProductMetric.

        :param left_column_name: left column name
        :param right_column_name: right column name
        :param embedding_client: embedding client
        """
        self._left_column_name = left_column_name
        self._right_column_name = right_column_name
        self._embedding_client = embedding_client

    @override
    def metric(self) -> str:
        return "inner_product"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._left_column_name}__{self._right_column_name}"

    @override
    def type(self) -> Literal["float"]:
        return "float"

    @override
    def description(self) -> Optional[str]:
        return f"Inner product between the '{self._left_column_name}' and '{self._right_column_name}' embeddings using the _{self._embedding_client._embedding_model}_ model."

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._left_column_name}, {self._right_column_name})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[float]:
        if self._left_column_name not in df or self._right_column_name not in df:
            raise ValueError(f"Missing columns {self._left_column_name} or {self._right_column_name} in dataframe {df}")

        left_column = df[self._left_column_name].tolist()
        right_column = df[self._right_column_name].tolist()

        left_column_embeddings = self._embedding_client.call(left_column)
        time.sleep(5)  # avoid back to back requests
        right_column_embeddings = self._embedding_client.call(right_column)

        inner_products = []
        for left_embedding, right_embedding in zip(left_column_embeddings, right_column_embeddings):
            inner_product = np.inner(left_embedding.embedding, right_embedding.embedding)
            inner_products.append(inner_product)

        return pd.Series(inner_products, dtype="float32[pyarrow]")
