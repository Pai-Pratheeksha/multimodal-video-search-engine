"""
PURPOSE:
Generate CLIP embeddings for every extracted frame.

INPUT:
frames/*.jpg

OUTPUT:
indexes/frame_embeddings.npy

Each frame becomes a 512-dimensional vector.
Used for semantic search.
"""
import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

print("Loading CLIP...")

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

FRAME_DIR = "frames"

embeddings = []

for file in sorted(os.listdir(FRAME_DIR)):

    if not file.endswith(".jpg"):
        continue

    image_path = os.path.join(FRAME_DIR, file)

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    embedding = image_features.cpu().numpy()[0]

    embeddings.append(
        (file, embedding)
    )

print(f"Generated {len(embeddings)} embeddings")

print("Embedding shape:",
      embeddings[0][1].shape)

import numpy as np

# Save embeddings
vectors = np.array(
    [emb[1] for emb in embeddings]
)

np.save(
    "indexes/frame_embeddings.npy",
    vectors
)

print("Embeddings saved!")