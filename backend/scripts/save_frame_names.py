"""
PURPOSE:
Store frame filenames in correct order.

INPUT:
frames/*.jpg

OUTPUT:
indexes/frame_names.json

Maps FAISS result index -> frame filename.
"""
import os
import json

frames = sorted([
    f for f in os.listdir("frames")
    if f.endswith(".jpg")
])

with open(
    "indexes/frame_names.json",
    "w"
) as f:
    json.dump(frames, f)

print("Frame names saved!")