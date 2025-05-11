// src/routes/result/[videoId]/chapter-stepper.svelte
<script lang="ts">
  import { Stepper, StepperItem, StepperTitle, StepperDescription } from "$lib/components/ui/stepper";
  import { formatTime } from "$lib/utils/format";
  import type { Chapter } from "$lib/types/api";
  
  export let chapters: Chapter[];
  export let activeChapter = 0;
  
  function handleChapterClick(index: number) {
    activeChapter = index;
  }
</script>

<Stepper {activeChapter} class="w-full max-w-3xl mx-auto">
  {#each chapters as chapter, index (chapter.num_chapter)}
    <StepperItem
      step={index}
      on:click={() => handleChapterClick(index)}
      class="cursor-pointer"
    >
      <StepperTitle
        class={activeChapter === index ? "text-primary" : ""}
      >
        {chapter.title}
      </StepperTitle>
      <StepperDescription
        class={activeChapter === index ? "text-primary" : ""}
      >
        {formatTime(chapter.start_time)} - {formatTime(chapter.end_time)}
      </StepperDescription>
      
      {#if activeChapter === index}
        <div class="mt-4 space-y-4">
          {#each chapter.paragraphs as paragraph, pIndex}
            <div class="group relative">
              <p class="text-sm leading-relaxed pr-16">
                {paragraph}
              </p>
              <button
                class="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity text-xs text-muted-foreground hover:text-foreground"
                on:click={() => {
                  // Handle timestamp click - maybe scroll video to this time
                  const time = chapter.paragraph_timestamps[pIndex];
                }}
              >
                {formatTime(chapter.paragraph_timestamps[pIndex])}
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
      {/if}
    </StepperItem>
  {/each}
</Stepper>