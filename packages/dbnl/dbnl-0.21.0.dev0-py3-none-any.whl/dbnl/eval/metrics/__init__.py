# ruff: noqa: F401
from __future__ import annotations

import itertools
from typing import Optional

from mlflow.metrics.genai.metric_definitions import answer_correctness as mlflow_answer_correctness
from mlflow.metrics.genai.metric_definitions import answer_similarity as mlflow_answer_similarity
from mlflow.metrics.genai.metric_definitions import faithfulness as mlflow_faithfulness
from mlflow.metrics.genai.metric_definitions import relevance as mlflow_relevance

from dbnl.eval.embedding_clients import EmbeddingClient
from dbnl.eval.llm.client import LLMClient

from .bleu import Bleu
from .context_hit import ContextHit
from .count_metrics import CharacterCount, SentenceCount, TokenCount, WordCount
from .inner_product_retrieval import InnerProductRetrieval
from .inner_product_target_prediction import InnerProductTargetPrediction
from .levenshtein import Levenshtein
from .metric import Metric
from .mlflow import (
    MLFlowGenAIFromPromptEvaluationMetric,
    MLFlowGenAIPredictionInputContextEvaluationMetric,
    MLFlowGenAIPredictionInputGTEvaluationMetric,
)
from .mrr import Mrr
from .prompts import _get_custom_answer_quality_prompt_by_name, _get_custom_answer_viability_prompt_by_name
from .rouge import Rouge, RougeMetricType, RougeScoreType
from .textstat_metrics import AutomatedReadabilityIndex, FleschKincaidGrade


def text_metrics(
    prediction: str,
    target: Optional[str] = None,
    eval_llm_client: Optional[LLMClient] = None,
    eval_embedding_client: Optional[EmbeddingClient] = None,
) -> list[Metric]:
    """
    Returns a set of metrics relevant for a generic text application

    :param prediction: prediction column name (i.e. generated text)
    :param target: target column name (i.e. expected text)
    :return: list of metrics
    """
    metrics = []
    metrics.extend([
        token_count(prediction),
        word_count(prediction),
        flesch_kincaid_grade(prediction),
        automated_readability_index(prediction),
    ])
    if target is not None:
        metrics.extend([
            bleu(prediction, target),
            levenshtein(prediction, target),
            rouge1(prediction, target),
            rouge2(prediction, target),
            rougeL(prediction, target),
            rougeLsum(prediction, target),
        ])
    if eval_llm_client is not None:
        metrics.extend([
            answer_viability_llm_text_toxicity(prediction, eval_llm_client),
            answer_viability_llm_sentiment_assessment(prediction, eval_llm_client),
            answer_viability_llm_reading_complexity(prediction, eval_llm_client),
            answer_quality_llm_grammar_accuracy(prediction, eval_llm_client),
        ])
    if target is not None and eval_embedding_client is not None:
        metrics.extend([
            inner_product_target_prediction(prediction, target, eval_embedding_client),
        ])
    if target is not None and eval_llm_client is not None:
        metrics.extend([
            quality_llm_text_similarity(prediction, target, eval_llm_client),
        ])

    return metrics


def text_monitor_metrics(columns: list[str], eval_llm_client: Optional[LLMClient] = None) -> list[Metric]:
    metrics = []
    """
    Returns a set of metrics suitable for monitoring generic text fields (no ground truth)

    :param columns: the column names in the dataframe of text fields to create monitor metrics
    :return: list of metrics
    """
    for col in columns:
        metrics += text_metrics(prediction=col, eval_llm_client=eval_llm_client)

    return metrics


def summarization_metrics(
    prediction: str,
    target: Optional[str] = None,
    eval_embedding_client: Optional[EmbeddingClient] = None,
) -> list[Metric]:
    """
    Returns a set of metrics relevant for a summarization task.

    :param prediction: prediction column name (i.e. generated summary)
    :param target: target column name (i.e. expected summary)
    :return: list of metrics
    """
    metrics = []
    metrics += count_metrics(prediction)
    metrics += non_llm_non_ground_truth_metrics(prediction)
    if target is not None:
        metrics += ground_truth_non_llm_answer_metrics(prediction, target)
        metrics += rouge_metrics(prediction, target)
    if target is not None and eval_embedding_client is not None:
        metrics.append(inner_product_target_prediction(prediction, target, eval_embedding_client))
    return metrics


