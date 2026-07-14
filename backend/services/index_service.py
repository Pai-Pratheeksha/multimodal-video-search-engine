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
    video_id: str
):

    embeddings_file = (
        f"indexes/{video_id}_embeddings.npy"
    )

    embeddings = np.load(
        embeddings_file
    ).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(
        embeddings
    )

    index_file = "indexes/frame_index.faiss"

    dimension = embeddings.shape[1]

    if os.path.exists(index_file):

        index = faiss.read_index(
            index_file
        )

    else:

        base_index = faiss.IndexFlatIP(
            dimension
        )

        index = faiss.IndexIDMap2(
            base_index
        )

    os.makedirs(
        "indexes",
        exist_ok=True
    )

    with open(
        f"metadata/{video_id}.json",
        "r"
    ) as f:

        frame_metadata = json.load(f)
        

    metadata_file = "indexes/frame_metadata.json"

    if os.path.exists(metadata_file):

        try:

            with open(metadata_file, "r") as f:

                all_metadata = json.load(f)

        except json.JSONDecodeError:

            all_metadata = []

    else:

        all_metadata = []

    if all_metadata:

        next_vector_id = (

                max(

                    item["vector_id"]

                    for item in all_metadata

                )

                + 1

            )

    else:

        next_vector_id = 0

    for i, item in enumerate(frame_metadata):

        item["vector_id"] = (

            next_vector_id + i

        )

    all_metadata = [

        item

        for item in all_metadata

        if item["video_id"] != video_id

    ]

    all_metadata.extend(
        frame_metadata
    )

    ids = np.arange(

        next_vector_id,

        next_vector_id + len(embeddings),

        dtype=np.int64

    )

    index.add_with_ids(
        embeddings,
        ids
    )

    faiss.write_index(
        index,
        index_file
    )

    with open(
        metadata_file,
        "w"
    ) as f:

        json.dump(
            all_metadata,
            f,
            indent=4
        )

    metadata_path = (
        f"metadata/{video_id}.json"
    )

    if os.path.exists(
        embeddings_file
    ):

        os.remove(
            embeddings_file
        )

    if os.path.exists(
        metadata_path
    ):

        os.remove(
            metadata_path
        )


    return {

        "video_id": video_id,

        "new_vectors": len(embeddings),

        "total_vectors": index.ntotal,

        "dimension": dimension,

        "index_file": index_file

    }