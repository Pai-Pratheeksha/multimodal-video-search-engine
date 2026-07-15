"""
PURPOSE:
Run the complete video processing pipeline.

INPUT:
Video File

OUTPUT:
Frames
Embeddings
FAISS Index
YOLO Metadata
Transcript
"""

from backend.services.frame_service import (
    extract_frames
)

from backend.services.embedding_service import (
    generate_embeddings
)

from backend.services.index_service import (
    build_faiss_index
)

from backend.services.detection_service import (
    detect_objects
)

from backend.services.audio_service import (
    extract_audio
)

from backend.services.transcript_generation_service import (
    generate_transcript
)


def process_video(
    video_path: str,
    video_id: str
):

    frame_result = extract_frames(
        video_path,
        video_id
    )

    embedding_result = (
        generate_embeddings(video_id)
    )

    index_result = (
        build_faiss_index(video_id)
    )

    detection_result = (
        detect_objects(video_id)
    )

    audio_result = (
        extract_audio(
            video_path,
            video_id
        )
    )

    transcript_result = (
        generate_transcript(video_id)
    )

    return {

        "frames":
            frame_result,

        "embeddings":
            embedding_result,

        "index":
            index_result,

        "detections":
            detection_result,

        "audio":
            audio_result,

        "transcript":
            transcript_result
    }