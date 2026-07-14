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
    query: str,
    videos: str = ""
):
    query = query.strip()

    if len(query) < 2:

        raise HTTPException(

            status_code=400,

            detail=
            "Please enter a valid search query."
        )
    
    selected_videos = [

        video

        for video in videos.split(",")

        if video

    ]

    print("Selected videos:", selected_videos)

    return search_multimodal(
        query,
        selected_videos
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

    video_id = (
        os.path.splitext(file.filename)[0]
        .strip()
        .lower()
        .replace(" ", "_")
    )

    library_file = "indexes/video_library.json"

    video_library = []

    if os.path.exists(library_file):

        try:

            with open(library_file, "r") as f:
                video_library = json.load(f)

        except json.JSONDecodeError:

            video_library = []

    for video in video_library:

        if video["video_id"] == video_id:

            raise HTTPException(

                status_code=409,

                detail=(
                    "This video has already been indexed."
                )

            )

    result = process_video(
        video_path,
        video_id
    )

    video_library.append({

        "video_id": video_id,

        "video_name": file.filename

    })

    with open(library_file, "w") as f:

        json.dump(
            video_library,
            f,
            indent=4
        )

    return {

        "message":
            "Video processed successfully",

        "filename":
            file.filename,

        "result":
            result
    }

@app.post("/upload-batch", tags=["Video Processing"])
async def upload_batch(
    files: list[UploadFile] = File(...)
):

    library_file = "indexes/video_library.json"

    os.makedirs(
        "videos",
        exist_ok=True
    )

    video_library = []

    if os.path.exists(library_file):

        try:

            with open(library_file, "r") as f:
                video_library = json.load(f)

        except json.JSONDecodeError:

            video_library = []

    processed = []

    duplicates = []

    failed = []

    for file in files:
        if not file.filename.lower().endswith(".mp4"):

            failed.append({

                "video": file.filename,

                "reason": "Invalid file type"

            })

            continue

        video_id = (
            os.path.splitext(file.filename)[0]
            .strip()
            .lower()
            .replace(" ", "_")
        )

        if any(
            video["video_id"] == video_id
            for video in video_library
        ):

            duplicates.append(file.filename)

            continue

        video_path = os.path.join(
            "videos",
            file.filename
        )

        with open(video_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        try:

            process_video(
                video_path,
                video_id
            )

        except Exception as e:

            if os.path.exists(video_path):

                os.remove(video_path)

            failed.append({

                "video": file.filename,

                "reason": str(e)

            })

            continue

        video_library.append({

            "video_id": video_id,

            "video_name": file.filename

        })

        processed.append({

            "video_id": video_id,

            "video_name": file.filename

        })

    with open(library_file, "w") as f:

        json.dump(
            video_library,
            f,
            indent=4
        )

    if processed:

        message = (
            f"Processed {len(processed)} video(s). "
            f"Skipped {len(duplicates)} duplicate(s). "
            f"Failed {len(failed)} upload(s)."
        )

    else:

        message = (
            "No new videos were uploaded."
        )

    return {

        "message": message,

        "processed": processed,

        "duplicates": duplicates,

        "failed": failed

    }

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "Multimodal Video Search Engine"
    }

@app.get("/video-status")
def video_status():

    library_file = "indexes/video_library.json"

    if not os.path.exists(library_file):

        return {
            "video_ready": False,
            "video_name": None,
            "video_url": None
        }

    video_library = []

    if os.path.exists(library_file):

        try:

            with open(library_file, "r") as f:
                video_library = json.load(f)

        except json.JSONDecodeError:

            video_library = []
        
    if not video_library:

        return {
            "video_ready": False,
            "video_name": None,
            "video_url": None
        }

    latest_video = video_library[-1]

    return {
        "video_ready": True,
        "video_name": latest_video["video_name"],
        "video_url": f"http://127.0.0.1:8000/videos/{latest_video['video_name']}"
    }

@app.get("/videos")
def get_videos():

    library_file = "indexes/video_library.json"

    if not os.path.exists(library_file):

        return []

    try:

        with open(library_file, "r") as f:

            videos = json.load(f)

    except json.JSONDecodeError:

        return []

    return videos

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