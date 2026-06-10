"""
PURPOSE:
Unified Multimodal Video Search Engine.

Combines:

1. CLIP + FAISS
   -> Semantic Visual Search

2. YOLO
   -> Object Search

3. Whisper
   -> Speech Search

INPUT:
Single user query

Example:
person
road
machine learning

PROCESS:

User Query
      ↓

 ┌──────────────┐
 │ CLIP + FAISS │
 └──────────────┘
      ↓
 Semantic Matches

 ┌──────────────┐
 │     YOLO     │
 └──────────────┘
      ↓
 Object Matches

 ┌──────────────┐
 │   Whisper    │
 └──────────────┘
      ↓
 Transcript Matches

OUTPUT:
Combined search results from all modalities.

Used as the main search interface before
building FastAPI and React frontend.
"""
import json
import faiss
import torch
import numpy as np

from transformers import (
    CLIPProcessor,
    CLIPModel
)

print("Loading CLIP...")

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

# Load FAISS index
index = faiss.read_index(
    "indexes/frame_index.faiss"
)

# Load frame names
with open(
    "indexes/frame_names.json",
    "r"
) as f:
    frame_names = json.load(f)

# Load YOLO detections
with open(
    "indexes/frame_objects.json",
    "r"
) as f:
    frame_objects = json.load(f)

# Load transcript
with open(
    "transcripts/transcript.json",
    "r"
) as f:
    transcript = json.load(f)

query = input(
    "\nEnter search query: "
).strip()

print("\n" + "=" * 50)
print("CLIP SEMANTIC SEARCH")
print("=" * 50)

# CLIP Search
inputs = processor(
    text=[query],
    return_tensors="pt",
    padding=True
)

with torch.no_grad():
    text_features = model.get_text_features(
        **inputs
    )

query_vector = (
    text_features.cpu()
    .numpy()
    .astype("float32")
)

faiss.normalize_L2(query_vector)

distances, indices = index.search(
    query_vector,
    5
)

print("\nTop Semantic Matches:\n")

for rank, idx in enumerate(indices[0]):

    similarity = distances[0][rank]

    if similarity < 0.20:
        continue

    print(
        f"{rank+1}. "
        f"{frame_names[idx]}"
        f" | Similarity: {similarity:.2%}"
    )

print("\n" + "=" * 50)
print("YOLO OBJECT SEARCH")
print("=" * 50)

found = False

for frame, objects in frame_objects.items():

    objects_lower = [
        obj.lower()
        for obj in objects
    ]

    if query.lower() in objects_lower:

        print(frame)

        found = True

if not found:
    print("No object matches found")

print("\n" + "=" * 50)
print("WHISPER TRANSCRIPT SEARCH")
print("=" * 50)

found = False

for segment in transcript:

    if query.lower() in (
        segment["text"].lower()
    ):

        print(
            f"[{segment['start']:.1f}s - "
            f"{segment['end']:.1f}s]"
        )

        print(segment["text"])
        print()

        found = True

if not found:
    print("No transcript matches found")