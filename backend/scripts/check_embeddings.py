"""
PURPOSE:
Verify saved CLIP embeddings.

INPUT:
indexes/frame_embeddings.npy

OUTPUT:
Displays embedding matrix shape.

Used for debugging.
"""
import numpy as np

embeddings = np.load(
    "indexes/frame_embeddings.npy"
)

print(embeddings.shape)