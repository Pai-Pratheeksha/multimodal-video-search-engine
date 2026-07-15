"""
PURPOSE:
Provide object search functionality
using YOLO detections.
"""

import os
import json

def search_objects(query: str, selected_videos=None):
    FRAME_OBJECTS = []

    if os.path.exists(
        "indexes/frame_objects.json"
    ):

        try:

            with open(
                "indexes/frame_objects.json",
                "r"
            ) as f:

                FRAME_OBJECTS = json.load(f)

        except json.JSONDecodeError:

            FRAME_OBJECTS = []

    if os.path.exists(
        "indexes/frame_metadata.json"
    ):

        with open(
            "indexes/frame_metadata.json",
            "r"
        ) as f:

            FRAME_METADATA = json.load(f)

    else:

        FRAME_METADATA = []

    metadata_lookup = {

        f"{item['video_id']}/{item['frame']}": item

        for item in FRAME_METADATA

    }


    if not FRAME_OBJECTS:
        return []
    
    matches = []
    MAX_RESULTS = 5

    for frame, objects in FRAME_OBJECTS.items():

        objects_lower = [
            obj.lower()
            for obj in objects
        ]

        if query.lower() not in objects_lower:
            continue
        
        metadata = metadata_lookup.get(frame)

        if not metadata:
            continue

        if (

            selected_videos

            and

            metadata["video_id"]

            not in selected_videos

        ):

            continue
        
        print("YOLO:", metadata["video_id"])

        matches.append({

            "video_id":
                metadata["video_id"],

            "frame":
                metadata["frame"],

            "frame_path":
                frame,

            "timestamp":
                metadata["timestamp"]

        })

    return matches[:MAX_RESULTS]