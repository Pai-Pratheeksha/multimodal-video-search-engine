"""
PURPOSE:
Detect objects in video frames using YOLO.

INPUT:
frames/*.jpg

OUTPUT:
indexes/frame_objects.json

Used by:
Video Processing Pipeline
"""

import os
import json

from ultralytics import YOLO

print("Loading YOLO Model...")

MODEL = YOLO(
    "yolov8n.pt"
)


def detect_objects(
    frame_dir: str = "frames",
    output_file: str = "indexes/frame_objects.json"
):

    frame_objects = {}

    files = sorted([
        f for f in os.listdir(frame_dir)
        if f.endswith(".jpg")
    ])

    for file in files:

        image_path = os.path.join(
            frame_dir,
            file
        )

        results = MODEL(
            image_path,
            conf=0.25,
            verbose=False
        )

        detected_objects = []

        for result in results:

            for box in result.boxes:

                class_id = int(
                    box.cls
                )

                class_name = (
                    MODEL.names[
                        class_id
                    ]
                )

                detected_objects.append(
                    class_name
                )

        detected_objects = list(
            set(detected_objects)
        )

        frame_objects[file] = (
            detected_objects
        )

    os.makedirs(
        "indexes",
        exist_ok=True
    )

    with open(
        output_file,
        "w"
    ) as f:

        json.dump(
            frame_objects,
            f,
            indent=4
        )

    return {

        "frames_processed":
            len(files),

        "output_file":
            output_file
    }