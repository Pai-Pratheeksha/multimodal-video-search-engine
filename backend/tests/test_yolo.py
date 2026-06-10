"""
PURPOSE:
Verify YOLO installation and object detection.

Used for:
- Testing YOLO model
- Checking detections on sample frames

Debug file only.
"""
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("frames/frame_0000.jpg")

for result in results:

    for box in result.boxes:

        class_id = int(box.cls)

        print(
            model.names[class_id]
        )