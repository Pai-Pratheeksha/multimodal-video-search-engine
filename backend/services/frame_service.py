"""
PURPOSE:
Extract frames from a video.

INPUT:
Video Path

OUTPUT:
frames/*.jpg

Used by:
Video Processing Pipeline
"""

import cv2
import os
import json

def extract_frames(
    video_path: str,
    output_dir: str = "frames"
):

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # Remove old frames
    for file in os.listdir(
        output_dir
    ):

        file_path = os.path.join(
            output_dir,
            file
        )

        if os.path.isfile(
            file_path
        ):
            os.remove(
                file_path
            )

    video = cv2.VideoCapture(
        video_path
    )

    fps = video.get(
        cv2.CAP_PROP_FPS
    )

    frame_count = 0
    saved_count = 0
    timestamps = {}

    while True:

        success, frame = (
            video.read()
        )

        if not success:
            break

        if frame_count % int(fps) == 0:

            frame_filename = (
                f"frame_{saved_count:04d}.jpg"
            )

            filename = os.path.join(
                output_dir,
                frame_filename
            )

            timestamps[
                frame_filename
            ] = {

                "timestamp":
                    round(
                        frame_count / fps,
                        2
                    )
            }

            cv2.imwrite(
                filename,
                frame
            )

            saved_count += 1

        frame_count += 1

    video.release()

    with open(
        "indexes/frame_timestamps.json",
        "w"
    ) as f:

        json.dump(
            timestamps,
            f,
            indent=4
        )

    return {
        "frames_extracted":
            saved_count,

        "output_directory":
            output_dir
    }