const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  const token = localStorage.getItem('token');
  const headers = {
    ...options.headers,
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  };

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    console.error('Error response:', errorData);
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response;
}

export async function processVideo(youtubeUrl: string, processingMode: string) {
  const response = await fetchWithAuth(`${API_BASE_URL}/video/process_video/`, {
    method: 'POST',
    body: JSON.stringify({ youtube_url: youtubeUrl, processing_mode: processingMode }),
  });

  return await response.json();
}

export async function getVideoResult(videoId: string) {
  const response = await fetchWithAuth(`${API_BASE_URL}/video/${videoId}`);
  return await response.json();
}

export async function updateVideoSummary(id: string, summary: string) {
  const response = await fetchWithAuth(`${API_BASE_URL}/video/${id}/summary`, {
    method: 'PUT',
    body: JSON.stringify({ summary }),
  });

  return await response.json();
}

export async function updateVideoTranscript(id: string, transcript: string) {
  const response = await fetchWithAuth(`${API_BASE_URL}/video/${id}/transcript`, {
    method: 'PUT',
    body: JSON.stringify({ transcript }),
  });

  return await response.json();
}

// ... (other API functions remain the same)