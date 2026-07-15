"""
PURPOSE:
Generate CLIP embeddings for all extracted frames.

INPUT:
frames/*.jpg

OUTPUT:
indexes/frame_embeddings.npy

Used by:
Video Processing Pipeline
"""

import os
import numpy as np
import torch
import json

from PIL import Image

from transformers import (
    CLIPProcessor,
    CLIPModel
)

print("Loading CLIP Model...")

MODEL = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch16"
)

PROCESSOR = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch16"
)


def generate_embeddings(
    video_id: str,
    output_file: str = None
):

    if output_file is None:
         output_file = f"indexes/{video_id}_embeddings.npy"

    frame_dir = os.path.join(
        "frames",
        video_id
    )

    embeddings = []

    files = sorted([
        f for f in os.listdir(frame_dir)
        if f.endswith(".jpg")
    ])

    for file in files:

        image_path = os.path.join(
            frame_dir,
            file
        )

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = PROCESSOR(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():

            image_features = (
                MODEL.get_image_features(
                    **inputs
                )
            )

        embedding = (
            image_features
            .cpu()
            .numpy()[0]
        )

        embedding = (
            embedding /
            np.linalg.norm(
                embedding
            )
        )

        embeddings.append(
            embedding
        )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    os.makedirs(
        "indexes",
        exist_ok=True
    )

    np.save(
        output_file,
        embeddings
    )

    with open(
        f"metadata/{video_id}.json",
        "r"
    ) as f:
        metadata = json.load(f)

    for i, embedding in enumerate(embeddings):

        metadata[i]["vector_id"] = i

    with open(
        f"metadata/{video_id}.json",
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    return {

        "embeddings_generated":
            len(embeddings),

        "embedding_dimension":
            embeddings.shape[1],

        "output_file":
            output_file
    }