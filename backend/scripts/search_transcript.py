"""
PURPOSE:
Search spoken content inside the video transcript.

INPUT:
User text query

Example:
machine learning

PROCESS:
User Query
    ↓
Transcript Search
    ↓
Matching Timestamp Segments

OUTPUT:
Start Time
End Time
Transcript Text

Example:

[12.5s - 18.2s]
Today we discuss machine learning...

Uses:
transcripts/transcript.json
"""
import json

with open(
    "transcripts/transcript.json",
    "r"
) as f:

    transcript = json.load(f)

query = input(
    "Enter phrase to search: "
).lower()

matches = []

for segment in transcript:

    if query in segment["text"].lower():

        matches.append(segment)

print("\nResults:\n")

if not matches:

    print("No matches found.")

else:

    for match in matches:

        print(
            f"[{match['start']:.1f}s - "
            f"{match['end']:.1f}s]"
        )

        print(match["text"])
        print()