def question_and_answer_metrics(
    prediction: str,
    target: Optional[str] = None,
    input: Optional[str] = None,
    context: Optional[str] = None,
    ground_truth_document_id: Optional[str] = None,
    retrieved_document_ids: Optional[str] = None,
    ground_truth_document_text: Optional[str] = None,
    top_retrieved_document_text: Optional[str] = None,
    eval_llm_client: Optional[LLMClient] = None,
    eval_embedding_client: Optional[EmbeddingClient] = None,
) -> list[Metric]:
    """
    Returns a set of metrics relevant for a question and answer task.

    :param prediction: prediction column name (i.e. generated answer)
    :param target: target column name (i.e. expected answer)
    :param input: input column name (i.e. question)
    :param context: context column name (i.e. document or set of documents retrieved)
    :param ground_truth_document_id: ground_truth_document_id containing the information in the target
    :param retrieved_document_ids: retrieved_document_ids containing the full context
    :param ground_truth_document_text: text containing the information in the target (ideal is for this to be the top retrieved document)
    :param top_retrieved_document_text: text of the top retrieved document
    :param eval_llm_client: eval_llm_client
    :param eval_embedding_client: eval_embedding_client
    :return: list of metrics
    """
    metrics = []
    metrics += text_metrics(prediction, target, eval_llm_client, eval_embedding_client)
    if ground_truth_document_id is not None and retrieved_document_ids is not None:
        metrics.extend([
            mrr(ground_truth_document_id, retrieved_document_ids),
            context_hit(ground_truth_document_id, retrieved_document_ids),
        ])
    if input is not None and eval_llm_client is not None:
        metrics.extend([
            answer_quality_llm_completeness(input, prediction, eval_llm_client),
        ])
    if input is not None and context is not None and eval_llm_client is not None:
        metrics.extend([
            answer_quality_llm_accuracy(input, context, prediction, eval_llm_client),
            answer_quality_llm_faithfulness(input, context, prediction, eval_llm_client),
        ])
    if input is not None and target is not None and eval_llm_client is not None:
        metrics.extend([
            answer_quality_llm_answer_similarity(input, prediction, target, eval_llm_client),
        ])

    return metrics


def question_and_answer_metrics_extended(
    prediction: str,
    target: Optional[str] = None,
    input: Optional[str] = None,
    context: Optional[str] = None,
    ground_truth_document_id: Optional[str] = None,
    retrieved_document_ids: Optional[str] = None,
    ground_truth_document_text: Optional[str] = None,
    top_retrieved_document_text: Optional[str] = None,
    eval_llm_client: Optional[LLMClient] = None,
    eval_embedding_client: Optional[EmbeddingClient] = None,
) -> list[Metric]:
    """
    Returns a set of all metrics relevant for a question and answer task.

    :param prediction: prediction column name (i.e. generated answer)
    :param target: target column name (i.e. expected answer)
    :param input: input column name (i.e. question)
    :param context: context column name (i.e. document or set of documents retrieved)
    :param ground_truth_document_id: ground_truth_document_id containing the information in the target
    :param retrieved_document_ids: retrieved_document_ids containing the full context
    :param ground_truth_document_text: text containing the information in the target (ideal is for this to be the top retrieved document)
    :param top_retrieved_document_text: text of the top retrieved document
    :param eval_llm_client: eval_llm_client
    :param eval_embedding_client: eval_embedding_client
    :return: list of metrics
    """

    metrics = []
    metrics += count_metrics(prediction)
    metrics += non_llm_non_ground_truth_metrics(prediction)
    if target is not None:
        metrics += ground_truth_non_llm_answer_metrics(prediction, target)
    if ground_truth_document_id is not None and retrieved_document_ids is not None:
        metrics += ground_truth_non_llm_retrieval_metrics(ground_truth_document_id, retrieved_document_ids)

    if eval_embedding_client is not None:
        if ground_truth_document_text is not None and top_retrieved_document_text is not None:
            metrics.append(
                inner_product_retrieval(
                    ground_truth_document_text,
                    top_retrieved_document_text,
                    eval_embedding_client,
                )
            )
        if target is not None:
            metrics.append(inner_product_target_prediction(prediction, target, eval_embedding_client))

    if eval_llm_client is not None:
        metrics += answer_viability_llm_metrics(prediction, eval_llm_client)
        metrics += answer_quality_llm_metrics(input, prediction, context, target, eval_llm_client)
    return metrics


