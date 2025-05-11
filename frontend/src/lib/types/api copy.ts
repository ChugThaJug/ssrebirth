export enum ProcessingMode {
  SIMPLE = "simple",
  DETAILED = "detailed",
  DETAILED_WITH_SCREENSHOTS = "detailed_with_screenshots"
}

export enum ChapterSource {
  AUTO = "auto",
  DESCRIPTION = "description"
}

export interface Chapter {
  num_chapter: number;
  title: string;
  start_paragraph_number: number;
  end_paragraph_number: number;
  start_time: number;
  end_time: number;
  paragraphs: string[];
  paragraph_timestamps: number[];
  screenshots?: string[];
}

export interface ProcessingStats {
  total_input_tokens: number;
  total_output_tokens: number;
  total_price: number;
}

export interface YouTubeResult {
  video_id: string;
  chapters: Chapter[];
  stats: ProcessingStats;
}

export interface YouTubeProcessingResponse {
  job_id: string;
  video_id: string;
  status: string;
  error?: string;
}

export interface YouTubeProcessingStatus {
  job_id: string;
  video_id: string;
  status: string;
  progress: number;
  result?: YouTubeResult;
  error?: string;
}