// src/lib/api.ts
import { user } from './firebase';
import { get } from 'svelte/store';

// Base URL for API
const API_BASE_URL = '/api/v1';

// Function to get auth headers
async function getAuthHeaders() {
  const currentUser = get(user);
  
  if (!currentUser || !currentUser.token) {
    throw new Error('User not authenticated');
  }
  
  return {
    'Authorization': `Bearer ${currentUser.token}`,
    'Content-Type': 'application/json'
  };
}

// Process a video
export async function processVideo(videoId: string, mode: string = 'detailed', chapterSource: string = 'auto') {
  try {
    const headers = await getAuthHeaders();
    
    const response = await fetch(`${API_BASE_URL}/youtube/process/${videoId}`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ mode, chapterSource })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to process video');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error processing video:', error);
    throw error;
  }
}

// Get processing status
export async function getProcessingStatus(jobId: string) {
  try {
    const headers = await getAuthHeaders();
    
    const response = await fetch(`${API_BASE_URL}/youtube/status/${jobId}`, {
      headers
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get processing status');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting status:', error);
    throw error;
  }
}

// Get video result
export async function getVideoResult(videoId: string) {
  try {
    const headers = await getAuthHeaders();
    
    const response = await fetch(`${API_BASE_URL}/youtube/result/${videoId}`, {
      headers
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get video result');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting video result:', error);
    throw error;
  }
}

// Get user's videos
export async function getUserVideos() {
  try {
    const headers = await getAuthHeaders();
    
    const response = await fetch(`${API_BASE_URL}/videos`, {
      headers
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get user videos');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting user videos:', error);
    throw error;
  }
}