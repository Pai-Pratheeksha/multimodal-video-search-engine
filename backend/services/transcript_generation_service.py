"""
PURPOSE:
Generate transcript from audio using Whisper.

INPUT:
transcripts/audio.wav

OUTPUT:
transcripts/transcript.json

Used by:
Video Processing Pipeline
"""

import json
import os
import whisper

print("Loading Whisper Model...")

MODEL = whisper.load_model(
    "base"
)


def generate_transcript(
    video_id: str
):

    audio_file = (
        f"transcripts/{video_id}_audio.wav"
    )

    output_file = (
        f"transcripts/{video_id}.json"
    )

    result = MODEL.transcribe(
        audio_file,
        fp16=False
    )

    segments = []

    for segment in result["segments"]:

        segments.append({

            "video_id":
                video_id,

            "start":
                segment["start"],

            "end":
                segment["end"],

            "text":
                segment["text"].strip()
        })

    os.makedirs(
        "transcripts",
        exist_ok=True
    )

    with open(
        output_file,
        "w"
    ) as f:

        json.dump(
            segments,
            f,
            indent=4
        )

    return {

        "segments_generated":
            len(segments),

        "output_file":
            output_file
    }