from backend.services.transcript_service import (
    search_transcript
)

results = search_transcript(
    "london"
)

print(results)