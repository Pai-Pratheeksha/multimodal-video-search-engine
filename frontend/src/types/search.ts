export interface ClipResult {
  frame: string;
  similarity: number;
  timestamp: number;
}

export interface TranscriptResult {
  start: number;
  end: number;
  text: string;
}

export interface YoloResult {
  frame: string;
  timestamp: number;
}

export interface SearchResponse {
  query: string;
  clip_results: ClipResult[];
  yolo_results: YoloResult[];
  transcript_results: TranscriptResult[];
}