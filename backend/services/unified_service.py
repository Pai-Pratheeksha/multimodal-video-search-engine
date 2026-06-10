from backend.services.clip_service import (
    search_frames
)

from backend.services.yolo_service import (
    search_objects
)

from backend.services.transcript_service import (
    search_transcript
)


def unified_search(query):

    return {

        "query":
            query,

        "clip_results":
            search_frames(query),

        "yolo_results":
            search_objects(query),

        "transcript_results":
            search_transcript(query)
    }