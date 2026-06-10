from backend.services.fusion_service import (
    search_multimodal
)

results = search_multimodal(
    "person"
)

print("\nFusion Results:\n")

for item in results:

    print(item)