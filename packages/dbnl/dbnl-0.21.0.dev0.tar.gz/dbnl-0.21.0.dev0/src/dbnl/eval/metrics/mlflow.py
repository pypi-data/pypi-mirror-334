from __future__ import annotations

import os
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Literal, Optional

import mlflow
import pandas as pd
from mlflow.metrics import MetricValue
from mlflow.metrics.genai import make_genai_metric_from_prompt
from typing_extensions import override

from dbnl.eval.llm import AzureOpenAILLMClient, LLMClient, OpenAILLMClient
from dbnl.tqdm import configure_tqdm

from .metric import Metric

DEFAULT_METRIC_VERSION = "v0"


@contextmanager
def _set_env(**environ: str) -> Generator[None, None, None]:
    curr = os.environ.copy()
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(curr)


class MLFlowGenAIMetric(Metric, ABC):
    def __init__(
        self,
        mlflow_metric: mlflow.models.evaluation.base.EvaluationMetric,
        eval_llm_client: LLMClient,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        self._mlflow_metric = mlflow_metric
        self._eval_llm_client = eval_llm_client
        self._version = version

    def metric(self) -> str:
        return f"{self._mlflow_metric.name}_{self._version}"

    def description(self) -> str:
        return "See Distributional's metric augmentation documentation for more information."

    @override
    def greater_is_better(self) -> Optional[bool]:
        gib = self._mlflow_metric.greater_is_better
        return bool(gib) if gib is not None else None

    @property
    def version(self) -> Optional[str]:
        return self._version

    @override
    def evaluate(self, eval_df: pd.DataFrame) -> pd.Series[Any]:
        env_vars: dict[str, str] = {}
        # hack to use envvars from client
        # make sure this works with vanilla openAI client
        if isinstance(self._eval_llm_client, AzureOpenAILLMClient):
            env_vars = {
                "OPENAI_API_TYPE": "azure",
                "OPENAI_API_VERSION": self._eval_llm_client.client._api_version,
                "OPENAI_API_BASE": str(self._eval_llm_client.client.base_url).split("openai/")[0],
                "OPENAI_API_KEY": self._eval_llm_client.client.api_key,
                "OPENAI_DEPLOYMENT_NAME": self._eval_llm_client.llm_model,
            }
        elif isinstance(self._eval_llm_client, OpenAILLMClient):
            env_vars = {"OPENAI_API_KEY": self._eval_llm_client.client.api_key}
            mlflow.metrics.genai.model_utils.REQUEST_URL_CHAT = (
                str(self._eval_llm_client.client.base_url) + "chat/completions"
            )

        with _set_env(**env_vars), configure_tqdm():
            value = self.evaluate_with_client(eval_df)

        assert isinstance(value.scores, list)
        # ensure this is going to be an int
        if self.type() == "int":
            return pd.Series(data=value.scores, dtype="int32[pyarrow]")
        else:
            raise ValueError(f"Unsupported type for metric {self.metric()}: {self.type()}")

    @abstractmethod
    def evaluate_with_client(self, eval_df: pd.DataFrame) -> MetricValue: ...


class MLFlowGenAIPredictionEvaluationMetric(MLFlowGenAIMetric):
    def __init__(
        self,
        mlflow_metric: mlflow.models.evaluation.base.EvaluationMetric,
        eval_llm_client: LLMClient,
        prediction: str,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        super().__init__(mlflow_metric, eval_llm_client, version=version)
        self._prediction = prediction

    def name(self) -> str:
        return f"{self.metric()}__{self._prediction}"

    def expression(self) -> str:
        return f"{self.metric()}({self._prediction})"

    def type(self) -> Literal["int"]:
        return "int"

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        # see for docs : https://github.com/mlflow/mlflow/blob/master/mlflow/metrics/genai/genai_metric.py#L504
        # have to provide an 'empty' series for input
        value = self._mlflow_metric.eval_fn(
            eval_df[self._prediction],
            None,
            pd.Series(index=eval_df[self._prediction].index),
        )
        assert isinstance(value, MetricValue)
        return value

    @override
    def component(self) -> Optional[str]:
        return self._prediction


class MLFlowGenAIPredictionGTEvaluationMetric(MLFlowGenAIMetric):
    def __init__(
        self,
        mlflow_metric: mlflow.models.evaluation.base.EvaluationMetric,
        eval_llm_client: LLMClient,
        prediction: str,
        target: str,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        super().__init__(mlflow_metric, eval_llm_client, version=version)
        self._prediction = prediction
        self._target = target

    def name(self) -> str:
        return f"{self.metric()}__{self._prediction}_{self._target}"

    def expression(self) -> str:
        return f"{self.metric()}({self._prediction}, {self._target})"

    def type(self) -> Literal["int"]:
        return "int"

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        # see for docs : https://github.com/mlflow/mlflow/blob/master/mlflow/metrics/genai/genai_metric.py#L504
        # have to provide an 'empty' series for input
        value = self._mlflow_metric.eval_fn(
            eval_df[self._prediction], None, pd.Series(index=eval_df[self._prediction].index), eval_df[self._target]
        )
        assert isinstance(value, MetricValue)
        return value

    @override
    def component(self) -> Optional[str]:
        return f"{self._prediction}__{self._target}"


class MLFlowGenAIPredictionInputEvaluationMetric(MLFlowGenAIMetric):
    def __init__(
        self,
        mlflow_metric: mlflow.models.evaluation.base.EvaluationMetric,
        eval_llm_client: LLMClient,
        prediction: str,
        input: str,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        super().__init__(mlflow_metric, eval_llm_client, version=version)
        self._prediction = prediction
        self._input = input

    def name(self) -> str:
        return f"{self.metric()}__{self._prediction}_{self._input}"

    def expression(self) -> str:
        return f"{self.metric()}({self._prediction}, {self._input})"

    def type(self) -> Literal["int"]:
        return "int"

    def greater_is_better(self) -> Optional[bool]:
        gib = self._mlflow_metric.greater_is_better
        return bool(gib) if gib is not None else None

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        # hack to use envvars from client
        # make sure this works with vanilla openAI client

        # see for docs : https://github.com/mlflow/mlflow/blob/master/mlflow/metrics/genai/genai_metric.py#L504
        value = self._mlflow_metric.eval_fn(eval_df[self._prediction], None, eval_df[self._input])
        assert isinstance(value, MetricValue)
        return value

    @override
    def component(self) -> Optional[str]:
        return f"{self._input}__{self._prediction}"


class MLFlowGenAIPredictionInputGTEvaluationMetric(MLFlowGenAIMetric):
    def __init__(
        self,
        mlflow_metric: mlflow.models.evaluation.base.EvaluationMetric,
        eval_llm_client: LLMClient,
        prediction: str,
        input: str,
        target: str,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        super().__init__(mlflow_metric, eval_llm_client, version=version)
        self._prediction = prediction
        self._target = target
        self._input = input

    def name(self) -> str:
        return f"{self.metric()}__{self._prediction}_{self._input}_{self._target}"

    def expression(self) -> str:
        return f"{self.metric()}({self._prediction}, {self._input}, {self._target})"

    def type(self) -> Literal["int"]:
        return "int"

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        # see for docs : https://github.com/mlflow/mlflow/blob/master/mlflow/metrics/genai/genai_metric.py#L504
        value = self._mlflow_metric.eval_fn(
            eval_df[self._prediction], None, eval_df[self._input], eval_df[self._target]
        )
        assert isinstance(value, MetricValue)
        return value


class MLFlowGenAIPredictionInputContextEvaluationMetric(MLFlowGenAIMetric):
    def __init__(
        self,
        mlflow_metric: mlflow.models.evaluation.base.EvaluationMetric,
        eval_llm_client: LLMClient,
        prediction: str,
        input: str,
        context: str,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        super().__init__(mlflow_metric, eval_llm_client, version=version)
        self._prediction = prediction
        self._context = context
        self._input = input

    def name(self) -> str:
        return f"{self.metric()}__{self._prediction}__{self._input}__{self._context}"

    def expression(self) -> str:
        return f"{self.metric()}({self._prediction}, {self._input}, {self._context})"

    def type(self) -> Literal["int"]:
        return "int"

    def greater_is_better(self) -> Optional[bool]:
        gib = self._mlflow_metric.greater_is_better
        return bool(gib) if gib is not None else None

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        # see for docs : https://github.com/mlflow/mlflow/blob/master/mlflow/metrics/genai/genai_metric.py#L504
        value = self._mlflow_metric.eval_fn(
            eval_df[self._prediction], None, eval_df[self._input], eval_df[self._context]
        )
        assert isinstance(value, MetricValue)
        return value


professionalism_example_score_2 = mlflow.metrics.genai.EvaluationExample(
    input="What is MLflow?",
    output=(
        "MLflow is like your friendly neighborhood toolkit for managing your machine learning projects. It helps "
        "you track experiments, package your code and models, and collaborate with your team, making the whole ML "
        "workflow smoother. It's like your Swiss Army knife for machine learning!"
    ),
    score=2,
    justification=(
        "The response is written in a casual tone. It uses contractions, filler words such as 'like', and "
        "exclamation points, which make it sound less professional. "
    ),
)
professionalism_example_score_4 = mlflow.metrics.genai.EvaluationExample(
    input="What is MLflow?",
    output=(
        "MLflow is an open-source platform for managing the end-to-end machine learning (ML) lifecycle. It was "
        "developed by Databricks, a company that specializes in big data and machine learning solutions. MLflow is "
        "designed to address the challenges that data scientists and machine learning engineers face when "
        "developing, training, and deploying machine learning models.",
    ),
    score=4,
    justification=("The response is written in a formal language and a neutral tone. "),
)

# https://github.com/mlflow/mlflow/blob/e6c7d6e0362c92d6145d59b83534162cb0e8913f/mlflow/metrics/genai/genai_metric.py#L306
professionalism = mlflow.metrics.genai.make_genai_metric(
    name="professionalism",
    definition=(
        "Professionalism refers to the use of a formal, respectful, and appropriate style of communication that is "
        "tailored to the context and audience. It often involves avoiding overly casual language, slang, or "
        "colloquialisms, and instead using clear, concise, and respectful language."
    ),
    grading_prompt=(
        "Professionalism: If the answer is written using a professional tone, below are the details for different scores: "
        "- Score 0: Language is extremely casual, informal, and may include slang or colloquialisms. Not suitable for "
        "professional contexts."
        "- Score 1: Language is casual but generally respectful and avoids strong informality or slang. Acceptable in "
        "some informal professional settings."
        "- Score 2: Language is overall formal but still have casual words/phrases. Borderline for professional contexts."
        "- Score 3: Language is balanced and avoids extreme informality or formality. Suitable for most professional contexts. "
        "- Score 4: Language is noticeably formal, respectful, and avoids casual elements. Appropriate for formal "
        "business or academic settings. "
    ),
    examples=[professionalism_example_score_2, professionalism_example_score_4],
    aggregations=[],
    greater_is_better=True,
    # model=oai_client.id(),
)

example = mlflow.metrics.genai.EvaluationExample(
    input="What is MLflow?",
    output=(
        "MLflow is an open-source platform for managing machine "
        "learning workflows, including experiment tracking, model packaging, "
        "versioning, and deployment, simplifying the ML lifecycle."
    ),
    score=4,
    justification=(
        "The definition effectively explains what MLflow is "
        "its purpose, and its developer. It could be more concise for a 5-score.",
    ),
    grading_context={
        "targets": (
            "MLflow is an open-source platform for managing "
            "the end-to-end machine learning (ML) lifecycle. It was developed by "
            "Databricks, a company that specializes in big data and machine learning "
            "solutions. MLflow is designed to address the challenges that data "
            "scientists and machine learning engineers face when developing, training, "
            "and deploying machine learning models."
        )
    },
)

ans_corr_metric = mlflow.metrics.genai.make_genai_metric(
    name="answer_correctness_2",
    definition=(
        "Answer correctness is evaluated on the accuracy of the provided output based on "
        "the provided targets, which is the ground truth. Scores can be assigned based on "
        "the degree of semantic similarity and factual correctness of the provided output "
        "to the provided targets, where a higher score indicates higher degree of accuracy."
    ),
    grading_prompt=(
        "Answer correctness: Below are the details for different scores:"
        "- Score 1: The output is completely incorrect. It is completely different from "
        "or contradicts the provided targets."
        "- Score 2: The output demonstrates some degree of semantic similarity and "
        "includes partially correct information. However, the output still has significant "
        "discrepancies with the provided targets or inaccuracies."
        "- Score 3: The output addresses a couple of aspects of the input accurately, "
        "aligning with the provided targets. However, there are still omissions or minor "
        "inaccuracies."
        "- Score 4: The output is mostly correct. It provides mostly accurate information, "
        "but there may be one or more minor omissions or inaccuracies."
        "- Score 5: The output is correct. It demonstrates a high degree of accuracy and "
        "semantic similarity to the targets."
    ),
    examples=[example],
    # model=oai_client.id(),
    include_input=False,
    grading_context_columns=["targets"],
    parameters={"temperature": 0.0},
    greater_is_better=True,
)

# extra_metrics = [
#    MLFlowGenAIPredictionEvaluationMetric(professionalism, oai_client, prediction="prediction"),
#    MLFlowGenAIPredictionGTEvaluationMetric(ans_corr_metric, oai_client, prediction="prediction", target="ground_truth")
# ]

metric = make_genai_metric_from_prompt(
    name="ease_of_understanding",
    judge_prompt=(
        "You must evaluate the output of a bot based on how easy it is to "
        "understand its outputs."
        "Evaluate the bot's output from the perspective of a layperson."
        "The bot was provided with this input: {input} and this output: {prediction}."
    ),
    model="openai:/gpt-4",
    # parameters={"temperature": 0.0},
    greater_is_better=True,
)


class MLFlowGenAIFromPromptEvaluationMetric(MLFlowGenAIMetric):
    def __init__(
        self,
        name: str,
        judge_prompt: str,
        eval_llm_client: LLMClient,
        prediction: Optional[str] = None,
        input: Optional[str] = None,
        context: Optional[str] = None,
        target: Optional[str] = None,
        greater_is_better: Optional[bool] = None,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        metric = make_genai_metric_from_prompt(
            name=name,
            judge_prompt=judge_prompt,
            model=eval_llm_client.id(),
            parameters={"temperature": 0.0},
            greater_is_better=greater_is_better,  # type: ignore[arg-type]
        )
        super().__init__(metric, eval_llm_client, version=version)
        self._prediction = prediction
        self._context = context
        self._input = input
        self._target = target

    def name(self) -> str:
        metric = self.metric()
        args_candidates = [self._prediction, self._input, self._context, self._target]
        res = "__".join([metric] + [arg for arg in args_candidates if arg is not None])
        return res

    def expression(self) -> str:
        res = f"{self.metric()}("
        if self._prediction is not None:
            res += f"{self._prediction}"
        if self._input is not None:
            res += f", {self._input}"
        if self._target is not None:
            res += f", {self._target}"
        if self._context is not None:
            res += f", {self._context}"
        res += ")"
        return res

    def type(self) -> Literal["int"]:
        return "int"

    def greater_is_better(self) -> Optional[bool]:
        gib = self._mlflow_metric.greater_is_better
        return bool(gib) if gib is not None else None

    @override
    def component(self) -> Optional[str]:
        if self._prediction is not None:
            if self._input is not None:
                return f"{self._input}__{self._prediction}"
            return self._prediction
        return None

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        # see for docs : https://github.com/mlflow/mlflow/blob/master/mlflow/metrics/genai/genai_metric.py#L504
        kwargs = {}
        if self._prediction is not None:
            kwargs["prediction"] = eval_df[self._prediction]
        if self._input is not None:
            kwargs["input"] = eval_df[self._input]
        if self._target is not None:
            kwargs["target"] = eval_df[self._target]
        if self._context is not None:
            kwargs["context"] = eval_df[self._context]

        value = self._mlflow_metric.eval_fn(**kwargs)
        assert isinstance(value, MetricValue)
        return value
