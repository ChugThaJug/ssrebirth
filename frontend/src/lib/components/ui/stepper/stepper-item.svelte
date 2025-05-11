<script lang="ts">
  import { getContext } from 'svelte';
  import type { Writable } from 'svelte/store';
  import { Button } from "$lib/components/ui/button";
  import { Check, Circle, ChevronRight } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import type { StepperContext } from './types';
  
  export let step: number;
  let className: string | undefined = undefined;
  export { className as class };
  
  const { currentStep, registerStep } = getContext<StepperContext>('stepper');
  const index = registerStep(step);
  
  $: state = $currentStep === step ? 'active' : 
            $currentStep > step ? 'completed' : 'inactive';
</script>

<div 
  class={cn(
    "relative",
    className
  )}
  data-state={state}
>
  <div class="flex items-start mb-4">
    <div class="flex items-center relative">
      <Button
        variant={state === 'completed' || state === 'active' ? "default" : "outline"}
        size="icon"
        class={cn(
          "z-10 rounded-full size-8",
          state === 'active' && "ring-2 ring-ring ring-offset-2 ring-offset-background"
        )}
        on:click
      >
        {#if state === 'completed'}
          <Check class="h-4 w-4" />
        {:else if state === 'active'}
          <Circle class="h-4 w-4" />
        {:else}
          <ChevronRight class="h-4 w-4" />
        {/if}
      </Button>
      {#if step !== 0}
        <div 
          class={cn(
            "absolute left-[15px] -top-[32px] w-[2px] h-[32px] bg-muted/50",
            state === 'completed' && "bg-primary"
          )} 
        />
      {/if}
    </div>
    <div class="ml-4 min-w-0 flex-1">
      <slot />
    </div>
  </div>
</div>