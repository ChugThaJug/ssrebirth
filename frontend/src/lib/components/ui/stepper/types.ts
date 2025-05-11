// src/lib/components/ui/stepper/types.ts
import type { Writable } from 'svelte/store';

export type StepperContext = {
  currentStep: Writable<number>;
  stepCount: Writable<number>;
  registerStep: (index: number) => number;
  updateCurrentStep: (step: number) => void;
};