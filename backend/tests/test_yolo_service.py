from backend.services.yolo_service import (
    search_objects
)

results = search_objects(
    "person"
)

print(results)