"""
PURPOSE:
Search frames using YOLO detected objects.

INPUT:
User query (person, car, dog, etc.)

OUTPUT:
Frames containing that object and timestamp.

Uses:
indexes/frame_objects.json
"""
import json
import re

with open(
    "indexes/frame_objects.json",
    "r"
) as f:
    frame_objects = json.load(f)

query = input(
    "Enter object to search: "
).strip().lower()

matches = []

for frame, objects in frame_objects.items():

    objects_lower = [
        obj.lower()
        for obj in objects
    ]

    if query in objects_lower:

        frame_num = int(
            re.search(
                r"\d+",
                frame
            ).group()
        )

        matches.append(
            (
                frame,
                frame_num
            )
        )

print("\nSearch Results:\n")

if not matches:

    print(
        f"No frames contain '{query}'"
    )

else:

    for frame, timestamp in matches:

        print(
            f"{frame}  |  {timestamp}s"
        )