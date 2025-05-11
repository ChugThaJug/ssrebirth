<!-- src/routes/(auth)/sign-in/+page.svelte -->
<script lang="ts">
  import { signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
  import { auth } from '$lib/firebase';
  import { goto } from '$app/navigation';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import * as Card from '$lib/components/ui/card';
  import { toast } from 'svelte-sonner';

  let email = '';
  let password = '';
  let loading = false;

  async function handleEmailSignIn() {
    try {
      loading = true;
      await signInWithEmailAndPassword(auth, email, password);
      toast.success('Signed in successfully');
      goto('/dashboard');
    } catch (error) {
      console.error('Sign in error:', error);
      toast.error(error.message || 'Failed to sign in');
    } finally {
      loading = false;
    }
  }

  async function handleGoogleSignIn() {
    try {
      loading = true;
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      toast.success('Signed in with Google successfully');
      goto('/dashboard');
    } catch (error) {
      console.error('Google sign in error:', error);
      toast.error(error.message || 'Failed to sign in with Google');
    } finally {
      loading = false;
    }
  }
</script>

<div class="flex min-h-screen items-center justify-center">
  <Card.Root class="w-full max-w-md">
    <Card.Header class="space-y-1">
      <Card.Title class="text-2xl font-bold tracking-tight">Sign in</Card.Title>
      <Card.Description>
        Enter your email and password to sign in to your account
      </Card.Description>
    </Card.Header>
    <Card.Content>
      <div class="grid gap-4">
        <Button 
          variant="outline" 
          class="w-full" 
          onclick={handleGoogleSignIn} 
          disabled={loading}
        >
          <svg class="mr-2 h-4 w-4" viewBox="0 0 24 24">
            <path
              d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
              fill="currentColor"
            />
          </svg>
          Sign in with Google
        </Button>
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <span class="w-full border-t"></span>
          </div>
          <div class="relative flex justify-center text-xs uppercase">
            <span class="bg-background px-2 text-muted-foreground">Or continue with</span>
          </div>
        </div>
        <div class="grid gap-2">
          <label for="email" class="text-sm font-medium leading-none">
            Email
          </label>
          <Input 
            id="email" 
            type="email" 
            bind:value={email} 
            placeholder="m@example.com" 
            required
          />
        </div>
        <div class="grid gap-2">
          <div class="flex items-center justify-between">
            <label for="password" class="text-sm font-medium leading-none">
              Password
            </label>
            <a href="/forgot-password" class="text-sm underline underline-offset-4">
              Forgot password?
            </a>
          </div>
          <Input 
            id="password" 
            type="password" 
            bind:value={password} 
            required
          />
        </div>
        <Button onclick={handleEmailSignIn} disabled={loading} class="w-full">
          {loading ? 'Signing in...' : 'Sign in'}
        </Button>
      </div>
      <div class="mt-4 text-center text-sm">
        Don't have an account?{' '}
        <a href="/sign-up" class="underline underline-offset-4">
          Sign up
        </a>
      </div>
    </Card.Content>
  </Card.Root>
</div>