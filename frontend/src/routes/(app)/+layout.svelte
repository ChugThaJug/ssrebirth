<!-- src/routes/(app)/+layout.svelte -->
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/firebase';
  import AppNav from '$lib/components/app-nav.svelte';
  import { Toaster } from 'svelte-sonner';
  
  let authChecked = false;
  let unsubscribe;
  
  onMount(() => {
    unsubscribe = user.subscribe(($user) => {
      authChecked = true;
      if (!$user && authChecked) {
        goto('/sign-in');
      }
    });
  });
  
  onDestroy(() => {
    if (unsubscribe) unsubscribe();
  });
</script>

{#if $user}
  <Toaster />
  <div class="min-h-screen bg-background flex flex-col">
    <AppNav />
    <main class="flex-1 p-4">
      <slot />
    </main>
  </div>
{:else if authChecked}
  <div class="flex h-screen items-center justify-center">
    <p>Redirecting to login...</p>
  </div>
{:else}
  <div class="flex h-screen items-center justify-center">
    <p>Loading...</p>
  </div>
{/if}