"""
PURPOSE:
Provide object search functionality
using YOLO detections.
"""

import json

with open(
    "indexes/frame_objects.json",
    "r"
) as f:

    FRAME_OBJECTS = json.load(f)

with open(
    "indexes/frame_timestamps.json",
    "r"
) as f:

    FRAME_TIMESTAMPS = (
        json.load(f)
    )


def search_objects(query: str):

    matches = []
    MAX_RESULTS = 5

    for frame, objects in FRAME_OBJECTS.items():

        objects_lower = [
            obj.lower()
            for obj in objects
        ]

        if query.lower() in objects_lower:

            matches.append({
                "frame":
                    frame,

                "timestamp":
                    FRAME_TIMESTAMPS[
                        frame
                    ]["timestamp"]

            })

    return matches[:MAX_RESULTS]