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
    frame_dir: str = "frames",
    output_file: str = "indexes/frame_embeddings.npy"
):

    embeddings = []

    frame_names = []

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

        frame_names.append(
            file
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

    return {

        "embeddings_generated":
            len(embeddings),

        "embedding_dimension":
            embeddings.shape[1],

        "output_file":
            output_file
    }