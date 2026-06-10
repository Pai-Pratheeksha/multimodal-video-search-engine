from backend.services.unified_service import (
    unified_search
)

results = unified_search(
    "person"
)

print(results)