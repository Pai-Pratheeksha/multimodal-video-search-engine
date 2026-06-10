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
    audio_file: str = "transcripts/audio.wav",
    output_file: str = "transcripts/transcript.json"
):

    result = MODEL.transcribe(
        audio_file,
        fp16=False
    )

    segments = []

    for segment in result["segments"]:

        segments.append({

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