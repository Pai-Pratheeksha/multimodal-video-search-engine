from pydantic import BaseModel


class ClipResult(BaseModel):
    frame: str
    similarity: float


class TranscriptResult(BaseModel):
    start: float
    end: float
    text: str


class SearchResponse(BaseModel):
    query: str
    clip_results: list[ClipResult]
    yolo_results: list[str]
    transcript_results: list[TranscriptResult]