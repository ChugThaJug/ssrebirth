<script lang="ts">
    import { createSubscription } from '$lib/apiLAST';
    
    let plan = 'basic';
    let error = '';
    
    async function handleSubscribe() {
      try {
        const result = await createSubscription(plan);
        if (result.checkout_url) {
          window.location.href = result.checkout_url;
        } else {
          error = 'Failed to create subscription. Please try again.';
        }
      } catch (err) {
        error = err instanceof Error ? err.message : 'An error occurred. Please try again.';
      }
    }
    </script>
    
    <h1>Choose a Subscription Plan</h1>
    <select bind:value={plan}>
      <option value="basic">Basic Plan</option>
      <option value="pro">Pro Plan</option>
    </select>
    <button on:click={handleSubscribe}>Subscribe</button>
    
    {#if error}
      <p class="error">{error}</p>
    {/if}