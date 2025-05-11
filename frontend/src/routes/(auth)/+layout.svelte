<!-- src/routes/(auth)/+layout.svelte -->
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { user } from '$lib/firebase';
  
  let authChecked = false;
  let unsubscribe;
  
  onMount(() => {
    unsubscribe = user.subscribe(($user) => {
      authChecked = true;
      if ($user && authChecked) {
        goto('/dashboard');  // Redirect to dashboard if already logged in
      }
    });
  });
  
  onDestroy(() => {
    if (unsubscribe) unsubscribe();
  });
</script>

{#if !$user && authChecked}
  <div class="flex min-h-screen items-center justify-center bg-background">
    <slot />
  </div>
{:else if $user && authChecked}
  <div class="flex h-screen items-center justify-center">
    <p>Redirecting to dashboard...</p>
  </div>
{:else}
  <div class="flex h-screen items-center justify-center">
    <p>Loading...</p>
  </div>
{/if}