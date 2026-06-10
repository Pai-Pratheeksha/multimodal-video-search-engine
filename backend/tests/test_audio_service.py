from backend.services.audio_service import (
    extract_audio
)

result = extract_audio(
    "videos/sample.mp4"
)

print(result)