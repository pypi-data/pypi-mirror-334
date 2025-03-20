from __future__ import annotations

from abc import ABC

from dbnl.eval.embedding_clients import EmbeddingClient

from .inner_product import InnerProductMetric


class InnerProductRetrieval(InnerProductMetric, ABC):
    def __init__(
        self,
        top_retrieved_document_text: str,
        ground_truth_document_text: str,
        embedding_client: EmbeddingClient,
    ):
        """
        Initializes a InnerProductTargetPrediction.

        :param target_column_name: target column name
        :param prediction_column_name: prediction column name
        :param embedding_client: embedding client
        """
        super().__init__(top_retrieved_document_text, ground_truth_document_text, embedding_client)
