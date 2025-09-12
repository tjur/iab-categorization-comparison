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

Following solutions were

### Test data