def answer_quality_llm_metrics(
    input: Optional[str],
    prediction: str,
    context: Optional[str],
    target: Optional[str],
    eval_llm_client: LLMClient,
) -> list[Metric]:
    """
    Returns a set of metrics which evaluate the quality of the generated answer. This does not include metrics that require a ground truth.

    :param input: input column name (i.e. question)
    :param prediction: prediction column name (i.e. generated answer)
    :param context: context column name (i.e. document or set of documents retrieved)
    :param eval_llm_client: eval_llm_client
    :return: list of metrics
    """
    metrics = [
        answer_quality_llm_commital(prediction, eval_llm_client),
        answer_quality_llm_coherence(prediction, eval_llm_client),
        answer_quality_llm_grammar_accuracy(prediction, eval_llm_client),
        answer_quality_llm_originality(prediction, eval_llm_client),
    ]

    if input is not None:
        metrics.append(answer_quality_llm_completeness(input, prediction, eval_llm_client))

    if input is not None and context is not None:
        metrics.extend([
            answer_quality_llm_contextual_relevance(input, context, eval_llm_client),
            answer_quality_llm_faithfulness(input, context, prediction, eval_llm_client),
            answer_quality_llm_relevance(input, context, prediction, eval_llm_client),
            answer_quality_llm_accuracy(input, context, prediction, eval_llm_client),
        ])

    if input is not None and target is not None:
        metrics.extend([
            answer_quality_llm_answer_similarity(input, prediction, target, eval_llm_client),
            answer_quality_llm_answer_correctness(input, prediction, target, eval_llm_client),
        ])

    return metrics


def answer_viability_llm_metrics(prediction: str, eval_llm_client: LLMClient) -> list[Metric]:
    """
    Returns a list of metrics relevant for a question and answer task.

    :param prediction: prediction column name (i.e. generated answer)
    :param eval_llm_client: eval_llm_client
    :return: list of metrics
    """
    answer_viability_funcs = [
        answer_viability_llm_text_fluency,
        answer_viability_llm_text_toxicity,
        answer_viability_llm_sentiment_assessment,
        answer_viability_llm_reading_complexity,
    ]
    metrics = []
    for answer_viability_func in answer_viability_funcs:
        metrics.append(answer_viability_func(prediction, eval_llm_client))
    return metrics


def ground_truth_non_llm_answer_metrics(prediction: str, target: str) -> list[Metric]:
    """
    Returns a set of metrics relevant for a question and answer task.

    :param prediction: prediction column name (i.e. generated answer)
    :param target: target column name (i.e. expected answer)
    :return: list of metrics
    """
    metrics = [
        bleu(prediction, target),
        levenshtein(prediction, target),
    ]
    metrics += rouge_metrics(prediction, target)
    return metrics


def ground_truth_non_llm_retrieval_metrics(ground_truth_document_id: str, retrieved_document_ids: str) -> list[Metric]:
    """
    Returns a set of metrics relevant for a question and answer task.

    :param ground_truth_document_id: ground_truth_document_id column name
    :param retrieved_document_ids: retrieved_document_ids column name
    :return: list of metrics
    """
    metrics = [
        mrr(ground_truth_document_id, retrieved_document_ids),
        context_hit(ground_truth_document_id, retrieved_document_ids),
    ]
    return metrics


