# User Guide

## Overview

The Multimodal Video Search Engine enables users to upload, search, preview, and manage multiple videos using semantic understanding, object detection, and speech transcription.

The system supports batch uploads, scoped multi-video search, incremental indexing, automatic video switching, and direct navigation to relevant moments.

---

## Uploading Videos

1. Open the application.
2. Click **Choose Videos**.
3. Select one or more MP4 files.
4. Review the selected videos.
5. Remove unwanted files if necessary.
6. Click **Upload Videos**.
7. Wait for processing to complete.

During processing:

- File selection is locked.
- Videos cannot be removed.

After processing completes, successfully indexed videos appear in the Video Library.

Internally, during processing, the system:

* Extracts video frames
* Generates CLIP embeddings
* Detects objects using YOLOv8
* Generates transcripts using Whisper
* Creates an incremental searchable index without rebuilding existing videos.

Once processing is complete, the uploaded video becomes searchable.

---

## Searching Videos

1. Select one or more indexed videos.
2. Enter a search query.
3. Click Search.

Only the selected videos are searched.

Examples of search queries:

### Semantic Queries

* person using laptop
* people walking outdoors
* road traffic

### Object Queries

* person
* car
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

The application automatically:

1. Opens the correct video if another video is currently loaded.
2. Scrolls to the video player.
3. Seeks to the selected timestamp.
4. Begins playback automatically.

---

## Video Library

The Video Library displays all indexed videos.

Users can:

- Preview any indexed video
- Select multiple videos for searching
- Delete indexed videos
- Switch previews at any time

## Deleting Videos

Click the Delete button beside any indexed video.

Deleting a video removes:

- Video file
- Extracted frames
- CLIP embeddings
- FAISS vectors
- YOLO metadata
- Whisper transcript
- Audio file

## Troubleshooting

### No Results Found

Try:

* Different keywords
* Simpler object names
* Queries related to visible content

### Search not possible

Select at least one indexed video before searching.

### Video Preview Missing

Click Play on a video or Jump To Moment from a search result.

### Duplicate Videos

Videos already indexed are skipped automatically during batch uploads.

### Processing Interrupted

If processing fails:

- Failed videos are reported.
- Successfully processed videos remain indexed.
- Duplicate videos are skipped.

## Search Scope

The search engine only searches the videos selected in the Video Library.

This allows users to:

- Search a single lecture
- Search multiple meetings
- Compare videos
- Reduce irrelevant search results
