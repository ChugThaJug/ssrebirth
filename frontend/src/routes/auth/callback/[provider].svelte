<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { loginWithOAuth } from '$lib/apiLAST';
    
    export let params: { provider: string };
    
    onMount(async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        if (code) {
            try {
                const result = await loginWithOAuth(params.provider, code);
                // Token is already stored in localStorage by the loginWithOAuth function
                goto('/dashboard');
            } catch (error) {
                console.error('OAuth login failed', error);
                goto('/login?error=oauth_failed');
            }
        } else {
            goto('/login?error=no_code');
        }
    });
    </script>
    
    <div>Processing OAuth login...</div>