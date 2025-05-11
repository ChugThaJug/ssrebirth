// src/routes/api/v1/youtube/process/[videoId]/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { authenticateRequest } from '$lib/server/auth';
import { prisma } from '$lib/server/prisma';
import { ProcessingMode, ChapterSource } from '$lib/types';

export const POST: RequestHandler = async (event) => {
  try {
    const user = await authenticateRequest(event);
    
    if (!user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), { 
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    const { videoId } = event.params;
    const { mode = 'detailed', chapterSource = 'auto' } = await event.request.json();
    
    // Check subscription limits
    if (user.tokenUsage >= user.tokenLimit) {
      return new Response(JSON.stringify({ 
        error: 'You have reached your monthly processing limit. Please upgrade your subscription.' 
      }), { 
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Create a unique job ID
    const jobId = `yt_job_${new Date().toISOString().replace(/[-:.]/g, '')}_${videoId}`;
    
    // First create or find the video
    let video = await prisma.video.findUnique({
      where: { videoId }
    });
    
    if (!video) {
      video = await prisma.video.create({
        data: {
          videoId,
          userId: user.id,
          processingMode: mode,
          chapterSource: chapterSource,
          status: 'pending'
        }
      });
    }
    
    // Then create the processing job
    const job = await prisma.processingJob.create({
      data: {
        jobId,
        videoId: video.id,
        userId: user.id,
        status: 'processing',
        mode,
        chapterSource
      }
    });
    
    // Start the processing in the background (this would call your existing processing logic)
    // processVideo(job.id, videoId, mode, chapterSource); // Background task
    
    return json({
      job_id: jobId,
      video_id: videoId,
      status: 'processing',
      mode,
      chapter_source: chapterSource
    });
  } catch (error) {
    console.error('Processing error:', error);
    return new Response(JSON.stringify({ error: 'Failed to process video' }), { 
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};