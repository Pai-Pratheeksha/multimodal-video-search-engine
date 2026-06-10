from backend.services.frame_service import (
    extract_frames
)

result = extract_frames(
    "videos/sample.mp4"
)

print(result)