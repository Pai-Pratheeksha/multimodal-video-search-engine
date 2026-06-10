"""
PURPOSE:
Run YOLO object detection on all frames.

INPUT:
frames/*.jpg

OUTPUT:
indexes/frame_objects.json

Stores detected objects for each frame.

Example:
{
    "frame_0001.jpg": ["person", "dog"]
}
"""
import os
import json
from ultralytics import YOLO

print("Loading YOLO...")

model = YOLO("yolov8n.pt")

FRAME_DIR = "frames"

frame_objects = {}

files = sorted([
    f for f in os.listdir(FRAME_DIR)
    if f.endswith(".jpg")
])

for i, file in enumerate(files, start=1):

    image_path = os.path.join(
        FRAME_DIR,
        file
    )

    results = model(
        image_path,
        conf=0.25,
        verbose=False
    )

    detected_objects = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls)

            class_name = model.names[class_id]

            detected_objects.append(
                class_name
            )

    # Remove duplicates
    detected_objects = list(
        set(detected_objects)
    )

    frame_objects[file] = detected_objects

    print(
        f"[{i}/{len(files)}] "
        f"{file}: "
        f"{detected_objects}"
    )

os.makedirs(
    "indexes",
    exist_ok=True
)

with open(
    "indexes/frame_objects.json",
    "w"
) as f:

    json.dump(
        frame_objects,
        f,
        indent=4
    )

print("\nObject metadata saved!")