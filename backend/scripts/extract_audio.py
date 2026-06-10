"""
PURPOSE:
Extract audio from video using FFmpeg.

INPUT:
videos/sample.mp4

OUTPUT:
transcripts/audio.wav

Required before Whisper transcription.
"""
import subprocess

video_path = "videos/sample.mp4"
audio_path = "transcripts/audio.wav"

subprocess.run([
    "ffmpeg",
    "-i",
    video_path,
    "-vn",
    "-acodec",
    "pcm_s16le",
    "-ar",
    "16000",
    "-ac",
    "1",
    audio_path
])

print("Audio extracted!")