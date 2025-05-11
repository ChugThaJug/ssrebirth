<script lang="ts">
  import { setContext } from 'svelte';
  import { writable, type Writable } from 'svelte/store';
  import { cn } from "$lib/utils";
  
  export let activeStep = 0;
  export let orientation: 'horizontal' | 'vertical' = 'vertical';
  let className: string | undefined = undefined;
  export { className as class };

  const stepCount: Writable<number> = writable(0);
  const currentStep: Writable<number> = writable(activeStep);

  // Keep currentStep in sync with activeStep prop
  $: {
    currentStep.set(activeStep);
  }

  const stepperContext = {
    currentStep,
    stepCount,
    registerStep: (index: number) => {
      stepCount.update(count => count + 1);
      return index;
    },
    updateCurrentStep: (step: number) => {
      currentStep.set(step);
      activeStep = step;
    }
  };

  setContext('stepper', stepperContext);
</script>

<div 
  class={cn(
    "relative", 
    orientation === "vertical" ? "space-y-4" : "flex space-x-4",
    className
  )} 
  {...$$restProps}
>
  <slot />
</div>