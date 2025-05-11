import type { PageLoad } from '@sveltejs/kit';

export const load: PageLoad = ({ params }) => {
  return {
    id: params.id
  };
};