<script lang="ts">
  import { onMount } from "svelte";
  import { getVideoResult, updateVideoSummary, updateVideoTranscript } from "$lib/api";
  import { Button } from "$lib/components/ui/button";
  import TiptapEditor from "$lib/components/TipTapEditor.svelte";

  export let data: { id: string };
  
  let videoResult: any = null;
  let error: string | null = null;
  let summaryEditMode = false;
  let transcriptEditMode = false;
  let tempSummary = "";
  let tempTranscript = "";
  
  onMount(async () => {
    try {
      if (data && data.id) {
        console.log(`Fetching video with ID: ${data.id}`);
        videoResult = await getVideoResult(data.id);
        console.log('Received video result:', videoResult);
        tempSummary = videoResult.summary;
        tempTranscript = videoResult.paragraphs;
      } else {
        throw new Error("Video ID is missing");
      }
    } catch (err) {
      console.error("Error fetching video result:", err);
      error = err instanceof Error ? err.message : "An error occurred while fetching the result";
    }
  });

  function formatContent(content: string) {
    return content.split('\n').map(line => `<p>${line}</p>`).join('');
  }

  async function handleSummaryUpdate(newSummary: string) {
    tempSummary = newSummary;
  }

  async function handleTranscriptUpdate(newTranscript: string) {
    tempTranscript = newTranscript;
  }

  async function saveSummary() {
    try {
      await updateVideoSummary(data.id, tempSummary);
      videoResult.summary = tempSummary;
      summaryEditMode = false;
    } catch (err) {
      console.error("Error updating summary:", err);
      error = err instanceof Error ? err.message : "An error occurred while updating the summary";
    }
  }

  async function saveTranscript() {
    try {
      await updateVideoTranscript(data.id, tempTranscript);
      videoResult.paragraphs = tempTranscript;
      transcriptEditMode = false;
    } catch (err) {
      console.error("Error updating transcript:", err);
      error = err instanceof Error ? err.message : "An error occurred while updating the transcript";
    }
  }

  function toggleSummaryEditMode() {
    summaryEditMode = !summaryEditMode;
    if (!summaryEditMode) {
      saveSummary();
    }
  }

  function toggleTranscriptEditMode() {
    transcriptEditMode = !transcriptEditMode;
    if (!transcriptEditMode) {
      saveTranscript();
    }
  }
</script>

<svelte:head>
  <title>{videoResult ? videoResult.title : 'Loading...'} | Stepify</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
  {#if error}
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline">{error}</span>
    </div>
  {:else if videoResult}
    <h1 class="text-3xl font-bold mb-4">{videoResult.title}</h1>
    <p class="mb-4">Video ID: {videoResult.youtube_id}</p>
    
    <div class="mb-8">
      <h2 class="text-2xl font-semibold mb-2">Summary</h2>
      <div class="flex justify-between items-center mb-2">
        <p class="text-sm text-gray-600">Click to edit the summary</p>
        <Button on:click={toggleSummaryEditMode}>
          {summaryEditMode ? 'Save' : 'Edit'}
        </Button>
      </div>
      {#if summaryEditMode}
        <TiptapEditor content={tempSummary} onUpdate={handleSummaryUpdate} />
      {:else}
        <div class="prose max-w-none">
          {@html formatContent(videoResult.summary)}
        </div>
      {/if}
    </div>
    
    <div>
      <h2 class="text-2xl font-semibold mb-2">Transcript</h2>
      <div class="flex justify-between items-center mb-2">
        <p class="text-sm text-gray-600">Click to edit the transcript</p>
        <Button on:click={toggleTranscriptEditMode}>
          {transcriptEditMode ? 'Save' : 'Edit'}
        </Button>
      </div>
      {#if transcriptEditMode}
        <TiptapEditor content={tempTranscript} onUpdate={handleTranscriptUpdate} />
      {:else}
        <div class="prose max-w-none">
          {@html formatContent(videoResult.paragraphs)}
        </div>
      {/if}
    </div>
  {:else}
    <p>Loading...</p>
  {/if}
</div>