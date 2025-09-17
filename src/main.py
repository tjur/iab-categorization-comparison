import os
from categories import (
    Embedder,
    get_llm_client,
    get_matching_categories_classification_model,
    get_matching_categories_hybrid_sbert_llm,
    get_matching_categories_llm,
)
from categories_data import CATEGORY_NAMES
from test_data import TEST_DATA


if __name__ == "__main__":
    embedder = Embedder(model_name="all-mpnet-base-v2")
    with (
        get_llm_client(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL", None),
        ) as openai_client,
        get_llm_client(
            api_key=os.getenv("LLAMA_API_KEY", ""),
            base_url=os.getenv("LLAMA_BASE_URL", None),
        ) as llama_client,
    ):
        for data in TEST_DATA:
            print(f"Campaign: {data['campaign_name']}")
            print(f"Description: {data['description']}")
            print(f"Keywords: {data['keywords']}\n")

            keywords = ", ".join(data["keywords"])
            categories_sbert_with_score = embedder.get_matching_categories(
                keywords, num=5, similarity_threshold=0.3
            )
            categories_sbert = [category for category, _ in categories_sbert_with_score]
            print(f"SBERT categories:\n{categories_sbert}\n")

            # model:
            # https://huggingface.co/PavanDeepak/text-classification-model-iab-categories-mixed-bert-base-uncased
            categories_mixed_bert_with_score = get_matching_categories_classification_model(
                keywords,
                model_name="PavanDeepak/text-classification-model-iab-categories-mixed-bert-base-uncased",
                num=5,
            )
            categories_mixed_bert = [
                category for category, _ in categories_mixed_bert_with_score
            ]
            print(f"Mixed BERT categories:\n{categories_mixed_bert}\n")

            # model:
            # https://huggingface.co/Mozilla/content-multilabel-iab-classifier
            categories_multilabel_classifier_with_score = (
                get_matching_categories_classification_model(
                    keywords,
                    model_name="Mozilla/content-multilabel-iab-classifier",
                    num=5,
                )
            )
            categories_multilabel_classifier = [
                category for category, _ in categories_multilabel_classifier_with_score
            ]
            print(
                f"Multi-label IAB classifier categories:\n{categories_multilabel_classifier}\n"
            )

            llama_model_name = os.getenv("LLAMA_MODEL_NAME", "")
            categories_llama = get_matching_categories_llm(
                keywords,
                llama_client,
                llama_model_name,
                CATEGORY_NAMES,
            )
            print(f"LLM categories (Llama, model: Llama-3.1-8B): {categories_llama}\n")

            openai_model_name = os.getenv("OPENAI_MODEL_NAME", "")
            categories_openai = get_matching_categories_llm(
                keywords,
                openai_client,
                openai_model_name,
                CATEGORY_NAMES,
            )
            print(
                f"LLM categories (OpenAI, model: {openai_model_name}):\n"
                f"{categories_openai}\n"
            )

            categories_sbert_llama = get_matching_categories_hybrid_sbert_llm(
                keywords,
                embedder,
                llama_client,
                llama_model_name,
                sbert_num=20,
                similarity_threshold=0.2,
            )
            print(
                f"Hybrid, SBERT + LLM categories (Llama, model: Llama-3.1-8B):\n"
                f"{categories_sbert_llama}\n"
            )

            categories_sbert_openai = get_matching_categories_hybrid_sbert_llm(
                keywords,
                embedder,
                openai_client,
                openai_model_name,
                sbert_num=20,
                similarity_threshold=0.2,
            )
            print(
                f"Hybrid, SBERT + LLM categories (OpenAI, model:{openai_model_name}):\n"
                f"{categories_sbert_openai}\n"
            )

            print("=" * 100)
