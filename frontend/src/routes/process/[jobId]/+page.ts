import type { PageLoad } from './$types';

export const load = (({ params }) => {
  return {
    jobId: params.jobId
  };
}) satisfies PageLoad;