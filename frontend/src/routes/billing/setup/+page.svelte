<script lang="ts">
    import { setupBilling } from '$lib/apiLAST';
    import { goto } from '$app/navigation';
    
    let error = '';
    
    async function handleSetupBilling() {
      try {
        await setupBilling();
        goto('/billing/subscribe');
      } catch (err) {
        error = err instanceof Error ? err.message : 'An error occurred during billing setup';
      }
    }
    </script>
    
    <h1>Setup Billing</h1>
    <button on:click={handleSetupBilling}>Setup Billing</button>
    
    {#if error}
      <p class="error">{error}</p>
    {/if}