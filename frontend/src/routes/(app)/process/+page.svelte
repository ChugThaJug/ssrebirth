<!-- src/routes/(app)/process/+page.svelte -->
<script lang="ts">
  import { processVideo } from '$lib/api';
  import { getVideoId } from '$lib/utils/youtube';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import * as Card from '$lib/components/ui/card';
  import { goto } from '$app/navigation';
  import { toast } from 'svelte-sonner';
  
  let videoUrl = '';
  let mode = 'detailed';
  let chapterSource = 'auto';
  let loading = false;
  
  async function handleSubmit() {
    try {
      if (!videoUrl) {
        toast.error('Please enter a YouTube URL');
        return;
      }
      
      const ytVideoId = getVideoId(videoUrl);
      
      if (!ytVideoId) {
        toast.error('Invalid YouTube URL');
        return;
      }
      
      loading = true;
      const result = await processVideo(ytVideoId, mode, chapterSource);
      toast.success('Video processing started');
      goto(`/process/${result.job_id}`);
    } catch (error) {
      console.error('Processing error:', error);
      toast.error(error.message || 'Failed to process video');
    } finally {
      loading = false;
    }
  }
</script>

<div class="container mx-auto px-4 py-8">
  <div class="mx-auto max-w-2xl">
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold mb-2">Process YouTube Video</h1>
      <p class="text-muted-foreground">Enter a YouTube URL to convert it into structured content</p>
    </div>
    
    <Card.Root>
      <Card.Content class="p-6">
        <form on:submit|preventDefault={handleSubmit} class="space-y-6">
          <div class="space-y-2">
            <label for="videoUrl" class="text-sm font-medium">
              YouTube URL <span class="text-destructive">*</span>
            </label>
            <Input 
              id="videoUrl"
              type="url" 
              bind:value={videoUrl}
              placeholder="https://www.youtube.com/watch?v=..."
              required
            />
          </div>
          
          <div class="grid gap-6 sm:grid-cols-2">
            <div class="space-y-2">
              <label for="processingMode" class="text-sm font-medium">
                Processing Mode
              </label>
              <select 
                id="processingMode"
                class="w-full rounded-md border border-input px-3 py-2"
                bind:value={mode}
              >
                <option value="simple">Simple (Fastest)</option>
                <option value="detailed">Detailed</option>
                <option value="detailed_with_screenshots">Detailed with Screenshots</option>
              </select>
              <p class="text-xs text-muted-foreground">
                {#if mode === 'simple'}
                  Quick processing with basic structuring
                {:else if mode === 'detailed'}
                  Detailed analysis with better organization
                {:else}
                  Comprehensive analysis with visual aids
                {/if}
              </p>
            </div>
            
            <div class="space-y-2">
              <label for="chapterSource" class="text-sm font-medium">
                Chapter Source
              </label>
              <select 
                id="chapterSource"
                class="w-full rounded-md border border-input px-3 py-2"
                bind:value={chapterSource}
              >
                <option value="auto">Auto-generated</option>
                <option value="description">From Description</option>
              </select>
              <p class="text-xs text-muted-foreground">
                {chapterSource === 'auto' 
                  ? 'AI-generated chapters based on content'
                  : 'Use chapters from video description'}
              </p>
            </div>
          </div>
          
          <Button 
            type="submit" 
            disabled={loading} 
            class="w-full"
          >
            {#if loading}
              <span class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent mr-2"></span>
              Processing...
            {:else}
              Process Video
            {/if}
          </Button>
        </form>
      </Card.Content>
    </Card.Root>
    
    <div class="mt-6 rounded-lg bg-muted p-4 text-sm">
      <h3 class="font-medium mb-2">Processing Information</h3>
      <ul class="list-disc list-inside space-y-1">
        <li>Processing time varies based on video length and selected mode</li>
        <li>Simple mode is fastest but provides basic structure</li>
        <li>Detailed mode provides better organization and summaries</li>
        <li>Screenshots are only available in the detailed with screenshots mode</li>
      </ul>
    </div>
  </div>
</div>