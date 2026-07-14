''' delete video which is already processed(indexed) and stored in the video library '''

import os
import json
import shutil
import faiss
import numpy as np

def delete_video(video_id: str):

    library_file = "indexes/video_library.json"

    if not os.path.exists(library_file):

        return {
            "success": False,
            "message": "Video library not found."
        }

    with open(library_file, "r") as f:

        video_library = json.load(f)

    video = next(

        (

            item

            for item in video_library

            if item["video_id"] == video_id

        ),

        None

    )

    if video is None:

        return {

            "success": False,

            "message": "Video not found."

        }
    
    video_path = os.path.join(

        "videos",

        video["video_name"]

    )

    if os.path.exists(video_path):

        os.remove(video_path)

    frame_dir = os.path.join(

        "frames",

        video_id

    )

    if os.path.exists(frame_dir):

        shutil.rmtree(frame_dir)

    transcript = os.path.join(

        "transcripts",

        f"{video_id}.json"

    )

    if os.path.exists(transcript):

        os.remove(transcript)

    audio_file = os.path.join(
        "transcripts",
        f"{video_id}.wav"
    )

    if os.path.exists(audio_file):

        os.remove(audio_file)

    video_library = [

        item

        for item in video_library

        if item["video_id"] != video_id

    ]

    with open(library_file, "w") as f:

        json.dump(

            video_library,

            f,

            indent=4

        )

    metadata_file = "indexes/frame_metadata.json"

    if os.path.exists(metadata_file):

        with open(metadata_file, "r") as f:

            frame_metadata = json.load(f)

    else:

        frame_metadata = []

    vector_ids = [

        item["vector_id"]

        for item in frame_metadata

        if item["video_id"] == video_id

    ]

    print("Deleting vector IDs:", vector_ids)

    frame_metadata = [

        item

        for item in frame_metadata

        if item["video_id"] != video_id

    ]

    with open(metadata_file, "w") as f:

        json.dump(

            frame_metadata,

            f,

            indent=4

        )

    objects_file = "indexes/frame_objects.json"

    filtered = {

        frame: objects

        for frame, objects in json.load(open(objects_file, "r")).items()

        if not frame.startswith(f"{video_id}/")

    }

    with open(objects_file, "w") as f:

        json.dump(

            filtered,

            f,

            indent=4

        )

    index_file = "indexes/frame_index.faiss"

    if os.path.exists(index_file):

        index = faiss.read_index(index_file)

    else:

        index = None

    print(index.ntotal)

    if index is not None and len(vector_ids) > 0:

        ids = np.array(
            vector_ids,
            dtype=np.int64
        )

        index.remove_ids(ids)

        faiss.write_index(
            index,
            index_file
        )
    print(index.ntotal)

    return {

        "success": True,

        "message": "Video deleted successfully."

    }