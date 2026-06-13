# User Guide

## Overview

The Multimodal Video Search Engine enables users to search video content using natural language queries, object detection, and speech transcription.

Users can upload a video, search for relevant content, and instantly navigate to important moments.

---

## Uploading a Video

1. Open the application.
2. Click **Choose Video**.
3. Select an MP4 video.
4. Click **Upload Video**.
5. Wait until processing completes.

During processing, the system:

* Extracts video frames
* Generates CLIP embeddings
* Detects objects using YOLOv8
* Generates transcripts using Whisper
* Builds searchable indexes

Once processing is complete, the uploaded video becomes searchable.

---

## Searching

Enter a search query in the search bar.

Examples:

### Semantic Queries

* person using laptop
* people walking outdoors
* road traffic
* building

### Object Queries

* person
* car
* chair
* laptop

### Speech Queries

* machine learning
* artificial intelligence
* computer vision

---

## Understanding Search Results

Each result contains:

* Thumbnail preview
* Timestamp
* Confidence score
* Evidence sources

Confidence levels:

### High Confidence

Strong agreement between multiple modalities.

### Medium Confidence

Moderate relevance.

### Low Confidence

Closest available match when stronger matches are unavailable.

---

## Jump To Moment

Click **Jump To Moment**.

The video player will:

1. Scroll into view.
2. Seek to the selected timestamp.
3. Begin playback automatically.

---

## Indexed Video

The application displays the currently indexed video.

Only the indexed video is searchable at any time.

Uploading a new video replaces the existing indexes.

---

## Troubleshooting

### No Results Found

Try:

* Different keywords
* Simpler object names
* Queries related to visible content

### Search Disabled

Upload and process a video before searching.

### Video Preview Missing

Refresh the page or upload a video again.
