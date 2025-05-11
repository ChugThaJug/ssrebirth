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
    let errorMessage;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;
    } catch {
      errorMessage = `HTTP error! status: ${response.status}`;
    }
    throw new Error(errorMessage);
  }

  return response;
}

export async function processContent(contentUrl: string, processingType: string, processingMode: string): Promise<ContentResponse> {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/content/process_content/`, {
      method: 'POST',
      body: JSON.stringify({
        content_type: 'youtube',
        content_id: contentUrl,
        processing_type: processingType,
        processing_mode: processingMode,
      }),
    });

    return await response.json();
  } catch (error) {
    console.error('Error processing content:', error);
    throw error;
  }
}

export async function getContentResult(contentId: string): Promise<ContentResponse> {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/content/${contentId}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching content result:', error);
    throw error;
  }
}

export async function updateContent(contentId: string, updateData: Partial<ContentResponse>): Promise<ContentResponse> {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/content/${contentId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });

    return await response.json();
  } catch (error) {
    console.error('Error updating content:', error);
    throw error;
  }
}

export interface ContentResponse {
  id: number;
  content_type: string;
  content_id: string;
  title: string | null;
  processed_content: string | null;
  processing_type: string;
  processing_mode: string;
  processing_time: number | null;
}