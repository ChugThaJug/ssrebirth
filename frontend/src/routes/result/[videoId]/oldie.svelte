<script lang="ts">
    import { onMount } from 'svelte';
    import { fade, slide } from 'svelte/transition';
    import { getVideoResult, getLatestVideoStatus } from '$lib/services/api';
    import type { YouTubeResult } from '$lib/types/api';
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
    import { 
      Stepper, 
      StepperItem, 
      StepperTitle, 
      StepperDescription 
    } from "$lib/components/ui/stepper";
    import { 
      ChevronDown, 
      ExternalLink, 
      Copy, 
      RefreshCw,
      Clock,
      FileText,
      BarChart3
    } from 'lucide-svelte';
    import { goto } from '$app/navigation';
  
    export let data: { videoId: string };
    
    let result: YouTubeResult | null = null;
    let error: string | null = null;
    let loading = true;
    let activeChapter = 0;
    let showAllText = false;
  
    async function fetchResult(videoId: string) {
      try {
        loading = true;
        error = null;
  
        const status = await getLatestVideoStatus(videoId);
        
        if (status.status === 'processing') {
          await goto(`/process/${status.job_id}`);
          return;
        }
        
        if (status.status === 'failed') {
          throw new Error(status.error || "Processing failed");
        }
  
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
  
    async function copyTimestamp(time: number) {
      try {
        await navigator.clipboard.writeText(formatTime(time));
      } catch (err) {
        console.error('Failed to copy timestamp:', err);
      }
    }
  
    function handleRetry() {
      fetchResult(data.videoId);
    }
  
    function handleChapterClick(index: number) {
      activeChapter = index;
    }
  </script>
  
  <svelte:head>
    <title>{result?.title || 'Video Result'} | Stepify</title>
    <meta name="description" content="Structured analysis and summary of the video content" />
  </svelte:head>
  
  <div class="container mx-auto px-4 py-8">
    {#if loading}
      <div 
        class="flex flex-col items-center justify-center py-12" 
        in:fade={{ duration: 200 }}
      >
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-foreground"></div>
        <p class="mt-4 text-sm text-muted-foreground">Loading analysis...</p>
      </div>
    {:else if error}
      <div 
        class="max-w-2xl mx-auto" 
        in:fade={{ duration: 200 }}
      >
        <Card>
          <CardContent class="pt-6">
            <div class="flex flex-col items-center text-center">
              <div class="rounded-full bg-destructive/15 p-3 text-destructive">
                <FileText class="h-6 w-6" />
              </div>
              <h2 class="mt-3 text-lg font-semibold">Error Loading Result</h2>
              <p class="mt-2 text-sm text-muted-foreground">{error}</p>
              <div class="mt-6 flex gap-3">
                <Button variant="outline" href="/">
                  Process New Video
                </Button>
                {#if data.videoId}
                  <Button variant="outline" on:click={handleRetry}>
                    <RefreshCw class="mr-2 h-4 w-4" />
                    Try Again
                  </Button>
                {/if}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    {:else if result}
      <div 
        class="max-w-4xl mx-auto space-y-8" 
        in:fade={{ duration: 200 }}
      >
        <!-- Video Preview -->
        {#if result.video_id}
          <div in:fade={{ duration: 300, delay: 100 }}>
            <Card>
              <CardContent class="p-0">
                <div class="relative">
                  <img 
                    src={getYoutubeThumbnail(result.video_id)} 
                    alt="Video thumbnail"
                    class="w-full h-auto rounded-t-lg object-cover"
                  />
                  <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent rounded-t-lg" />
                  <div class="absolute bottom-4 left-4 right-4">
                    <h1 class="text-white text-xl md:text-2xl font-bold leading-tight">
                      {result.title || 'Video Analysis'}
                    </h1>
                  </div>
                </div>
                
                <div class="p-4 md:p-6 flex flex-wrap gap-3 justify-between items-center">
                  <div class="flex flex-wrap gap-2">
                    <Button variant="outline" href="/">
                      Process New Video
                    </Button>
                    <a 
                      href={`https://youtube.com/watch?v=${result.video_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Button variant="ghost" class="gap-2">
                        <ExternalLink class="h-4 w-4" />
                        Watch on YouTube
                      </Button>
                    </a>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        {/if}
  
        <!-- Chapters -->
        {#if result.chapters?.length > 0}
          <div 
            class="space-y-6"
            in:fade={{ duration: 300, delay: 200 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Video Chapters</CardTitle>
                <CardDescription>
                  Click on a chapter to view its content
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Stepper 
                  bind:activeStep={activeChapter}
                  orientation="vertical"
                  class="w-full"
                >
                  {#each result.chapters as chapter, i (chapter.num_chapter)}
                    <StepperItem 
                      step={i}
                      class="cursor-pointer"
                      on:click={() => handleChapterClick(i)}
                    >
                      <StepperTitle class={activeChapter === i ? "text-primary" : ""}>
                        {chapter.title}
                      </StepperTitle>
                      <div class="flex items-center gap-2 mt-1">
                        <Clock class="h-3 w-3 text-muted-foreground" />
                        <StepperDescription class={activeChapter === i ? "text-primary" : ""}>
                          {formatTime(chapter.start_time)} - {formatTime(chapter.end_time)}
                        </StepperDescription>
                      </div>
  
                      {#if activeChapter === i}
                        <div 
                          class="mt-4 space-y-4 text-foreground"
                          transition:slide={{ duration: 200 }}
                        >
                          {#each chapter.paragraphs as paragraph, pIndex}
                            <div class="group relative">
                              <p class="text-sm leading-relaxed pr-16">
                                {paragraph}
                              </p>
                              <button
                                class="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity text-xs text-muted-foreground hover:text-foreground flex items-center gap-1"
                                on:click|stopPropagation={() => copyTimestamp(chapter.paragraph_timestamps[pIndex])}
                              >
                                <Copy class="h-3 w-3" />
                                {formatTime(chapter.paragraph_timestamps[pIndex])}
                              </button>
                            </div>
                          {/each}
  
                          {#if chapter.screenshots?.length}
                            <div 
                              class="mt-6 grid grid-cols-2 gap-4 md:grid-cols-3"
                              transition:slide={{ duration: 200 }}
                            >
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
                      {/if}
                    </StepperItem>
                  {/each}
                </Stepper>
              </CardContent>
            </Card>
          </div>
        {:else}
          <div 
            in:fade={{ duration: 200 }}
          >
            <Card>
              <CardContent class="py-12 text-center text-muted-foreground">
                No chapters available for this video.
              </CardContent>
            </Card>
          </div>
        {/if}
  
        <!-- Stats -->
        {#if result.stats}
          <div 
            in:fade={{ duration: 300, delay: 300 }}
          >
            <Card>
              <CardHeader>
                <CardTitle class="flex items-center gap-2">
                  <BarChart3 class="h-5 w-5" />
                  Processing Statistics
                </CardTitle>
                <CardDescription>Analysis and processing metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <dl class="grid grid-cols-1 gap-4 sm:grid-cols-3">
                  <div class="rounded-lg border p-4">
                    <dt class="text-sm font-medium text-muted-foreground">Input Tokens</dt>
                    <dd class="mt-2 text-2xl font-semibold">
                      {formatNumber(result.stats.total_input_tokens)}
                    </dd>
                  </div>
                  <div class="rounded-lg border p-4">
                    <dt class="text-sm font-medium text-muted-foreground">Output Tokens</dt>
                    <dd class="mt-2 text-2xl font-semibold">
                      {formatNumber(result.stats.total_output_tokens)}
                    </dd>
                  </div>
                  <div class="rounded-lg border p-4">
                    <dt class="text-sm font-medium text-muted-foreground">Processing Cost</dt>
                    <dd class="mt-2 text-2xl font-semibold">
                      {formatPrice(result.stats.total_price)}
                    </dd>
                  </div>
                </dl>
              </CardContent>
            </Card>
  
            <div class="flex justify-center pt-4">
              <Button 
                variant="ghost" 
                class="text-sm text-muted-foreground"
                on:click={() => showAllText = !showAllText}
              >
                {showAllText ? 'Show Less' : 'Show All Text'}
                <ChevronDown class={`ml-2 h-4 w-4 transition-transform duration-200 ${showAllText ? 'rotate-180' : ''}`} />
              </Button>
            </div>
          </div>
        {/if}
  
        <!-- Full Text -->
        {#if showAllText}
          <div transition:slide={{ duration: 200 }}>
            <Card>
              <CardHeader>
                <CardTitle>Complete Text</CardTitle>
                <CardDescription>Full transcription organized by chapters</CardDescription>
              </CardHeader>
              <CardContent class="space-y-6">
                {#each result.chapters as chapter}
                  <div class="space-y-2">
                    <h3 class="font-semibold border-l-2 border-primary pl-3">
                      {chapter.title}
                    </h3>
                    <div class="space-y-4 pl-3">
                      {#each chapter.paragraphs as paragraph}
                        <p class="text-sm leading-relaxed">{paragraph}</p>
                      {/each}
                    </div>
                  </div>
                {/each}
              </CardContent>
            </Card>
          </div>
        {/if}
      </div>
    {/if}
  </div>