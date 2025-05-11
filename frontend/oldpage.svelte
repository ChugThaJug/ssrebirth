<script lang="ts">
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import { getVideoResult, getLatestVideoStatus } from '$lib/services/api';
  import type { YouTubeResult } from '$lib/services/api';
  import { formatTime, formatNumber, formatPrice } from '$lib/utils/format';
  import { getYoutubeThumbnail } from '$lib/utils/youtube';
  import { Button } from "$lib/components/ui/button";
  import { 
    Card, 
    CardContent, 
    CardHeader, 
    CardTitle,
    CardDescription 
  } from "$lib/components/ui/card";
  import { goto } from '$app/navigation';

  export let data: { videoId: string };
  
  let result: YouTubeResult | null = null;
  let error: string | null = null;
  let loading = true;

  async function fetchResult(videoId: string) {
    try {
      loading = true;
      error = null;

      // Check if processing is complete
      const status = await getLatestVideoStatus(videoId);
      
      if (status.status === 'processing') {
        // If still processing, redirect to processing page
        await goto(`/process/${status.job_id}`);
        return;
      }
      
      if (status.status === 'failed') {
        throw new Error(status.error || "Processing failed");
      }

      // Fetch the result
      result = await getVideoResult(videoId);
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load video result";
    } finally {
      loading = false;
    }
  }

  onMount(async () => {
    if (!data.videoId) {
      error = "No video ID provided";
      loading = false;
      return;
    }

    await fetchResult(data.videoId);
  });

  function copyTimestamp(time: number) {
    const timestamp = formatTime(time);
    navigator.clipboard.writeText(timestamp);
  }
</script>

<svelte:head>
  <title>{result?.title || 'Video Result'} | Stepify</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
  {#if loading}
    <div class="flex flex-col items-center justify-center py-12" transition:fade>
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-foreground"></div>
      <p class="mt-4 text-sm text-muted-foreground">Loading analysis...</p>
    </div>
  {:else if error}
    <div class="max-w-2xl mx-auto" transition:fade>
      <div 
        class="bg-destructive/15 text-destructive px-4 py-3 rounded-lg"
        role="alert"
      >
        <h2 class="font-medium">Error</h2>
        <p class="text-sm mt-1">{error}</p>
        <div class="mt-4 flex gap-2">
          <Button variant="outline" href="/">Process New Video</Button>
          {#if data.videoId}
            <Button variant="outline" on:click={() => fetchResult(data.videoId)}>
              Try Again
            </Button>
          {/if}
        </div>
      </div>
    </div>
  {:else if result}
    <div class="max-w-4xl mx-auto space-y-8" transition:fade>
      <!-- Header -->
      <div class="flex justify-between items-start">
        <div>
          <h1 class="text-3xl font-bold">{result.title || 'Video Analysis'}</h1>
          <p class="text-muted-foreground mt-2">Structured content and analysis</p>
        </div>
        <Button variant="outline" href="/">Process New Video</Button>
      </div>

      <!-- Video Preview -->
      {#if result.video_id}
        <div transition:fade>
          <Card>
            <CardContent class="p-0">
              <img 
                src={getYoutubeThumbnail(result.video_id)} 
                alt="Video thumbnail"
                class="w-full h-auto rounded-t-lg object-cover"
              />
              <div class="p-6">
                <div class="flex justify-between items-center">
                  <h2 class="text-xl font-semibold">{result.title || 'Video Content'}</h2>
                  <a 
                    href={`https://youtube.com/watch?v=${result.video_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-sm text-muted-foreground hover:text-foreground"
                  >
                    Watch on YouTube ↗
                  </a>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      {/if}

      <!-- Chapters -->
      {#if result.chapters?.length > 0}
        <div class="space-y-6">
          {#each result.chapters as chapter (chapter.num_chapter)}
            <div transition:fade>
              <Card>
                <CardHeader>
                  <div class="flex justify-between items-center">
                    <CardTitle>
                      Chapter {chapter.num_chapter}: {chapter.title}
                    </CardTitle>
                    <Button 
                      variant="ghost" 
                      size="sm"
                      on:click={() => copyTimestamp(chapter.start_time)}
                      class="text-muted-foreground hover:text-foreground"
                    >
                      {formatTime(chapter.start_time)}
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div class="space-y-4">
                    {#each chapter.paragraphs as paragraph, i}
                      <div class="group relative">
                        <p class="text-sm leading-relaxed pr-16">
                          {paragraph}
                        </p>
                        <button
                          class="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity text-xs text-muted-foreground hover:text-foreground"
                          on:click={() => copyTimestamp(chapter.paragraph_timestamps[i])}
                        >
                          {formatTime(chapter.paragraph_timestamps[i])}
                        </button>
                      </div>
                    {/each}

                    {#if chapter.screenshots?.length}
                      <div class="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3">
                        {#each chapter.screenshots as screenshot}
                          <img 
                            src={screenshot} 
                            alt={`Screenshot from ${chapter.title}`}
                            class="rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-zoom-in"
                            loading="lazy"
                          />
                        {/each}
                      </div>
                    {/if}
                  </div>
                </CardContent>
              </Card>
            </div>
          {/each}
        </div>
      {:else}
        <div transition:fade>
          <Card>
            <CardContent class="py-8">
              <p class="text-center text-muted-foreground">
                No chapters available for this video.
              </p>
            </CardContent>
          </Card>
        </div>
      {/if}

      <!-- Processing Stats -->
      {#if result.stats}
        <div transition:fade>
          <Card>
            <CardHeader>
              <CardTitle>Processing Statistics</CardTitle>
              <CardDescription>Analysis and processing metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <dl class="grid grid-cols-2 gap-4 sm:grid-cols-3">
                <div>
                  <dt class="text-sm font-medium text-muted-foreground">Input Tokens</dt>
                  <dd class="mt-1 text-2xl font-semibold">
                    {formatNumber(result.stats.total_input_tokens)}
                  </dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-muted-foreground">Output Tokens</dt>
                  <dd class="mt-1 text-2xl font-semibold">
                    {formatNumber(result.stats.total_output_tokens)}
                  </dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-muted-foreground">Processing Cost</dt>
                  <dd class="mt-1 text-2xl font-semibold">
                    {formatPrice(result.stats.total_price)}
                  </dd>
                </div>
              </dl>
            </CardContent>
          </Card>
        </div>
      {/if}
    </div>
  {/if}
</div>