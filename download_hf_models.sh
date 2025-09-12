#!/bin/bash

set -e

# Download required ML models from Hugging Face
uvx --from "huggingface-hub>=0.34.4" --isolated hf download \
    "sentence-transformers/all-mpnet-base-v2" --exclude "*onnx*" "*openvino*" "*pytorch*"

uvx --from "huggingface-hub>=0.34.4" --isolated hf download \
    "Mozilla/content-multilabel-iab-classifier" --exclude "*onnx*" "*openvino*" "*pytorch*"

uvx --from "huggingface-hub>=0.34.4" --isolated hf download \
    "PavanDeepak/text-classification-model-iab-categories-mixed-bert-base-uncased" \
    --exclude "*onnx*" "*openvino*" "*pytorch*"