def rouge_metrics(prediction: str, target: str) -> list[Metric]:
    """
    Returns all rouge metrics between the `prediction` and `target` columns.

    :param prediction: prediction column name
    :param target: target column name
    :return: list of rouge metrics
    """
    rouge_funcs = [rouge1, rouge2, rougeL, rougeLsum]
    metrics = []
    for rouge_func, score_type in itertools.product(rouge_funcs, RougeScoreType):
        metrics.append(rouge_func(prediction, target, score_type=score_type))
    return metrics


def non_llm_non_ground_truth_metrics(prediction: str) -> list[Metric]:
    """
    Returns a set of metrics relevant for a question and answer task.

    :param prediction: prediction column name (i.e. generated answer)
    :return: list of metrics
    """
    metrics = [
        flesch_kincaid_grade(prediction),
        automated_readability_index(prediction),
    ]
    return metrics


def count_metrics(text_col_name: str) -> list[Metric]:
    """
    Returns a set of metrics relevant for a question and answer task.

    :param text_col_name: text column name
    :return: list of metrics
    """
    metrics = [
        character_count(text_col_name),
        sentence_count(text_col_name),
        token_count(text_col_name),
        word_count(text_col_name),
    ]
    return metrics


def quality_llm_text_similarity(prediction: str, target: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the similarty of the prediction and target text by evaluating using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_text_similarity` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: similarity metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_text_similarity")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        target=target,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_accuracy(input: str, context: str, prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the accuracy of the answer by evaluating the accuracy score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_accuracy` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param context: context column name
    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: accuracy metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_accuracy")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        input=input,
        prediction=prediction,
        context=context,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_completeness(input: str, prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the completeness of the answer by evaluating the completeness score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_completeness` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param prediction: prediction column
    :param eval_llm_client: eval_llm_client
    :return: completeness metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_completeness")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        input=input,
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_commital(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the commital of the answer by evaluating the commital score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_commital` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: commital metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_commital")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_coherence(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the coherence of the answer by evaluating the coherence score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_coherence` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: coherence metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_coherence")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_contextual_relevance(input: str, context: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the contextual relevance of the answer by evaluating the contextual relevance score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_contextual_relevance` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param context: context column name
    :param eval_llm_client: eval_llm_client
    :return: contextual relevance metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_contextual_relevance")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        input=input,
        context=context,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_grammar_accuracy(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the grammar accuracy of the answer by evaluating the grammar accuracy score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_grammar_accuracy` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: grammar accuracy metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_grammar_accuracy")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_originality(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the originality of the answer by evaluating the originality score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_originality` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: originality metric
    """
    prompt = _get_custom_answer_quality_prompt_by_name("llm_originality")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_viability_llm_text_fluency(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the text fluency of the answer by evaluating the perplexity of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_text_fluency` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: text fluency metric
    """
    prompt = _get_custom_answer_viability_prompt_by_name("llm_text_fluency")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_viability_llm_text_toxicity(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the toxicity of the answer by evaluating the toxicity score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_text_toxicity` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: toxicity metric
    """
    prompt = _get_custom_answer_viability_prompt_by_name("llm_text_toxicity")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_viability_llm_sentiment_assessment(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the sentiment of the answer by evaluating the sentiment assessment score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_sentiment_assessment` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: sentiment assessment metric
    """
    prompt = _get_custom_answer_viability_prompt_by_name("llm_sentiment_assessment")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_viability_llm_reading_complexity(prediction: str, eval_llm_client: LLMClient) -> Metric:
    """Computes the reading complexity of the answer by evaluating the reading complexity score of the answer using a language model.

    This metric is generated by an LLM using a specific specific prompt named `llm_reading_complexity` available in `dbnl.eval.metrics.prompts`.

    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: reading complexity metric
    """
    prompt = _get_custom_answer_viability_prompt_by_name("llm_reading_complexity")
    return MLFlowGenAIFromPromptEvaluationMetric(
        name=prompt["name"],
        judge_prompt=prompt["judge_prompt"],
        prediction=prediction,
        eval_llm_client=eval_llm_client,
        version=prompt["version"],
    )


def answer_quality_llm_answer_similarity(
    input: str, prediction: str, target: str, eval_llm_client: LLMClient
) -> Metric:
    """
    Returns answer similarity metric.

    This metric is generated by an LLM using a specific specific prompt named `llm_answer_similarity` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param prediction: prediction column name
    :param target: target column name
    :param eval_llm_client: eval_llm_client
    :return: answer similarity metric
    """
    return MLFlowGenAIPredictionInputGTEvaluationMetric(
        mlflow_answer_similarity(model=eval_llm_client.id()),
        eval_llm_client,
        prediction=prediction,
        input=input,
        target=target,
    )


def answer_quality_llm_answer_correctness(
    input: str, prediction: str, target: str, eval_llm_client: LLMClient
) -> Metric:
    """
    Returns answer correctness metric.

    This metric is generated by an LLM using a specific specific prompt named `llm_answer_correctness` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param prediction: prediction column name
    :param target: target column name
    :param eval_llm_client: eval_llm_client
    :return: answer correctness metric
    """
    return MLFlowGenAIPredictionInputGTEvaluationMetric(
        mlflow_answer_correctness(model=eval_llm_client.id()),
        eval_llm_client,
        prediction,
        input,
        target,
    )


def answer_quality_llm_relevance(input: str, context: str, prediction: str, eval_llm_client: LLMClient) -> Metric:
    """
    Returns relevance metric with context.

    This metric is generated by an LLM using a specific specific prompt named `llm_relevance` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param context: context column name
    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: answer relevance metric with context
    """
    return MLFlowGenAIPredictionInputContextEvaluationMetric(
        mlflow_relevance(model=eval_llm_client.id()),
        eval_llm_client,
        prediction=prediction,
        input=input,
        context=context,
    )


def answer_quality_llm_faithfulness(input: str, context: str, prediction: str, eval_llm_client: LLMClient) -> Metric:
    """
    Returns faithfulness metric.

    This metric is generated by an LLM using a specific specific prompt named `llm_faithfulness` available in `dbnl.eval.metrics.prompts`.

    :param input: input column name
    :param context: context column name
    :param prediction: prediction column name
    :param eval_llm_client: eval_llm_client
    :return: faithfulness metric
    """
    return MLFlowGenAIPredictionInputContextEvaluationMetric(
        mlflow_faithfulness(model=eval_llm_client.id()),
        eval_llm_client,
        prediction=prediction,
        input=input,
        context=context,
    )


def bleu(prediction: str, target: str) -> Metric:
    """
    Returns the bleu metric between the `prediction` and `target` columns.

    The BLEU score is a metric for evaluating a generated sentence to a reference sentence. The BLEU score is a number between 0 and 1, where 1 means that the generated sentence is identical to the reference sentence.

    :param prediction: prediction column name
    :param target: target column name
    :return: bleu metric
    """
    return Bleu(prediction, target)


def levenshtein(prediction: str, target: str) -> Metric:
    """
    Returns the levenshtein metric between the `prediction` and `target` columns.

    The Levenshtein distance is a metric for evaluating the similarity between two strings. The Levenshtein distance is an integer value, where 0 means that the two strings are identical, and a higher value returns the number of edits required to transform one string into the other.

    :param prediction: prediction column name
    :param target: target column name
    :return: levenshtein metric
    """
    return Levenshtein(prediction, target)


def mrr(ground_truth_document_id: str, retrieved_document_ids: str) -> Metric:
    """
    Returns the mean reciprocal rank (MRR) metric.

    This metric is used to evaluate the quality of a ranked list of documents. The MRR score is a number between 0 and 1, where 1 means that the ground truth document is ranked first in the list. The MRR score is calculated by taking the reciprocal of the rank of the first relevant document in the list.

    :param ground_truth_document_id: ground_truth_document_id column name
    :param retrieved_document_ids: retrieved_document_ids column name
    :return: mrr metric
    """
    return Mrr(ground_truth_document_id, retrieved_document_ids)


def context_hit(ground_truth_document_id: str, retrieved_document_ids: str) -> Metric:
    """
    Returns the context hit metric.

    This boolean-valued metric is used to evaluate whether the ground truth document is present in the list of retrieved documents. The context hit metric is 1 if the ground truth document is present in the list of retrieved documents, and 0 otherwise.

    :param ground_truth_document_id: ground_truth_document_id column name
    :param retrieved_document_ids: retrieved_document_ids column name
    :return: context hit metric
    """
    return ContextHit(ground_truth_document_id, retrieved_document_ids)


def inner_product_target_prediction(prediction: str, target: str, eval_embedding_client: EmbeddingClient) -> Metric:
    """
    Returns the inner product metric between the `prediction` and `target` columns.

    This metric is used to evaluate the similarity between the prediction and target columns using the inner product of their embeddings. The embedding client is used to retrieve the embeddings for the prediction and target columns. An embedding is a high-dimensional vector representation of a string of text.

    :param prediction: prediction column name
    :param target: target column name
    :param embedding_client: embedding client
    :return: inner product metric
    """
    return InnerProductTargetPrediction(prediction, target, eval_embedding_client)


def inner_product_retrieval(
    ground_truth_document_text: str,
    top_retrieved_document_text: str,
    eval_embedding_client: EmbeddingClient,
) -> Metric:
    """
    Returns the inner product metric between the `ground_truth_document_text` and `top_retrieved_document_text` columns.

    This metric is used to evaluate the similarity between the ground truth document and the top retrieved document using the inner product of their embeddings. The embedding client is used to retrieve the embeddings for the ground truth document and the top retrieved document. An embedding is a high-dimensional vector representation of a string of text.

    :param ground_truth_document_text: ground_truth_document_text column name
    :param top_retrieved_document_text: top_retrieved_document_text column name
    :param embedding_client: embedding client
    :return: inner product metric
    """
    return InnerProductRetrieval(ground_truth_document_text, top_retrieved_document_text, eval_embedding_client)


def rouge1(prediction: str, target: str, score_type: RougeScoreType = RougeScoreType.FMEASURE) -> Metric:
    """
    Returns the rouge1 metric between the `prediction` and `target` columns.

    ROUGE-1 is a recall-oriented metric that calculates the overlap of unigrams (individual words) between the predicted/generated summary and the reference summary. It measures how many single words from the reference summary appear in the predicted summary. ROUGE-1 focuses on basic word-level similarity and is used to evaluate the content coverage.

    :param prediction: prediction column name
    :param target: target column name
    :return: rouge1 metric
    """
    return Rouge(RougeMetricType.ROUGE1, prediction, target, score_type=score_type)


def rouge2(prediction: str, target: str, score_type: RougeScoreType = RougeScoreType.FMEASURE) -> Metric:
    """
    Returns the rouge2 metric between the `prediction` and `target` columns.

    ROUGE-2 is a recall-oriented metric that calculates the overlap of bigrams (pairs of words) between the predicted/generated summary and the reference summary. It measures how many pairs of words from the reference summary appear in the predicted summary. ROUGE-2 focuses on word-level similarity and is used to evaluate the content coverage.

    :param prediction: prediction column name
    :param target: target column name
    :return: rouge2 metric
    """
    return Rouge(RougeMetricType.ROUGE2, prediction, target, score_type=score_type)


def rougeL(prediction: str, target: str, score_type: RougeScoreType = RougeScoreType.FMEASURE) -> Metric:
    """
    Returns the rougeL metric between the `prediction` and `target` columns.

    ROUGE-L is a recall-oriented metric based on the Longest Common Subsequence (LCS) between the reference and generated summaries. It measures how well the generated summary captures the longest sequences of words that appear in the same order in the reference summary. This metric accounts for sentence-level structure and coherence.

    :param prediction: prediction column name
    :param target: target column name
    :return: rougeL metric
    """
    return Rouge(RougeMetricType.ROUGEL, prediction, target, score_type=score_type)


def rougeLsum(prediction: str, target: str, score_type: RougeScoreType = RougeScoreType.FMEASURE) -> Metric:
    """
    Returns the rougeLsum metric between the `prediction` and `target` columns.

    ROUGE-LSum is a variant of ROUGE-L that applies the Longest Common Subsequence (LCS) at the sentence level for summarization tasks. It evaluates how well the generated summary captures the overall sentence structure and important elements of the reference summary by computing the LCS for each sentence in the document.

    :param prediction: prediction column name
    :param target: target column name
    :return: rougeLsum metric
    """
    return Rouge(RougeMetricType.ROUGELSUM, prediction, target, score_type=score_type)


def flesch_kincaid_grade(text_col_name: str) -> Metric:
    """
    Returns the Flesch-Kincaid Grade metric for the `text_col_name` column.

    Calculates the Flesch-Kincaid Grade Level for a given text. The Flesch-Kincaid Grade Level is a readability metric that estimates the U.S. school grade level required to understand the text. It is based on the average number of syllables per word and words per sentence.

    :param text_col_name: text column name
    :return: flesch_kincaid_grade metric
    """
    return FleschKincaidGrade(text_col_name)


def automated_readability_index(text_col_name: str) -> Metric:
    """
    Returns the Automated Readability Index metric for the `text_col_name` column.

    Calculates the Automated Readability Index (ARI) for a given text. ARI is a readability metric that estimates the U.S. school grade level necessary to understand the text, based on the number of characters per word and words per sentence.

    :param text_col_name: text column name
    :return: automated_readability_index metric
    """
    return AutomatedReadabilityIndex(text_col_name)


def character_count(text_col_name: str) -> Metric:
    """
    Returns the character count metric for the `text_col_name` column.

    :param text_col_name: text column name
    :return: character_count metric
    """
    return CharacterCount(text_col_name)


def sentence_count(text_col_name: str) -> Metric:
    """
    Returns the sentence count metric for the `text_col_name` column.

    :param text_col_name: text column name
    :return: sentence_count metric
    """
    return SentenceCount(text_col_name)


def token_count(text_col_name: str) -> Metric:
    """
    Returns the token count metric for the `text_col_name` column.

    A token is a sequence of characters that represents a single unit of meaning, such as a word or punctuation mark. The token count metric calculates the total number of tokens in the text. Different languages may have different tokenization rules. This function is implemented using the `spaCy` library.

    :param text_col_name: text column name
    :return: token_count metric
    """
    return TokenCount(text_col_name)


def word_count(text_col_name: str) -> Metric:
    """
    Returns the word count metric for the `text_col_name` column.

    :param text_col_name: text column name
    :return: word_count metric
    """
    return WordCount(text_col_name)


__all__ = (
    "Metric",
    "RougeScoreType",
    "summarization_metrics",
    "question_and_answer_metrics",
    "question_and_answer_metrics_extended",
    "answer_quality_llm_metrics",
    "answer_viability_llm_metrics",
    "ground_truth_non_llm_answer_metrics",
    "ground_truth_non_llm_retrieval_metrics",
    "rouge_metrics",
    "non_llm_non_ground_truth_metrics",
    "count_metrics",
    "answer_quality_llm_accuracy",
    "answer_quality_llm_completeness",
    "answer_quality_llm_commital",
    "answer_quality_llm_coherence",
    "answer_quality_llm_contextual_relevance",
    "answer_quality_llm_grammar_accuracy",
    "answer_quality_llm_originality",
    "answer_viability_llm_text_fluency",
    "answer_viability_llm_text_toxicity",
    "answer_viability_llm_sentiment_assessment",
    "answer_viability_llm_reading_complexity",
    "answer_quality_llm_answer_similarity",
    "answer_quality_llm_answer_correctness",
    "answer_quality_llm_relevance",
    "answer_quality_llm_faithfulness",
    "bleu",
    "levenshtein",
    "mrr",
    "context_hit",
    "inner_product_target_prediction",
    "inner_product_retrieval",
    "rouge1",
    "rouge2",
    "rougeL",
    "rougeLsum",
    "flesch_kincaid_grade",
    "automated_readability_index",
    "character_count",
    "sentence_count",
    "token_count",
    "word_count",
)
