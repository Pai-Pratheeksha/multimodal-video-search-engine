# Imports
import os
import json
import shutil
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Services
from backend.services.unified_service import (
    unified_search
)

from backend.services.video_pipeline_service import (
    process_video
)

from backend.services.fusion_service import (
    search_multimodal
)

# Create App
app = FastAPI(
    title="Multimodal Video Search Engine",
    description="""
    Search videos using:

    - CLIP semantic search
    - YOLO object search
    - Whisper transcript search
    """,
    version="1.0.0"
)

app.mount(
    "/frames",
    StaticFiles(directory="frames"),
    name="frames"
)

app.mount(
    "/videos",
    StaticFiles(directory="videos"),
    name="videos"
)

# Add Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def root():

    return {
        "message": "API Running"
    }


@app.get("/search", tags=["Search"])
def search(query: str):

    return unified_search(query)

@app.get(
    "/multimodal-search"
)
def multimodal_search(
    query: str
):

    return search_multimodal(
        query
    )

@app.post("/upload", tags=["Video Processing"])
async def upload_video(
    file: UploadFile = File(...)
):
    # Validate file type
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(
            status_code=400,
            detail="Only MP4 files are supported"
        )

    os.makedirs(
        "videos",
        exist_ok=True
    )

    video_path = os.path.join(
        "videos",
        file.filename
    )

    with open(
        video_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = process_video(
        video_path
    )

    return {

        "message":
            "Video processed successfully",

        "filename":
            file.filename,

        "result":
            result
    }

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Multimodal Video Search Engine"
    }

@app.get("/video-info")
def video_info():

    frame_count = 0
    transcript_segments = 0
    indexed_frames = 0

    if os.path.exists("frames"):

        frame_count = len([
            f for f in os.listdir("frames")
            if f.endswith(".jpg")
        ])

    if os.path.exists(
        "transcripts/transcript.json"
    ):

        with open(
            "transcripts/transcript.json",
            "r"
        ) as f:

            transcript = json.load(f)

        transcript_segments = len(
            transcript
        )

    if os.path.exists(
        "indexes/frame_names.json"
    ):

        with open(
            "indexes/frame_names.json",
            "r"
        ) as f:

            frames = json.load(f)

        indexed_frames = len(
            frames
        )

    return {

        "frames_extracted":
            frame_count,

        "indexed_frames":
            indexed_frames,

        "transcript_segments":
            transcript_segments,

        "clip_index_exists":
            os.path.exists(
                "indexes/frame_index.faiss"
            ),

        "object_metadata_exists":
            os.path.exists(
                "indexes/frame_objects.json"
            ),

        "transcript_exists":
            os.path.exists(
                "transcripts/transcript.json"
            )
    }