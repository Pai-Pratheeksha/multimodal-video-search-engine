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
    video_path: str
):

    frame_result = extract_frames(
        video_path
    )

    embedding_result = (
        generate_embeddings()
    )

    index_result = (
        build_faiss_index()
    )

    detection_result = (
        detect_objects()
    )

    audio_result = (
        extract_audio(
            video_path
        )
    )

    transcript_result = (
        generate_transcript()
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