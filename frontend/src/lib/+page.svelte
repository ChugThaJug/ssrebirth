<script lang="ts">
  import { fade } from 'svelte/transition';
  import { 
    processVideo, 
    ProcessingMode, 
    ChapterSource
  } from '$lib/services/api';
  import { getVideoId } from '$lib/utils/youtube';
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { 
    Select,
    SelectContent, 
    SelectItem, 
    SelectTrigger, 
    SelectValue 
  } from "$lib/components/ui/select";
  import { goto } from '$app/navigation';

  let videoUrl = "";
  let error = "";
  let loading = false;

  // Initialize with string values that match the enum values
  let selectedMode = "detailed";
  let selectedChapterSource = "auto";

  async function handleSubmit() {
    if (!videoUrl) {
      error = "Please enter a YouTube URL";
      return;
    }

    const videoId = getVideoId(videoUrl);
    if (!videoId) {
      error = "Invalid YouTube URL";
      return;
    }

    loading = true;
    error = "";

    try {
      // Send the string values directly
      const result = await processVideo(videoId, selectedMode, selectedChapterSource);
      await goto(`/process/${result.job_id}`);
    } catch (err) {
      error = err instanceof Error ? err.message : "An error occurred";
    } finally {
      loading = false;
    }
  }

  // Helper function to format display text
  function formatDisplayText(text: string): string {
    return text.toLowerCase().replace(/_/g, ' ');
  }

  // Define options for the select components
  const modeOptions = [
    { value: "simple", label: "Simple" },
    { value: "detailed", label: "Detailed" },
    { value: "detailed_with_screenshots", label: "Detailed with Screenshots" }
  ];

  const sourceOptions = [
    { value: "auto", label: "Auto-generated" },
    { value: "description", label: "From Description" }
  ];

  // Helper function to get description text
  function getModeDescription(mode: string): string {
    switch (mode) {
      case 'simple':
        return 'Quick processing with basic structuring';
      case 'detailed':
        return 'Detailed analysis with better organization';
      case 'detailed_with_screenshots':
        return 'Comprehensive analysis with visual aids';
      default:
        return '';
    }
  }
</script>

<svelte:head>
  <title>Stepify - YouTube Video Processing</title>
  <meta name="description" content="Process YouTube videos and get structured content with AI-powered analysis" />
</svelte:head>

<div class="container mx-auto px-4 py-8 max-w-2xl" in:fade>
  <div class="text-center mb-8">
    <h1 class="text-4xl font-bold tracking-tight mb-4">
      Process YouTube Videos
    </h1>
    <p class="text-lg text-muted-foreground">
      Convert any YouTube video into well-structured, readable content with AI-powered analysis.
    </p>
  </div>

  <div class="bg-card border rounded-lg p-6 shadow-sm">
    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      <div class="space-y-2">
        <label for="videoUrl" class="block text-sm font-medium">
          YouTube URL <span class="text-destructive">*</span>
        </label>
        <Input 
          type="url" 
          id="videoUrl"
          name="videoUrl"
          bind:value={videoUrl}
          placeholder="https://www.youtube.com/watch?v=..."
          required
          aria-describedby={error ? "url-error" : undefined}
          class="h-12"
        />
        {#if error}
          <div 
            id="url-error" 
            class="bg-destructive/15 text-destructive text-sm p-3 rounded-md" 
            role="alert"
            transition:fade
          >
            {error}
          </div>
        {/if}
      </div>

      <div class="grid gap-6 sm:grid-cols-2">
        <div class="space-y-2">
          <label for="processingMode" class="block text-sm font-medium">
            Processing Mode
          </label>
          <Select 
            defaultValue={selectedMode}
            onValueChange={(value) => selectedMode = value}
          >
            <SelectTrigger class="h-12">
              <SelectValue placeholder="Select mode">
                {formatDisplayText(selectedMode)}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              {#each modeOptions as option}
                <SelectItem value={option.value}>
                  {option.label}
                </SelectItem>
              {/each}
            </SelectContent>
          </Select>
          <p class="text-xs text-muted-foreground">
            {getModeDescription(selectedMode)}
          </p>
        </div>

        <div class="space-y-2">
          <label for="chapterSource" class="block text-sm font-medium">
            Chapter Source
          </label>
          <Select 
            defaultValue={selectedChapterSource}
            onValueChange={(value) => selectedChapterSource = value}
          >
            <SelectTrigger class="h-12">
              <SelectValue placeholder="Select source">
                {selectedChapterSource === 'auto' ? 'Auto-generated' : 'From Description'}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              {#each sourceOptions as option}
                <SelectItem value={option.value}>
                  {option.label}
                </SelectItem>
              {/each}
            </SelectContent>
          </Select>
          <p class="text-xs text-muted-foreground">
            {selectedChapterSource === 'auto' 
              ? 'AI-generated chapters based on content'
              : 'Use chapters from video description'}
          </p>
        </div>
      </div>

      <Button 
        type="submit" 
        disabled={loading} 
        class="w-full h-12"
        variant="default"
      >
        {#if loading}
          <div class="animate-spin mr-2 h-4 w-4 border-2 border-current border-t-transparent rounded-full" />
          Processing...
        {:else}
          Process Video
        {/if}
      </Button>
    </form>
  </div>

  <div class="mt-6 space-y-4 text-sm text-muted-foreground">
    <div class="bg-muted/50 rounded-lg p-4">
      <h2 class="font-medium mb-2">Processing Information</h2>
      <ul class="list-disc list-inside space-y-1">
        <li>Processing time varies based on video length and selected mode</li>
        <li>Simple mode is fastest but provides basic structure</li>
        <li>Detailed mode provides better organization and summaries</li>
        <li>Screenshots are only available in detailed mode with screenshots</li>
      </ul>
    </div>
  </div>
</div>