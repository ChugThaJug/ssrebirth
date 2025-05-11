<script lang="ts">
import { createSubscription } from '$lib/apiLAST';

let plan = 'basic';

async function handleSubscribe() {
    try {
        const result = await createSubscription(plan);
        window.location.href = result.checkout_url;
    } catch (error) {
        console.error('Subscription creation failed', error);
    }
}
</script>

<h1>Choose a Subscription Plan</h1>
<select bind:value={plan}>
    <option value="basic">Basic Plan</option>
    <option value="pro">Pro Plan</option>
</select>
<button on:click={handleSubscribe}>Subscribe</button>

