<script lang="ts">
  import type { Chapter } from "$lib/types/api";
  import { formatTime } from "$lib/utils/format";
  import { cn } from "$lib/utils";
  import { Clock } from "lucide-svelte";

  export let chapters: Chapter[];
  export let activeChapter: number;
  export let onChapterClick: (index: number) => void;
</script>

<div class="w-full">
  <div class="space-y-1">
    <h3 class="font-medium">On this page</h3>
    <p class="text-sm text-muted-foreground">
      {chapters.length} chapter{chapters.length === 1 ? '' : 's'}
    </p>
  </div>
  <div class="mt-4 space-y-1">
    {#each chapters as chapter, index}
      <button
        class={cn(
          "flex flex-col w-full text-left px-3 py-2 text-sm transition-colors rounded-md hover:bg-muted/50",
          activeChapter === index && "bg-muted"
        )}
        on:click={() => onChapterClick(index)}
      >
        <span class={cn(
          "line-clamp-1 font-medium",
          activeChapter === index && "text-primary"
        )}>
          {chapter.title}
        </span>
        <span class="flex items-center gap-1 text-xs text-muted-foreground mt-0.5">
          <Clock class="h-3 w-3" />
          {formatTime(chapter.start_time)}
        </span>
      </button>
    {/each}
  </div>
</div>