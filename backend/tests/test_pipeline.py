from backend.services.video_pipeline_service import (
    process_video
)

result = process_video(
    "videos/sample.mp4"
)

print(result)