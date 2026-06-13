# System Architecture

## Overview

The Multimodal Video Search Engine combines computer vision, speech recognition, vector search, and multimodal fusion to retrieve relevant video moments.

---

## High-Level Pipeline

```text
Video Upload
      │
      ▼
Video Processing
      │
 ┌────┼────┐
 ▼    ▼    ▼
CLIP YOLO Whisper
 │    │     │
 └────┼─────┘
      ▼
Fusion Engine
      ▼
Unified Moments
      ▼
React Frontend
```

---

## Video Processing Pipeline

### Frame Extraction

OpenCV extracts frames from uploaded videos.

Output:

```text
frames/
```

---

### CLIP Service

Generates image embeddings for extracted frames.

Model:

```text
openai/clip-vit-base-patch16
```

Embeddings are indexed using FAISS.

Outputs:

```text
frame_index.faiss
frame_names.json
```

---

### YOLO Service

Detects objects in video frames.

Model:

```text
YOLOv8
```

Output:

```text
frame_objects.json
```

---

### Whisper Service

Generates speech transcripts.

Model:

```text
OpenAI Whisper
```

Output:

```text
transcript.json
```

---

## Search Pipeline

### Semantic Search

Query → CLIP Text Embedding → FAISS Search

---

### Object Search

Query → Object Match → Matching Frames

---

### Transcript Search

Query → Transcript Match → Relevant Segments

---

## Fusion Engine

Combines results from:

* CLIP
* YOLO
* Whisper

Techniques:

* Temporal Clustering
* Confidence Scoring
* Evidence Aggregation
* Ranking

Output:

```json
{
  "timestamp": 42.3,
  "score": 0.81,
  "confidence": "high",
  "sources": [
    "clip",
    "yolo"
  ]
}
```

---

## Frontend Architecture

### UploadForm

Video upload and processing.

### SearchBar

Natural language query input.

### VideoPlayer

Video preview and playback.

### MomentResults

Search result visualization and navigation.

---

## Current Limitations

* Single video indexing
* Local FAISS storage
* Sequential processing
* CPU inference

---

## Future Enhancements

* Multi-video collections
* PostgreSQL metadata storage
* Qdrant vector database
* Agentic AI query planning
* Streaming video indexing
* Cloud deployment
