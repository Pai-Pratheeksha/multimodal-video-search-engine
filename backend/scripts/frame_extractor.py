"""
PURPOSE:
Extract frames from a video.

INPUT:
videos/sample.mp4

OUTPUT:
frames/frame_0000.jpg
frames/frame_0001.jpg
...

Used whenever a new video is added.
"""
import cv2
import os

VIDEO_PATH = "videos/sample.mp4"
OUTPUT_DIR = "frames"

os.makedirs(OUTPUT_DIR, exist_ok=True)

video = cv2.VideoCapture(VIDEO_PATH)

fps = video.get(cv2.CAP_PROP_FPS)

frame_count = 0
saved_count = 0

while True:
    success, frame = video.read()

    if not success:
        break

    if frame_count % int(fps) == 0:
        filename = os.path.join(
            OUTPUT_DIR,
            f"frame_{saved_count:04d}.jpg"
        )

        cv2.imwrite(filename, frame)
        saved_count += 1

    frame_count += 1

video.release()

print(f"Saved {saved_count} frames")