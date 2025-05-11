import type { 
  YouTubeProcessingResponse, 
  YouTubeProcessingStatus,
  YouTubeResult,
  Chapter,
  ProcessingStats
} from '$lib/types/api';
import { ProcessingMode, ChapterSource } from '$lib/types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = 'An error occurred';
    try {
      const error = await response.json();
      message = error.detail || message;
    } catch (_) {
      message = response.statusText;
    }
    throw new APIError(response.status, message);
  }
  return response.json();
}

export async function processVideo(
  videoId: string,
  mode: ProcessingMode = ProcessingMode.DETAILED,
  chapterSource: ChapterSource = ChapterSource.AUTO
): Promise<YouTubeProcessingResponse> {
  const response = await fetch(
    `${API_BASE_URL}/youtube/process/${videoId}?mode=${mode}&chapter_source=${chapterSource}`,
    { method: 'POST' }
  );
  return handleResponse(response);
}

export async function getProcessingStatus(jobId: string): Promise<YouTubeProcessingStatus> {
  const response = await fetch(`${API_BASE_URL}/youtube/status/${jobId}`);
  return handleResponse(response);
}

export async function getLatestVideoStatus(videoId: string): Promise<YouTubeProcessingStatus> {
  const response = await fetch(`${API_BASE_URL}/youtube/latest-status?video_id=${videoId}`);
  return handleResponse(response);
}

export async function getVideoResult(videoId: string): Promise<YouTubeResult> {
  const response = await fetch(`${API_BASE_URL}/youtube/result/${videoId}`);
  return handleResponse(response);
}

// Export all types
export type {
  YouTubeProcessingResponse,
  YouTubeProcessingStatus,
  YouTubeResult,
  Chapter,
  ProcessingStats
};

// Export enums
export { ProcessingMode, ChapterSource };