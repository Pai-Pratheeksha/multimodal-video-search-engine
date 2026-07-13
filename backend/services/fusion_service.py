"""
PURPOSE:
Fuse CLIP, YOLO and Whisper
results into unified moments.
"""

import os
import json

CLUSTER_WINDOW = 3  # seconds
TOP_K_RESULTS = 5
MIN_SCORE = 0.25
MIN_RESULTS = 2

from backend.services.clip_service import (
    search_frames
)

from backend.services.yolo_service import (
    search_objects
)

from backend.services.transcript_service import (
    search_transcript
)

def get_nearest_frame(
    video_id: str,
    timestamp: float,
    frame_metadata: list
):
    if not frame_metadata:
        return None

    nearest = None

    smallest_diff = float("inf")

    for frame in frame_metadata:

        if frame["video_id"] != video_id:
            continue

        diff = abs(
            frame["timestamp"] - timestamp
        )

        if diff < smallest_diff:

            smallest_diff = diff

            nearest = frame

    return nearest

def search_multimodal(
    query: str,
    selected_videos=None
):
    query = query.strip()

    if len(query) < 2:
        return []
    
    if os.path.exists(
        "indexes/frame_metadata.json"
    ):

        with open(
            "indexes/frame_metadata.json",
            "r"
        ) as f:

            FRAME_METADATA = json.load(f)

    else:

        FRAME_METADATA = []

    clip_results = (
        search_frames(query, selected_videos)
    )

    print("\nCLIP RESULTS")
    print(clip_results)

    yolo_results = (
        search_objects(query, selected_videos)
    )

    print("\nYOLO RESULTS")
    print(yolo_results)

    transcript_results = (
        search_transcript(query, selected_videos)
    )

    print("\nTRANSCRIPT RESULTS")
    print(transcript_results)

    all_moments = []

    for item in clip_results:

        all_moments.append({

            "video_id":
                item["video_id"],

            "timestamp":
                item["timestamp"],

            "source":
                "clip",

            "score":
                item["similarity"]
        })

    for item in yolo_results:

        all_moments.append({

            "video_id":
                item["video_id"],

            "timestamp":
                item["timestamp"],

            "source":
                "yolo",

            "score":
                1.0
        })

    for item in transcript_results:

        all_moments.append({

            "video_id":
                item["video_id"],

            "timestamp":
                item["start"],

            "source":
                "whisper",

            "score":
                1.0
        })

    all_moments.sort(
        key=lambda x:(
            x["video_id"],
            x["timestamp"]
        )
    )

    clusters = []
    current_cluster = []

    for moment in all_moments:

        if not current_cluster:

            current_cluster.append(
                moment
            )

            continue

        previous = current_cluster[-1]

        same_video = (
            previous["video_id"] == moment["video_id"]
        )

        close_in_time = (
            abs(moment["timestamp"] - previous["timestamp"]) <=
            CLUSTER_WINDOW
        )

        if same_video and close_in_time:

            current_cluster.append(
                moment
            )

        else:

            clusters.append(
                current_cluster
            )

            current_cluster = [
                moment
            ]

    # Add final cluster
    if current_cluster:

        clusters.append(
            current_cluster
        )

    unified_moments = []

    for cluster in clusters:

        timestamps = [

            item["timestamp"]

            for item in cluster
        ]

        center_timestamp = round(

            sum(timestamps) /
            len(timestamps),

            2
        )

        video_id = cluster[0]["video_id"]

        thumbnail = (

            get_nearest_frame(
                video_id,
                center_timestamp,
                FRAME_METADATA
            )
        )

        clip_score = 0.0
        yolo_score = 0.0
        whisper_score = 0.0

        for item in cluster:

            if item["source"] == "clip":

                clip_score = max(

                    clip_score,

                    item["score"]
                )

            elif item["source"] == "yolo":

                yolo_score = 1.0

            elif item["source"] == "whisper":

                whisper_score = 1.0


        cluster_score = (

            0.6 * clip_score +

            0.2 * yolo_score +

            0.2 * whisper_score
        )

        sources = list(

            set(

                item["source"]

                for item in cluster
            )
        )

        if cluster_score >= 0.50:

            confidence = "high"

        elif cluster_score >= 0.25:

            confidence = "medium"

        else:

            confidence = "low"

        thumbnail_path = None

        if thumbnail:

            thumbnail_path = (
                f"{video_id}/"
                f"{thumbnail['frame']}"
            )

        unified_moments.append({

            "timestamp":
                center_timestamp,
            
            "video_id":
                video_id,

            "thumbnail":
                thumbnail_path,

            "score":
                round(
                    cluster_score,
                    4
                ),

            "clip_score":
                round(
                    clip_score,
                    4
                ),

            "yolo_match":
                bool(
                    yolo_score
                ),

            "whisper_match":
                bool(
                    whisper_score
                ),

            "sources":
                sources,

            "confidence":
                confidence
        })

    unified_moments.sort(

        key=lambda x:
            x["score"],

        reverse=True
    )

    print("\n=== UNIFIED MOMENTS ===\n")

    for moment in unified_moments:

        print(moment)


    filtered = [

        moment

        for moment in unified_moments

        if moment["score"] >= MIN_SCORE
    ]

    if len(filtered) > 0:

        return filtered[:TOP_K_RESULTS]

    print("Fusion:", selected_videos)

    return unified_moments[:MIN_RESULTS]