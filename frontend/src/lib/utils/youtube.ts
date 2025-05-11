// src/lib/utils/youtube.ts
export function getVideoId(url: string): string | null {
  if (!url) return null;
  
  try {
    // Regular URL formats
    const regExp = /^.*(youtu.be\/|v\/|e\/|u\/\w+\/|embed\/|v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    
    if (match && match[2].length === 11) {
      return match[2];
    }
    
    // URL in format youtube.com/shorts/ID
    const shortsExp = /^.*(youtube.com\/shorts\/)([^#\&\?]*).*/;
    const shortsMatch = url.match(shortsExp);
    
    if (shortsMatch && shortsMatch[2].length === 11) {
      return shortsMatch[2];
    }
    
    // Handle direct video ID input (11 characters)
    if (url.length === 11 && /^[A-Za-z0-9_-]{11}$/.test(url)) {
      return url;
    }
    
    return null;
  } catch (error) {
    console.error('Error parsing YouTube URL:', error);
    return null;
  }
}