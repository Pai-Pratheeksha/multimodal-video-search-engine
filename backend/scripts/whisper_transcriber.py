"""
PURPOSE:
Convert video audio into text using OpenAI Whisper.

INPUT:
transcripts/audio.wav

OUTPUT:
transcripts/transcript.json

Each transcript segment contains:
- start time
- end time
- spoken text

Example:
[
    {
        "start": 0.0,
        "end": 4.5,
        "text": "Hello everyone"
    }
]

Used for speech-based video search.
"""
import whisper
import json
import os

print("Loading Whisper...")

model = whisper.load_model("base")

result = model.transcribe(
    "transcripts/audio.wav",
    fp16=False
)

segments = []

for segment in result["segments"]:

    segments.append({
        "start": segment["start"],
        "end": segment["end"],
        "text": segment["text"].strip()
    })

os.makedirs(
    "transcripts",
    exist_ok=True
)

with open(
    "transcripts/transcript.json",
    "w"
) as f:

    json.dump(
        segments,
        f,
        indent=4
    )

print("Transcript saved!")