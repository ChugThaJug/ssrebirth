<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fade } from 'svelte/transition';
  import { getProcessingStatus } from '$lib/services/api';
  import type { YouTubeProcessingStatus } from '$lib/services/api';
  import { Progress } from "$lib/components/ui/progress";
  import { Button } from "$lib/components/ui/button";
  import { 
    Card, 
    CardContent, 
    CardHeader, 
    CardTitle 
  } from "$lib/components/ui/card";
  import { goto } from '$app/navigation';

  export let data: { jobId: string };

  let status: YouTubeProcessingStatus | null = null;
  let error: string | null = null;
  let intervalId: number;

  async function checkStatus() {
    if (!data.jobId) {
      error = "No job ID provided";
      return;
    }

    try {
      status = await getProcessingStatus(data.jobId);
      
      if (status.error) {
        error = status.error;
        clearInterval(intervalId);
      } else if (status.status === 'completed') {
        clearInterval(intervalId);
        if (!status.video_id) {
          throw new Error("No video ID in response");
        }
        await goto(`/result/${status.video_id}`);
      } else if (status.status === 'failed') {
        error = status.error || "Processing failed";
        clearInterval(intervalId);
      }
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to fetch status";
      clearInterval(intervalId);
    }
  }

  onMount(() => {
    checkStatus();
    intervalId = setInterval(checkStatus, 5000);
  });

  onDestroy(() => {
    if (intervalId) clearInterval(intervalId);
  });

  $: progressPercentage = status ? Math.round(status.progress * 100) : 0;
  
  function getStatusMessage(status: YouTubeProcessingStatus): string {
    const messages = {
      downloading: 'Downloading video content...',
      processing: 'Processing and analyzing content...',
      analyzing: 'Performing deep content analysis...',
      generating: 'Generating structured content...',
      completed: 'Processing complete!',
      failed: 'Processing failed',
      pending: 'Waiting to begin processing...'
    };
    return messages[status.status as keyof typeof messages] || `Status: ${status.status}`;
  }
</script>

<svelte:head>
  <title>Processing Video | Stepify</title>
</svelte:head>

<div class="container mx-auto px-4 py-8 max-w-2xl" in:fade>
  <div class="mb-6 flex items-center justify-between">
    <h1 class="text-3xl font-bold">Processing Video</h1>
    <Button variant="outline" href="/" size="sm">New Video</Button>
  </div>

  {#if error}
    <div 
      class="bg-destructive/15 text-destructive px-4 py-3 rounded-lg" 
      role="alert"
      transition:fade
    >
      <h2 class="font-medium">Processing Error</h2>
      <p class="text-sm mt-1">{error}</p>
      <div class="mt-4 flex gap-2">
        <Button variant="outline" href="/">Start Over</Button>
        <Button variant="outline" on:click={checkStatus}>Retry</Button>
      </div>
    </div>
  {:else if status}
    <div class="space-y-6" transition:fade>
      <Card>
        <CardHeader>
          <CardTitle>{getStatusMessage(status)}</CardTitle>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <Progress value={progressPercentage} />
            <div class="flex justify-between text-sm">
              <span class="text-muted-foreground">Progress</span>
              <span class="font-medium">{progressPercentage}%</span>
            </div>
          </div>
        </CardContent>
      </Card>

      <div class="bg-muted/50 rounded-lg p-4">
        <div class="space-y-3">
          <div>
            <h3 class="text-sm font-medium">Processing Details</h3>
            <dl class="mt-2 grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt class="text-muted-foreground">Job ID</dt>
                <dd class="font-mono mt-1">{status.job_id}</dd>
              </div>
              {#if status.video_id}
                <div>
                  <dt class="text-muted-foreground">Video ID</dt>
                  <dd class="font-mono mt-1">{status.video_id}</dd>
                </div>
              {/if}
            </dl>
          </div>
        </div>
      </div>

      <p class="text-sm text-muted-foreground">
        Please keep this page open while we process your video. 
        You'll be automatically redirected when processing is complete.
      </p>
    </div>
  {:else}
    <div class="flex flex-col items-center justify-center py-12" transition:fade>
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-foreground"></div>
      <p class="mt-4 text-sm text-muted-foreground">Initializing process...</p>
    </div>
  {/if}
</div>