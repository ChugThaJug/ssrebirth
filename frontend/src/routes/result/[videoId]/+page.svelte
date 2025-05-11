<script lang="ts">
  import { cn } from "$lib/utils";
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
    BarChart3,
    PlayCircle,
    BookOpen,
    Info
  } from 'lucide-svelte';
  import { goto } from '$app/navigation';

  export let data: { videoId: string };
  
  let result: YouTubeResult | null = null;
  let error: string | null = null;
  let loading = true;
  let activeChapter = 0;
  let showAllText = false;
  let chapterContainerRef: HTMLDivElement;

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

  async function copyTimestamp(time: number, event: MouseEvent) {
    event.stopPropagation();
    try {
      await navigator.clipboard.writeText(formatTime(time));
      // Could add a toast notification here
    } catch (err) {
      console.error('Failed to copy timestamp:', err);
    }
  }

  function handleRetry() {
    fetchResult(data.videoId);
  }

  function handleChapterClick(index: number) {
    activeChapter = index;
    // Scroll the chapter into view on mobile
    if (window.innerWidth < 1024 && chapterContainerRef) {
      chapterContainerRef.scrollIntoView({ behavior: 'smooth' });
    }
  }

  function getTotalDuration(): string {
    if (!result?.chapters?.length) return '0:00';
    const lastChapter = result.chapters[result.chapters.length - 1];
    return formatTime(lastChapter.end_time);
  }
</script>

<svelte:head>
  <title>{result?.title || 'Video Result'} | Stepify</title>
  <meta name="description" content="Structured analysis and summary of the video content" />
</svelte:head>

