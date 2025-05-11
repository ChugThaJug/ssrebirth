// src/lib/api.ts
const API_BASE_URL = 'http://localhost:8000'; // Update this to your API URL


export async function processVideo(youtubeUrl: string, processingMode: string) {
  const response = await fetch(`${API_BASE_URL}/process_video/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ youtube_url: youtubeUrl, processing_mode: processingMode }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to process video');
  }

  return await response.json();
}

export async function getVideoResult(videoId: string) {
  const response = await fetch(`${API_BASE_URL}/video/${videoId}`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch video result for ID: ${videoId}`);
  }

  return await response.json();
}

export async function updateVideoSummary(id: string, summary: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/video/${id}/summary`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ summary }),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to update summary');
  }
}

export async function updateVideoTranscript(id: string, transcript: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/video/${id}/transcript`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ transcript }),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to update transcript');
  }
}

export async function loginWithOAuth(provider: string, code: string) {
  const response = await fetchWithAuth(`${API_BASE_URL}/auth/login/oauth/${provider}`, {
    method: 'POST',
    body: JSON.stringify({ code }),
  });

  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
}

export async function createSubscription(plan: string) {
  const response = await fetchWithAuth(`${API_BASE_URL}/billing/create_subscription`, {
    method: 'POST',
    body: JSON.stringify({ plan }),
  });

  return await response.json();
}

export async function getSubscriptionStatus() {
  const response = await fetchWithAuth(`${API_BASE_URL}/billing/subscription_status`);
  return await response.json();
}