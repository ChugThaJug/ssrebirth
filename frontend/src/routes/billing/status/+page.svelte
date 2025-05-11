<script lang="ts">
    import { onMount } from 'svelte';
    import { getSubscriptionStatus } from '$lib/apiLAST';
    
    let status = null;
    
    onMount(async () => {
        try {
            status = await getSubscriptionStatus();
        } catch (error) {
            console.error('Failed to fetch subscription status', error);
        }
    });
    </script>
    
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-2xl font-bold mb-4">Subscription Status</h1>
      {#if status}
        <p>Subscribed: {status.is_subscribed}</p>
        <p>Plan: {status.plan}</p>
        <p>Ends at: {status.end_date || 'N/A'}</p>
      {:else}
        <p>Loading subscription status...</p>
      {/if}
    </div>