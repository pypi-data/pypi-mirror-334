from __future__ import annotations

import re
from typing import Any

from .mlflow import DEFAULT_METRIC_VERSION

CUSTOM_ANSWER_QUALITY_PROMPTS = [
    {
        "name": "llm_text_similarity",
        "version": "v0",
        "judge_prompt": """Given the generated text : {prediction}, score the semantic similarity to the reference text : {target}. Rate the semantic similarity from 1 (completely different meaning and facts between the generated and reference texts) to 5 (nearly the exact same semantic meaning and facts present in the generated and reference texts)."

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_accuracy",
        "version": "v0",
        "judge_prompt": """Given the context {context} and the question {input}, assess the factual accuracy of the generated answer {prediction}. Rate its correctness from 1 (completely inaccurate) to 5 (highly accurate).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_completeness",
        "version": "v0",
        "judge_prompt": """To what extent does the generated answer {prediction} fully address and cover all aspects of the question {input}? Rate its completeness from 1 (completely incomplete) to 5 (fully comprehensive).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_commital",
        "version": "v0",
        "judge_prompt": """Evaluate the level of commitment and decisiveness in the generated answer {prediction}. Does the answer provide a clear and definitive response, or is it vague and non-committal? Rate from 1 (very vague) to 5 (very decisive)

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_coherence",
        "version": "v0",
        "judge_prompt": """Assess the logical flow and coherence of the generated answer {prediction}. Consider if the answer is well-organized and makes logical sense throughout. Rate from 1 (disjointed and incoherent) to 5 (logically consistent and coherent)

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_contextual_relevance",
        "version": "v0",
        "judge_prompt": """How relevant is the provided context {context} in relation to the question {input}? Evaluate if the context helps in understanding and effectively answering the question. Rate on a scale from 1 (not relevant at all) to 5 (highly relevant).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_grammar_accuracy",
        "version": "v0",
        "judge_prompt": """Rate the grammatical accuracy of the generated answer : {prediction}. Consider if the answer is free from grammatical errors and is well-written. Rate from 1 (many grammatical errors) to 5 (perfect grammar).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_originality",
        "version": "v0",
        "judge_prompt": """Assess the originality and creativity of the generated answer {prediction}. Consider if the answer provides unique insights or ideas. Rate from 1 (not original, very generic) to 5 (highly original and creative).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
]

CUSTOM_ANSWER_VIABILITY_PROMPTS = [
    {
        "name": "llm_text_fluency",
        "version": "v0",
        "judge_prompt": """Evaluate the fluency and ease of reading of the generated answer {prediction}. Consider if the answer flows smoothly and is easy to read. Rate from 1 (very difficult to read) to 5 (very easy to read).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_text_toxicity",
        "version": "v0",
        "judge_prompt": """Assess the level of toxicity in the generated answer {prediction}. Consider if the answer contains offensive or harmful language. Rate from 1 (highly toxic and offensive) to 5 (completely inoffensive).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_sentiment_assessment",
        "version": "v0",
        "judge_prompt": """Evaluate the sentiment conveyed in the generated answer {prediction}. Consider if the answer has a positive, neutral, or negative tone. Rate from 1 (very negative) to 5 (very positive).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
    {
        "name": "llm_reading_complexity",
        "version": "v0",
        "judge_prompt": """How complex is the generated answer {prediction} to read and understand? Consider if the answer is written in a simple and understandable manner. Rate from 1 (very complex and hard to understand) to 5 (very simple and easy to understand).

        Example output, make certain that 'score:' and 'justification:' text is present in output:
        score: 4
        justification: XYZ""",
    },
]


def _extract_strings_within_braces(input_string: str) -> list[str]:
    """
    Returns:
        list: A list of strings that are enclosed within '{' and '}'.
    """
    pattern = r"\{([^}]*)\}"
    matches = re.findall(pattern, input_string)
    return matches


def _add_all_fields_to_prompts(prompts: list[dict[str, Any]]) -> None:
    for prompt in prompts:
        prompt["all_fields"] = _extract_strings_within_braces(prompt["judge_prompt"])


_add_all_fields_to_prompts(CUSTOM_ANSWER_QUALITY_PROMPTS)
_add_all_fields_to_prompts(CUSTOM_ANSWER_VIABILITY_PROMPTS)


def _get_custom_answer_quality_prompt_by_name(name: str, version: str = DEFAULT_METRIC_VERSION) -> dict[str, Any]:
    """
    Returns the prompt by name.

    :param name: prompt name
    :param version: prompt version (optional, defaults to "v0")
    :return: prompt
    :raises ValueError: if the prompt with the specified name and version is not found
    """
    for prompt in CUSTOM_ANSWER_QUALITY_PROMPTS:
        if prompt["name"] == name and prompt["version"] == version:
            return prompt
    raise ValueError(f"Prompt with name {name} and version {version} not found.")


def _get_custom_answer_viability_prompt_by_name(name: str, version: str = DEFAULT_METRIC_VERSION) -> dict[str, Any]:
    """
    Returns the prompt by name.

    :param name: prompt name
    :param version: prompt version (optional, defaults to "v0")
    :return: prompt
    :raises ValueError: if the prompt with the specified name and version is not found
    """
    for prompt in CUSTOM_ANSWER_VIABILITY_PROMPTS:
        if prompt["name"] == name and prompt["version"] == version:
            return prompt
    raise ValueError(f"Prompt with name {name} and version {version} not found.")
