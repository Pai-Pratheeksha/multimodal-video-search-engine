from backend.services.clip_service import (
    search_frames
)

results = search_frames(
    "person"
)

print(results)