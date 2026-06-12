"""
PURPOSE:
Provide semantic frame search
using CLIP + FAISS.
"""

import json
import faiss
import torch
import os

from transformers import (
    CLIPProcessor,
    CLIPModel
)

print("Loading CLIP Service...")

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch16"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch16"
)


def search_frames(
    query: str,
    top_k: int = 20
):
    if os.path.exists(
        "indexes/frame_index.faiss"
    ):

        index = faiss.read_index(
            "indexes/frame_index.faiss"
        )

        with open(
            "indexes/frame_names.json",
            "r"
        ) as f:

            FRAME_NAMES = json.load(f)

    else:

        index = None

        FRAME_NAMES = []

    if os.path.exists(
        "indexes/frame_timestamps.json"
    ):

        with open(
            "indexes/frame_timestamps.json",
            "r"
        ) as f:

            FRAME_TIMESTAMPS = (
                json.load(f)
            )

    else:

        FRAME_TIMESTAMPS = {}

    if index is None:
        return []

    inputs = processor(
        text=[query],
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():

        text_features = (
            model.get_text_features(
                **inputs
            )
        )

    query_vector = (
        text_features
        .cpu()
        .numpy()
        .astype("float32")
    )

    faiss.normalize_L2(
        query_vector
    )

    similarities, indices = (
        index.search(
            query_vector,
            top_k
        )
    )

    results = []

    for rank, idx in enumerate(
        indices[0]
    ):

        similarity = float(
            similarities[0][rank]
        )

        if similarity >= 0.22:
            frame_name = (
                FRAME_NAMES[idx]
            )

            results.append({

                "frame":
                    frame_name,

                "similarity":
                    round(
                        similarity,
                        4
                ),
                "timestamp":
                    FRAME_TIMESTAMPS[
                        frame_name
                    ]["timestamp"]
            })

    return results