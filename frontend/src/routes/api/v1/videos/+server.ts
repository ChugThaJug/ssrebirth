// src/routes/api/v1/videos/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { authenticateRequest } from '$lib/server/auth';
import { prisma } from '$lib/server/prisma';

export const GET: RequestHandler = async (event) => {
  try {
    const user = await authenticateRequest(event);
    
    if (!user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), { 
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const videos = await prisma.video.findMany({
      where: { userId: user.id },
      orderBy: { createdAt: 'desc' }
    });
    
    return json(videos);
  } catch (error) {
    console.error('Error fetching videos:', error);
    return new Response(JSON.stringify({ error: 'Failed to fetch videos' }), { 
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};