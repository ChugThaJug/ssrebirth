<!-- src/routes/(app)/dashboard/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { getUserVideos } from '$lib/api';
  import { Button } from '$lib/components/ui/button';
  import * as Card from '$lib/components/ui/card/index.js';
  import { Clock, ExternalLink, BarChart3 } from 'lucide-svelte';
  
  let videos = [];
  let loading = true;
  let error = null;
  
  onMount(async () => {
    try {
      loading = true;
      videos = await getUserVideos();
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  });
  
  function getStatusColor(status) {
    switch (status) {
      case 'completed': return 'text-green-500';
      case 'processing': return 'text-blue-500';
      case 'failed': return 'text-red-500';
      default: return 'text-gray-500';
    }
  }
</script>

<div class="flex h-full flex-col gap-6">
  <div>
    <h1 class="text-lg font-semibold">Your Videos</h1>
    <p class="text-sm">View and manage your processed YouTube videos.</p>
  </div>
  
  <div class="flex justify-between mb-4">
    <Button href="/process">Process New Video</Button>
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center h-40">
      <p>Loading your videos...</p>
    </div>
  {:else if error}
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      <p>{error}</p>
    </div>
  {:else if videos.length === 0}
    <Card.Root>
      <Card.Content class="flex flex-col items-center justify-center h-40">
        <p class="text-lg mb-4">You haven't processed any videos yet</p>
        <Button href="/process">Process Your First Video</Button>
      </Card.Content>
    </Card.Root>
  {:else}
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {#each videos as video}
        <Card.Root>
          <Card.Content class="p-0">
            <div class="relative">
              <img 
                src={`https://img.youtube.com/vi/${video.videoId}/maxresdefault.jpg`} 
                alt="Video thumbnail"
                class="w-full h-auto aspect-video object-cover rounded-t-lg"
              />
              <div class="absolute top-2 right-2">
                <span class={`px-2 py-1 rounded-full text-xs ${getStatusColor(video.status)} bg-white/90`}>
                  {video.status}
                </span>
              </div>
            </div>
            
            <div class="p-4">
              <h3 class="font-semibold line-clamp-1">{video.title || 'Untitled Video'}</h3>
              
              <div class="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                <Clock class="h-3 w-3" />
                <span>{new Date(video.createdAt).toLocaleDateString()}</span>
                {#if video.stats}
                  <span class="mx-2">•</span>
                  <BarChart3 class="h-3 w-3" />
                  <span>${video.stats.total_price || '0.00'}</span>
                {/if}
              </div>
              
              <div class="flex justify-between mt-4">
                <Button 
                  variant="outline" 
                  href={`/result/${video.videoId}`} 
                  disabled={video.status !== 'completed'}
                >
                  View Results
                </Button>
                
                <Button 
                  variant="ghost" 
                  href={`https://youtube.com/watch?v=${video.videoId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ExternalLink class="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card.Content>
        </Card.Root>
      {/each}
    </div>
  {/if}
</div>