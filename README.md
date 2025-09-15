# iab-categorization-comparison

Comparison of approaches that can be used to find the best-matching IAB categories for ad campaign keywords.


## Requirements

* [uv](https://docs.astral.sh/uv/)
* [Python](https://www.python.org/) 3.13 (installed via `uv`)

For development:

* [pre-commit](https://pre-commit.com/)


Download required SBERT embeddings model from Hugging Face:

    ./download_hf_models.sh

Rename file `.env.example` as `.env`, adjust values and load environment variables with:

    set -a ; source .env ; set +a

To run comparison of each implemented approach on the test data and get a report:

    uv run python src/main.py

## Approaches

This section describes all solutions that were implemented and verified against test data.
The specific logic can be found in [category.py](src/categories.py) file.

### SBERT model (sentence embeddings)

Uses [sentence-transformers](https://sbert.net/) Python library with the `all-mpnet-base-v2` model
([available models](https://sbert.net/docs/sentence_transformer/pretrained_models.html#original-models))
to create vector representations (embeddings) for both IAB categories and campaign keywords. Cosine similarity is then used to identify which categories most closely align with the keywords.

### Mixed BERT model

Employs a pre-trained BERT-based
[classification model](https://huggingface.co/PavanDeepak/text-classification-model-iab-categories-mixed-bert-base-uncased),
specifically fine-tuned for IAB category classification. Uses Hugging Face's text classification pipeline for direct category prediction.

At the moment of writing, it was the most popular model related to IAB classification
available on Hugging Face.

### Multi-label IAB classifier

Utilizes Mozilla's
[multi-label IAB classifier](https://huggingface.co/Mozilla/content-multilabel-iab-classifier)
designed for content categorization.

At the moment of writing, it was the second most popular model related to IAB classification
available on Hugging Face.

### LLM

Leverages Large Language Models with structured prompts to classify campaign keywords into IAB categories. Uses chain-of-thought reasoning and JSON-formatted responses.

Both OpenAI `GPT-5 nano` and Meta `Llama 3.1 8B` models were tested, to compare results between
closed and open-source LLMs. `GPT-5 nano` was chosen since it should be good enough
for simple, well-defined tasks like classification, as described by model provider.

### Hybrid solution (LLM with SBERT prefiltering)

Combines the efficiency of SBERT embeddings with the reasoning capabilities of LLMs.
In the first step [SBERT approach](#sbert-model-sentence-embeddings) is used to identify 20 candidate categories,
then LLM reasoning is applied to select and rank the most relevant ones from the reduced set,
improving accuracy.

## Test data

Test data was generated with OpenAI gpt-4.1 model.
It consists of sample campaigns, with descriptions and keywords, and
is available in [test_data.py](src/test_data.py) file along with an LLM prompt
used for its generation.

## Results
