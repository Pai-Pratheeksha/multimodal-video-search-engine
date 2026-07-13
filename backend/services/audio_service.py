"""
PURPOSE:
Extract audio from video using FFmpeg.

INPUT:
Video File

OUTPUT:
transcripts/audio.wav

Used by:
Video Processing Pipeline
"""

import os
import subprocess


def extract_audio(
    video_path: str,
    video_id: str
):

    output_file = (
        f"transcripts/{video_id}_audio.wav"
    )

    os.makedirs(
        "transcripts",
        exist_ok=True
    )

    command = [

        "ffmpeg",

        "-y",

        "-i",
        video_path,

        "-vn",

        "-acodec",
        "pcm_s16le",

        "-ar",
        "16000",

        "-ac",
        "1",

        output_file
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return {

        "audio_file":
            output_file
    }