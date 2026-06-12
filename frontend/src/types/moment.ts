export interface Moment {

  timestamp: number;

  thumbnail?: string;

  score: number;

  clip_score: number;

  yolo_match: boolean;

  whisper_match: boolean;

  sources: string[];

  confidence:
    "high" |
    "medium" |
    "low";
}