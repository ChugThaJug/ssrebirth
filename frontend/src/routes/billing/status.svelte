<script lang="ts">
    import { onMount } from 'svelte';
    import { getSubscriptionStatus } from '$lib/apiLAST';
    
    interface SubscriptionStatus {
        is_subscribed: boolean;
        plan: string;
        end_date: string | null;
    }
    
    let status: SubscriptionStatus | null = null;
    
    onMount(async () => {
        try {
            status = await getSubscriptionStatus();
        } catch (error) {
            console.error('Failed to fetch subscription status', error);
        }
    });
    </script>
    
    <h1>Subscription Status</h1>
    {#if status}
        <p>Subscribed: {status.is_subscribed}</p>
        <p>Plan: {status.plan}</p>
        <p>Ends at: {status.end_date || 'N/A'}</p>
    {:else}
        <p>Loading subscription status...</p>
    {/if}