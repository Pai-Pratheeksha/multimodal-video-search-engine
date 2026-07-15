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
    "yolov8s.pt"
)


def detect_objects(
    video_id: str,
    output_file: str = "indexes/frame_objects.json"
):

    frame_dir = os.path.join(
        "frames",
        video_id
    )

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

        frame_objects[
            f"{video_id}/{file}"
        ] = detected_objects

    os.makedirs(
        "indexes",
        exist_ok=True
    )

    existing_objects = {}

    if os.path.exists(output_file):

        try:

            with open(output_file, "r") as f:

                existing_objects = json.load(f)

        except json.JSONDecodeError:

            existing_objects = {}

    existing_objects = {

        frame: objects

        for frame, objects in existing_objects.items()

        if not frame.startswith(
            f"{video_id}/"
        )

    }

    existing_objects.update(
        frame_objects
    )

    with open(output_file, "w") as f:

        json.dump(
            existing_objects,
            f,
            indent=4
        )

    return {

        "video_id": video_id,

        "frames_processed":
            len(files),

        "output_file":
            output_file
    }