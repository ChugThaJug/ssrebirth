<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { loginWithOAuth } from '$lib/apiLAST';
  import { Button } from "$lib/components/ui/button";
  
  let error = '';
  
  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    if (code) {
      handleOAuthLogin('google', code);
    }
  });
  
  function initiateOAuthLogin() {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    const redirectUri = import.meta.env.VITE_GOOGLE_REDIRECT_URI;
    
    if (!clientId || !redirectUri) {
      console.error('Google OAuth credentials are not properly configured');
      error = 'OAuth configuration error. Please check the console for details.';
      return;
    }
  
    const scope = 'openid profile email';
    
    const googleAuthUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
    googleAuthUrl.searchParams.append('client_id', clientId);
    googleAuthUrl.searchParams.append('redirect_uri', redirectUri);
    googleAuthUrl.searchParams.append('response_type', 'code');
    googleAuthUrl.searchParams.append('scope', scope);
    googleAuthUrl.searchParams.append('access_type', 'offline');
    googleAuthUrl.searchParams.append('prompt', 'consent');
  
    window.location.href = googleAuthUrl.toString();
  }
  
    async function handleOAuthLogin(provider: string, code: string) {
    try {
      console.log(`Attempting to login with provider: ${provider}, code: ${code}`);
      const result = await loginWithOAuth(provider, code);
      console.log("Login successful", result);
      goto('/dashboard');
    } catch (err) {
      console.error("Login failed", err);
      if (err instanceof Error) {
        error = err.message;
        console.error("Error details:", err);
      } else {
        error = 'An unknown error occurred during login';
        console.error("Unknown error:", err);
      }
    }
  }
  
  </script>
  
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    {#if error}
      <p class="text-red-500 mb-4">{error}</p>
    {/if}
    <Button on:click={initiateOAuthLogin}>Login with Google</Button>
  </div>