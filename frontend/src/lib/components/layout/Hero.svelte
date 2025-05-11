<!-- home page -->

<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "$lib/components/ui/select";
  import { processContent } from "$lib/apiLAST";
  import { Search } from "lucide-svelte";
  
  let youtubeUrl = "";
  let processingMode = "simple";
  let error = "";
  let loading = false;
  
  async function handleSubmit() {
    if (!youtubeUrl) {
      error = "Please enter a YouTube URL";
      return;
    }
    
    loading = true;
    error = "";
    
    try {
      const result = await processContent(youtubeUrl, processingMode);
      window.location.href = `/result/${result.content_id}`;
    } catch (err: any) {
      error = err.message || "An error occurred while processing the content";
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
<title>Stepify YouTube videos for the sake of your time</title>
</svelte:head>

<div class="container relative">
<section class="mx-auto flex max-w-[980px] flex-col items-center gap-2 py-8 md:py-12 md:pb-8 lg:py-24 lg:pb-20">
  <h1 class="text-center text-7xl font-bold leading-tight tracking-tighter md:text-6xl lg:leading-[1.1]">Stepify YouTube videos <br>for the sake of your time</h1>
  <p class="max-w-[750px] text-center text-lg sm:text-xl text-balance text-muted-foreground">
    No time for YouTube videos? Get a step-by-step tutorial of any video to follow along. Pure transcript. Powered by AI.
  </p>

  <div class="relative w-full max-w-[600px] mt-8">
    {#if error}
      <div class="bg-destructive/15 text-destructive px-4 py-3 rounded-md mb-4" role="alert">
        <span class="block sm:inline">{error}</span>
      </div>
    {/if}
    
    <form on:submit|preventDefault={handleSubmit} class="flex items-center space-x-2">
      <div class="relative flex-grow">
        <Input 
          type="url" 
          bind:value={youtubeUrl} 
          placeholder="Enter YouTube URL" 
          required
          class="pr-24" 
        />
        <div class="absolute right-2 top-1/2 -translate-y-1/2">
          <Select bind:value={processingMode}>
            <SelectTrigger class="h-8 w-20">
              <SelectValue placeholder="Mode" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="simple">Simple</SelectItem>
              <SelectItem value="detailed">Detailed</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      <Button type="submit" disabled={loading} class="h-10 px-4">
        {#if loading}
          <span class="loading loading-spinner loading-sm"></span>
        {:else}
          <Search class="h-4 w-4" />
        {/if}
      </Button>
    </form>
  </div>

  <div class="flex w-full items-center justify-center space-x-4 py-4 md:pb-10">
    <a href="/docs" class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground shadow hover:bg-primary/90 h-9 px-4 py-2">
      Stepified videos
    </a>
    <a href="https://github.com/yourusername/your-repo" target="_blank" rel="noreferrer" class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2">
      Search database
    </a>
  </div>
</section>
</div>