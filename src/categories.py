"""Different solutions to find the best-matching IAB categories for ad campaign keywords."""

from contextlib import contextmanager
import logging
from typing import Generator
from openai import OpenAI, OpenAIError
from pydantic import BaseModel
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline, utils

from categories_data import CATEGORY_NAMES


logger = logging.getLogger(__name__)


class Embedder:
    """
    SBERT category embeddings manager.

    The model used is `all-mpnet-base-v2`, the best available sentence-transformer model.
    It's size is 420 MB. To download it, run:

    ```
    ./download_hf_models.sh
    ```

    Other available models:
    https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#original-models
    """

    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.embeddings_model = SentenceTransformer(model_name)
        self.category_embeddings = self.embeddings_model.encode(CATEGORY_NAMES)

    def get_embedding(self, text: str) -> torch.Tensor:
        """Get embedding for the text."""
        return self.embeddings_model.encode(text)

    def get_matching_categories(
        self,
        text: str,
        num: int = 1,
        similarity_threshold: float = 0.3,
    ) -> list[tuple[str, float]]:
        """
        Get IAB categories matching the text using Sentence-BERT model.
        It calculates cosine similarity between the text and each category name using SBERT embeddings.
        Returns list of tuples (category name, similarity score) sorted by similarity score in descending order.
        """
        keyword_embedding = self.get_embedding(text)
        similarities = util.cos_sim(keyword_embedding, self.category_embeddings)

        top_k_scores, top_k_indices = similarities.topk(k=min(num, len(CATEGORY_NAMES)))
        results = []
        for score, index in zip(top_k_scores[0], top_k_indices[0]):
            score = round(score.item(), 2)
            if score < similarity_threshold:
                break
            category = CATEGORY_NAMES[index]
            results.append((category, score))

        return results


@contextmanager
def get_llm_client(
    api_key: str,
    base_url: str | None = None,
) -> Generator[OpenAI, None, None]:
    """Get LLM client."""
    client = OpenAI(api_key=api_key, base_url=base_url)
    yield client
    client.close()


class MatchingCategoriesResult(BaseModel):
    """LLM response format for matching IAB categories."""

    # use chain-of-thought technique
    reasoning: str
    categories: list[str]


def get_matching_categories_llm(
    text: str,
    client: OpenAI,
    model_name: str,
    available_categories: list[str],
    limit: int = 5,
) -> list[str]:
    """
    Get matching IAB categories using LLM.

    The input should contain keywords separated by commas.

    The prompt lists all available categories, so the LLM can choose only from them.
    Otherwise it could answer with categories in different format for each response or
    categories that don't exist (depending on the LLM used).
    """

    prompt = f"""
    You're a classification expert that can classify Google Ads advertisement campaign
    keywords into the most matching IAB categories.

    <objective>
    Classify the given keywords with the most matching IAB categories among the given ones.
    </objective>

    <rules>
    - use only IAB categories from the <iab_categories> section, each is separated by comma
    - all given keywords describe the same ad campaign (its advertised product, placement, etc.)
    - you should classify keywords only with the most relevant IAB categories
    - at least one category must be chosen
    - select up to {limit} most matching categories
    - returned categories must be ordered by the relevance to the campaign keywords, starting from the most matching
    - Google Ads campaign keywords are provided in the <keywords> section, each separated by comma
    - your response must have a JSON format specified in <output_format>, do not include any other text
    </rules>

    <iab_categories>
    {", ".join(available_categories)}
    </iab_categories>

    <keywords>
    {text}
    </keywords>

    <output_format>
    {{
        "reasoning": <explanation of your reasoning, why you chose these categories>,
        "categories": <list of IAB categories that match given campaign keywords, ordered by the relevance, starting from the most matching>
    }}
    </output_format>
    """

    try:
        response = client.chat.completions.parse(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format=MatchingCategoriesResult,
        )
    except OpenAIError as err:
        logger.error(f"Error while classifying keywords with LLM: {err}")
        return []

    result = response.choices[0].message.parsed
    if result is None:
        logger.error("Error while parsing IAB categories returned by LLM")
        return []

    return result.categories[:limit]


def get_matching_categories_classification_model(
    text: str,
    model_name: str,
    num: int = 1,
) -> list[tuple[str, float]]:
    """Get matching IAB categories using ML classification model from Hugging Face."""

    utils.logging.set_verbosity_error()  # type: ignore[no-untyped-call]
    pipe = pipeline("text-classification", model=model_name, top_k=num)
    results = pipe(text)
    return [
        (result["label"], round(float(result["score"]), 2))  # type: ignore[index]
        for result in results[0]
    ]


def get_matching_categories_hybrid_sbert_llm(
    text: str,
    embedder: Embedder,
    client: OpenAI,
    model_name: str,
    sbert_num: int = 20,
    similarity_threshold: float = 0.2,
    llm_limit: int = 5,
) -> list[str]:
    """
    Get matching IAB categories using hybrid approach with SBERT and LLM.

    First, find good candidates using SBERT embeddings and then use LLM to keep only the best ones.
    """

    sbert_results = embedder.get_matching_categories(
        text, num=sbert_num, similarity_threshold=similarity_threshold
    )

    return get_matching_categories_llm(
        text,
        client,
        model_name,
        [category for category, _ in sbert_results],
        llm_limit,
    )
