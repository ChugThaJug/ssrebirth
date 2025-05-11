import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { isValidVideoId } from '$lib/utils/youtube';

export const load = (({ params }) => {
  const { videoId } = params;

  if (!videoId || !isValidVideoId(videoId)) {
    throw error(400, {
      message: 'Invalid video ID'
    });
  }

  return {
    videoId
  };
}) satisfies PageLoad;