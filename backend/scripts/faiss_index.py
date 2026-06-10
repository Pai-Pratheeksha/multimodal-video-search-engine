"""
PURPOSE:
Create FAISS index from CLIP embeddings.

INPUT:
indexes/frame_embeddings.npy

OUTPUT:
indexes/frame_index.faiss

Used for fast semantic similarity search.
"""
import numpy as np
import faiss

# Load embeddings
embeddings = np.load(
    "indexes/frame_embeddings.npy"
)

print("Embeddings shape:", embeddings.shape)

# Convert to float32
embeddings = embeddings.astype("float32")

# Create FAISS index
faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(
    embeddings.shape[1]
)

index.add(embeddings)

print("Vectors indexed:", index.ntotal)

# Save index
faiss.write_index(
    index,
    "indexes/frame_index.faiss"
)

print("FAISS index saved!")