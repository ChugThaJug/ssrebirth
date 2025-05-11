// frontend/src/lib/apiService.ts
import { browser } from '$app/environment';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  if (!browser) return new Response();

  const token = localStorage.getItem('token');
  const headers = {
    ...options.headers,
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  };

  const response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return response;
}

export async function processVideo(
  videoId: string, 
  mode: string = 'detailed',
  chapterSource: string = 'auto'
): Promise<any> {
  const response = await fetchWithAuth(
    `${API_BASE_URL}/youtube/process/${videoId}`,
    {
      method: 'POST',
      body: JSON.stringify({ mode, chapter_source: chapterSource })
    }
  );
  return response.json();
}

export async function getProcessingStatus(jobId: string): Promise<any> {
  const response = await fetchWithAuth(`${API_BASE_URL}/youtube/status/${jobId}`);
  return response.json();
}

export async function getVideoResult(videoId: string): Promise<any> {
  const response = await fetchWithAuth(`${API_BASE_URL}/youtube/result/${videoId}`);
  return response.json();
}

export async function loginUser(email: string, password: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }
  
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
}

export async function registerUser(
  email: string, 
  password: string, 
  username: string
): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, username })
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Registration failed');
  }
  
  return response.json();
}