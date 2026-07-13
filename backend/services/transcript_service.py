"""
PURPOSE:
Provide transcript search
using Whisper output.
"""

import os
import json


def search_transcript(query: str, selected_videos=None):

    transcript_dir = "transcripts"

    if not os.path.exists(transcript_dir):
        return []

    matches = []

    MAX_RESULTS = 5

    transcript_files = [

        file

        for file in os.listdir(transcript_dir)

        if file.endswith(".json")

    ]

    for transcript_file in transcript_files:

        try:

            with open(

                os.path.join(
                    transcript_dir,
                    transcript_file
                ),

                "r"

            ) as f:

                transcript = json.load(f)

        except json.JSONDecodeError:

            continue

        for segment in transcript:

            if (

                query.lower()

                not in

                segment["text"].lower()

            ):

                continue

            if len(segment["text"]) <= 15:

                continue

            if (

                selected_videos

                and

                segment["video_id"]

                not in selected_videos

            ):

                continue
            
            print("WHISPER:", segment["video_id"])

            matches.append({

                "video_id":
                    segment["video_id"],

                "start":
                    segment["start"],

                "end":
                    segment["end"],

                "text":
                    segment["text"]

            })
    matches.sort(

        key=lambda x: (

            x["video_id"],

            x["start"]

        )

    )

    return matches[:MAX_RESULTS]