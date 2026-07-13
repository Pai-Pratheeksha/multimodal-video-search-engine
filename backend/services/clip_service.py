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
    selected_videos=None,
    top_k: int = 20
):
    if os.path.exists(
        "indexes/frame_index.faiss"
    ):

        index = faiss.read_index(
            "indexes/frame_index.faiss"
        )

    else:

        index = None

    FRAME_METADATA = []

    metadata_file = "indexes/frame_metadata.json"

    if os.path.exists(metadata_file):

        try:

            with open(metadata_file, "r") as f:
                FRAME_METADATA = json.load(f)

        except json.JSONDecodeError:

            FRAME_METADATA = []

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
        if idx >= len(FRAME_METADATA):
            continue

        similarity = float(
            similarities[0][rank]
        )

        if similarity < 0.22:
            continue

        frame = FRAME_METADATA[idx]

        if (
            selected_videos
            and
            frame["video_id"]
            not in selected_videos
        ):

            continue
        
        print(frame["video_id"], selected_videos)

        results.append({

            "video_id":
                frame["video_id"],

            "frame":
                frame["frame"],

            "frame_path":
                f"{frame['video_id']}/{frame['frame']}",

            "timestamp":
                frame["timestamp"],

            "similarity":
                round(
                    similarity,
                    4
                )

        })

    return results