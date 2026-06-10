# Multimodal Video Search Engine

A multimodal video retrieval system that enables users to search video content using:

- Semantic Search (CLIP)
- Object Detection (YOLOv8)
- Speech Search (Whisper)
- Multimodal Fusion Ranking

Users can upload a video, search using natural language queries, and instantly jump to the most relevant moments.

---

## Features

### Semantic Search

Uses OpenAI CLIP embeddings and FAISS indexing to retrieve visually similar frames from natural language queries.

Example:

> "person using a laptop"

---

### Object Search

Uses YOLOv8 object detection to search frames containing detected objects.

Example:

> "person"

> "car"

> "chair"

---

### Speech Search

Uses OpenAI Whisper transcription to search spoken content.

Example:

> "machine learning"

> "artificial intelligence"

---

### Multimodal Fusion

Results from:

- CLIP
- YOLO
- Whisper

are fused into unified moments using:

- Temporal clustering
- Weighted ranking
- Evidence aggregation

---

### Interactive Video Navigation

- Thumbnail previews
- Jump to timestamp
- Auto-play
- Smooth scrolling

---

## Architecture

```text
Video Upload
      │
      ▼
Video Processing Pipeline
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
Frontend Results
      ▼
Jump To Moment
```

---

## Tech Stack

### Backend

- FastAPI
- PyTorch
- Transformers
- FAISS
- OpenCV
- YOLOv8
- Whisper

### Frontend

- React
- TypeScript
- Tailwind CSS
- Axios
- Vite

---

## Project Structure

```text
backend/
├── app.py
├── models/
├── services/
├── tests/
└── scripts/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── api/
│   └── types/

docs/
.gitignore
requirements.txt
README.md
```

---

## Installation

### Backend

```bash
pip install -r requirements.txt
```

Start API:

```bash
uvicorn backend.app:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## First Run

Create the required directories:

```bash
mkdir frames
mkdir indexes
mkdir transcripts
mkdir videos
```

Download the YOLO model:

```bash
yolo detect predict model=yolov8n.pt
```

or download `yolov8n.pt` from the Ultralytics release page and place it in the project root.

Then start the backend:

```bash
uvicorn backend.app:app --reload
```
---

## Future Improvements

- Agentic AI Query Planning
- Real-time Video Indexing
- Multi-video Collections
- Hybrid Vector Databases
- Cloud Deployment
