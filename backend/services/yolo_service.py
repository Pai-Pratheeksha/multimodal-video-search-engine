"""
PURPOSE:
Provide object search functionality
using YOLO detections.
"""

import os
import json

def search_objects(query: str):
    if os.path.exists(
        "indexes/frame_objects.json"
    ):

        with open(
            "indexes/frame_objects.json",
            "r"
        ) as f:

            FRAME_OBJECTS = (
                json.load(f)
            )

    else:

        FRAME_OBJECTS = {}

    if os.path.exists(
        "indexes/frame_timestamps.json"
    ):

        with open(
            "indexes/frame_timestamps.json",
            "r"
        ) as f:

            FRAME_TIMESTAMPS = (
                json.load(f)
            )

    else:

        FRAME_TIMESTAMPS = {}


    if not FRAME_OBJECTS:
        return []
    
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
                    FRAME_TIMESTAMPS
                    .get(frame, {})
                    .get("timestamp", 0)

            })

    return matches[:MAX_RESULTS]