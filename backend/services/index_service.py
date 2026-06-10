"""
PURPOSE:
Create FAISS index from CLIP embeddings.

INPUT:
indexes/frame_embeddings.npy
frames/*.jpg

OUTPUT:
indexes/frame_index.faiss
indexes/frame_names.json

Used by:
Video Processing Pipeline
"""

import os
import json
import faiss
import numpy as np


def build_faiss_index(
    embeddings_file: str = "indexes/frame_embeddings.npy",
    frame_dir: str = "frames"
):

    embeddings = np.load(
        embeddings_file
    ).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(
        embeddings
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    os.makedirs(
        "indexes",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "indexes/frame_index.faiss"
    )

    frame_names = sorted([
        f for f in os.listdir(frame_dir)
        if f.endswith(".jpg")
    ])

    with open(
        "indexes/frame_names.json",
        "w"
    ) as f:

        json.dump(
            frame_names,
            f,
            indent=4
        )

    return {

        "vectors_indexed":
            index.ntotal,

        "dimension":
            dimension,

        "index_file":
            "indexes/frame_index.faiss"
    }