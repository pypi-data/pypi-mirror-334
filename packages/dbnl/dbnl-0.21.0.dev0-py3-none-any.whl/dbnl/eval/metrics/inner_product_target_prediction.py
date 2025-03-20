from __future__ import annotations

from abc import ABC

from dbnl.eval.embedding_clients import EmbeddingClient

from .inner_product import InnerProductMetric


class InnerProductTargetPrediction(InnerProductMetric, ABC):
    def __init__(
        self,
        prediction: str,
        target: str,
        embedding_client: EmbeddingClient,
    ):
        """
        Initializes a InnerProductTargetPrediction.

        :param target_column_name: target column name
        :param prediction_column_name: prediction column name
        :param embedding_client: embedding client
        """
        super().__init__(prediction, target, embedding_client)
