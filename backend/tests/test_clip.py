"""
PURPOSE:
Verify CLIP installation and functionality.

Used for:
- Loading CLIP model
- Generating test image embeddings

Debug file only.
"""
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

print("Loading CLIP...")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

image = Image.open("frames/frame_0000.jpg").convert("RGB")

inputs = processor(
    images=image,
    return_tensors="pt"
)

with torch.no_grad():
    image_features = model.get_image_features(**inputs)

print(type(image_features))
print(image_features.shape)