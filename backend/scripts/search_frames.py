"""
PURPOSE:
Semantic video search using CLIP + FAISS.

PROCESS:
Text Query
 -> CLIP Text Embedding
 -> FAISS Search
 -> Matching Frames

INPUT:
User query

OUTPUT:
Most relevant video frames.
"""
import json
import faiss
import numpy as np
import torch

from transformers import (
    CLIPProcessor,
    CLIPModel
)

# Load CLIP
print("Loading CLIP...")

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

# Load index
index = faiss.read_index(
    "indexes/frame_index.faiss"
)

# Load frame names
with open(
    "indexes/frame_names.json",
    "r"
) as f:
    frame_names = json.load(f)

# Query
query = input("Search: ")

inputs = processor(
    text=[query],
    return_tensors="pt",
    padding=True
)

with torch.no_grad():
    text_features = model.get_text_features(**inputs)

query_vector = (
    text_features.cpu()
    .numpy()
    .astype("float32")
)

faiss.normalize_L2(query_vector)

# Search top 5
distances, indices = index.search(
    query_vector,
    5
)

print("\nTop Matches:\n")

for rank, idx in enumerate(indices[0]):
    score = distances[0][rank]

    if score < 0.2:
        continue

    print(
        f"{rank+1}.",
        frame_names[idx],
        f"(distance={distances[0][rank]:.2f})"
    )