<div class="container mx-auto px-4 py-8">
  {#if loading}
    <div 
      class="flex flex-col items-center justify-center min-h-[50vh]" 
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
    <div class="lg:grid lg:grid-cols-[1fr_300px] lg:gap-8" in:fade={{ duration: 200 }}>
      <div class="max-w-3xl space-y-8">
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
                    <div class="flex items-center gap-2 mt-2 text-white/80 text-sm">
                      <Clock class="h-4 w-4" />
                      <span>Total Duration: {getTotalDuration()}</span>
                      <span class="mx-2">•</span>
                      <BookOpen class="h-4 w-4" />
                      <span>{result.chapters.length} Chapters</span>
                    </div>
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
                        <PlayCircle class="h-4 w-4" />
                        Watch on YouTube
                      </Button>
                    </a>
                  </div>
                  {#if result.stats}
                    <div class="text-sm text-muted-foreground">
                      Processing cost: {formatPrice(result.stats.total_price)}
                    </div>
                  {/if}
                </div>
              </CardContent>
            </Card>
          </div>
        {/if}

        {#if result.chapters?.length > 0}
          <div 
            class="space-y-6" 
            in:fade={{ duration: 300, delay: 200 }}
            bind:this={chapterContainerRef}
          >
            <Card>
              <CardHeader>
                <CardTitle class="flex items-center gap-2">
                  <BookOpen class="h-5 w-5" />
                  Content Analysis
                </CardTitle>
                <CardDescription>
                  All chapters are expanded for easy viewing
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
                      
                      <div class="mt-1.5">
                        <div class="flex items-center gap-2 text-sm text-muted-foreground">
                          <Clock class="h-3 w-3" />
                          <span>{formatTime(chapter.start_time)} - {formatTime(chapter.end_time)}</span>
                        </div>
                      </div>

                      <div class="mt-6 rounded-lg bg-muted/50 p-4">
                        <div class="prose prose-sm max-w-none dark:prose-invert">
                          {#each chapter.paragraphs as paragraph, pIndex}
                            <div class="group relative mb-4 last:mb-0">
                              <p class="text-base leading-relaxed pr-16">
                                {paragraph}
                              </p>
                              <button
                                class="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity text-xs text-muted-foreground hover:text-foreground flex items-center gap-1 px-2 py-1 rounded-md hover:bg-muted"
                                on:click={(e) => copyTimestamp(chapter.paragraph_timestamps[pIndex], e)}
                              >
                                <Copy class="h-3 w-3" />
                                {formatTime(chapter.paragraph_timestamps[pIndex])}
                              </button>
                            </div>
                          {/each}
                        </div>

                        {#if chapter.screenshots?.length}
                          <div class="mt-8 grid grid-cols-2 gap-4">
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
                    </StepperItem>
                  {/each}
                </Stepper>
              </CardContent>
            </Card>
          </div>
        {:else}
          <div in:fade={{ duration: 200 }}>
            <Card>
              <CardContent class="py-12 text-center text-muted-foreground">
                <Info class="h-12 w-12 mx-auto mb-4 text-muted-foreground/50" />
                <p>No chapters available for this video.</p>
              </CardContent>
            </Card>
          </div>
        {/if}

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

        {#if showAllText}
          <div transition:slide={{ duration: 200 }}>
            <Card>
              <CardHeader>
                <CardTitle>Complete Transcription</CardTitle>
                <CardDescription>Full content organized by chapters</CardDescription>
              </CardHeader>
              <CardContent class="space-y-8">
                {#each result.chapters as chapter}
                  <div class="space-y-4">
                    <div class="border-l-2 border-primary pl-4">
                      <h3 class="font-semibold">
                        {chapter.title}
                      </h3>
                      <div class="flex items-center gap-2 mt-1 text-sm text-muted-foreground">
                        <Clock class="h-3 w-3" />
                        <span>{formatTime(chapter.start_time)} - {formatTime(chapter.end_time)}</span>
                      </div>
                    </div>
                    <div class="space-y-4 pl-4">
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

      <div class="hidden lg:block">
        <div class="sticky top-8 space-y-6">
          {#if result.chapters?.length > 0}
            <Card>
              <CardHeader class="pb-3">
                <CardTitle class="text-sm font-medium">
                  On this page
                </CardTitle>
              </CardHeader>
              <CardContent class="space-y-1">
                {#each result.chapters as chapter, i}
                  <button
                    class={cn(
                      "flex flex-col w-full text-left px-3 py-2 text-sm transition-colors rounded-md hover:bg-muted/50",
                      activeChapter === i && "bg-muted"
                    )}
                    on:click={() => handleChapterClick(i)}
                  >
                    <span class={cn(
                      "line-clamp-1 font-medium",
                      activeChapter === i && "text-primary"
                    )}>
                      {chapter.title}
                    </span>
                    <span class="flex items-center gap-1 text-xs text-muted-foreground mt-0.5">
                      <Clock class="h-3 w-3" />
                      {formatTime(chapter.start_time)}
                    </span>
                  </button>
                {/each}
              </CardContent>
            </Card>
          {/if}

          {#if result.stats}
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm flex items-center gap-2">
                  <BarChart3 class="h-4 w-4" />
                  Processing Statistics
                </CardTitle>
              </CardHeader>
              <CardContent class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-muted-foreground">Input Tokens</span>
                  <span class="font-medium">{formatNumber(result.stats.total_input_tokens)}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-muted-foreground">Output Tokens</span>
                  <span class="font-medium">{formatNumber(result.stats.total_output_tokens)}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-muted-foreground">Total Tokens</span>
                  <span class="font-medium">
                    {formatNumber(result.stats.total_input_tokens + result.stats.total_output_tokens)}
                  </span>
                </div>
                <div class="pt-2 mt-2 border-t">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium">Processing Cost</span>
                    <span class="font-semibold text-primary">
                      {formatPrice(result.stats.total_price)}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div class="lg:hidden mt-8">
              <Card>
                <CardHeader>
                  <CardTitle class="flex items-center gap-2">
                    <BarChart3 class="h-5 w-5" />
                    Processing Statistics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <dl class="grid grid-cols-2 gap-4">
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
                    <div class="rounded-lg border p-4 col-span-2">
                      <dt class="text-sm font-medium text-muted-foreground">Processing Cost</dt>
                      <dd class="mt-2 text-2xl font-semibold text-primary">
                        {formatPrice(result.stats.total_price)}
                      </dd>
                    </div>
                  </dl>
                </CardContent>
              </Card>
            </div>
          {/if}

          <Card>
            <CardHeader class="pb-3">
              <CardTitle class="text-sm">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent class="space-y-2">
              <Button 
                variant="outline" 
                class="w-full justify-start text-sm"
                href="/"
              >
                <RefreshCw class="h-4 w-4 mr-2" />
                Process New Video
              </Button>
              <a 
                href={`https://youtube.com/watch?v=${result.video_id}`}
                target="_blank"
                rel="noopener noreferrer"
                class="w-full"
              >
                <Button 
                  variant="outline"
                  class="w-full justify-start text-sm"
                >
                  <PlayCircle class="h-4 w-4 mr-2" />
                  Watch on YouTube
                </Button>
              </a>
              <Button 
                variant="outline"
                class="w-full justify-start text-sm"
                on:click={() => showAllText = !showAllText}
              >
                <FileText class="h-4 w-4 mr-2" />
                {showAllText ? 'Hide Full Text' : 'Show Full Text'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  {/if}
</div>

<style lang="postcss">
:global(.prose) {
  max-width: none;
}

:global(.prose p) {
  margin: 0;
}

:global(.dark .prose) {
  color: var(--foreground);
}

:global(.prose p + p) {
  margin-top: 1em;
}

@media (max-width: 640px) {
  :global(.prose) {
    font-size: 0.9375rem;
  }
}

:global(html) {
  scroll-behavior: smooth;
}
</style>