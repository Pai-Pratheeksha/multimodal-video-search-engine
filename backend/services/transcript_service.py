"""
PURPOSE:
Provide transcript search
using Whisper output.
"""

import os
import json


def search_transcript(query: str):
    if os.path.exists(
        "transcripts/transcript.json"
    ):

        with open(
            "transcripts/transcript.json",
            "r"
        ) as f:

            TRANSCRIPT = json.load(f)

    else:

        TRANSCRIPT = []

    if not TRANSCRIPT:
        return []

    matches = []
    MAX_RESULTS = 5

    for segment in TRANSCRIPT:

        if (
            query.lower() in segment["text"].lower()
            and len(segment["text"]) > 15
        ):

            matches.append({

                "start":
                    segment["start"],

                "end":
                    segment["end"],

                "text":
                    segment["text"]
            })

    return matches[:MAX_RESULTS]