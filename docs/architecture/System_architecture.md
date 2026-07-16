# System Architecture

## Overview

The Multimodal Video Search Engine is a scalable multimedia retrieval system that combines computer vision, speech recognition, vector similarity search, and multimodal fusion to retrieve relevant moments across multiple videos.

The system supports incremental indexing, scoped multi-video search, batch uploads, automatic video switching, and complete video lifecycle management.

---

## High-Level Pipeline

```text
                    React + Vite
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
 Batch Video Upload                   Search Query
        │                                     │
        ▼                                     ▼
                  FastAPI Backend
                         │
                         ▼
              Video Processing Pipeline
                         │
        ┌────────┬────────┬────────┬─────────┐
        ▼        ▼        ▼        ▼
   Frame      CLIP     YOLO     Whisper
 Extraction Embeddings Objects Transcript
        │        │        │        │
        └────────┴────────┴────────┘
                    │
      Incremental FAISS Index (IndexIDMap2)
                    │
                    ▼
          Multimodal Fusion Engine
                    │
                    ▼
          Ranked Search Results
                    │
                    ▼
     Interactive Video Navigation
```

---

## Video Processing Pipeline

Each uploaded video passes through the following stages:

1. Frame Extraction
2. CLIP Embedding Generation
3. Incremental FAISS Indexing
4. YOLO Object Detection
5. Audio Extraction
6. Whisper Transcription
7. Metadata Generation
8. Video Library Update

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

Embeddings are normalized and inserted into a FAISS IndexIDMap2, enabling:

- Incremental indexing
- Stable vector IDs
- Efficient vector deletion
- Cosine similarity search

Outputs:

```text
indexes/
├── frame_index.faiss
├── frame_metadata.json
├── video_library.json
```

---

### YOLO Service

Detects objects in video frames.

Model:

```text
YOLOv8
```

Each processed frame stores detected object labels, allowing object-based retrieval within selected videos.

---

### Whisper Service

Generates speech transcripts.

Model:

```text
OpenAI Whisper
```

Output:

```text
transcripts/
├── lecture.json
├── lecture_audio.wav
├── meeting.json
├── meeting_audio.wav
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

Fusion combines evidence using:

- Temporal clustering
- Weighted confidence scoring
- Cross-modal evidence aggregation
- Ranking

Weights:

CLIP      → 0.6

YOLO      → 0.2

Whisper   → 0.2

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

## Incremental Indexing

The system avoids rebuilding the complete FAISS index when new videos are uploaded.

Each upload:

- generates new CLIP embeddings
- assigns unique vector IDs
- inserts vectors into IndexIDMap2
- updates metadata
- preserves existing vectors

## Video Lifecycle

Videos move through the following lifecycle:

```text

Upload
      ↓
Processing
      ↓
Indexing
      ↓
Search
      ↓
Preview
      ↓
Deletion
      ↓
Metadata Cleanup
      ↓
Vector Removal
```
---

## Frontend Architecture

### UploadForm

- Batch upload
- File validation
- Duplicate handling

### VideoLibrary

- Video preview
- Multi-video selection
- Video deletion

### SearchBar

- Query submission

### MomentResults

- Ranked results
- Confidence indicators
- Jump to moment

### VideoPlayer

- Automatic video switching
- Timestamp navigation

---

## Design Decisions

Why CLIP?

- Open vocabulary semantic search.

Why YOLO?

- Accurate object localization.

Why Whisper?

- Speech understanding.

Why FAISS?

- Fast approximate nearest-neighbor search.

Why IndexIDMap2?

- Stable vector identifiers for incremental insertion and deletion.

Why Temporal Fusion?

- Combines complementary evidence from vision and speech.

---

## Current Limitations

- Local filesystem storage
- CPU inference
- Sequential processing pipeline
- No authentication
- Single-user deployment

---

## Future Enhancements

- Background task queue
- Docker deployment
- GPU acceleration
- PostgreSQL metadata storage
- Cloud object storage
- Distributed vector database
- User authentication
- Query caching
- LLM-powered video summarization
- Conversational video search
