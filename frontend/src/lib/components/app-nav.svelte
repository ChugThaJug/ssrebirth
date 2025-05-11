<!-- src/lib/components/app-nav.svelte -->
<script lang="ts">
  import { auth, user } from '$lib/firebase';
  import { signOut } from 'firebase/auth';
  import { goto } from '$app/navigation';
  import { Button } from '$lib/components/ui/button';
  import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
  import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';
  
  async function handleSignOut() {
    try {
      await signOut(auth);
      goto('/');
    } catch (error) {
      console.error('Sign out error:', error);
    }
  }
  
  function getInitials(name) {
    if (!name) return '';
    return name.split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase();
  }
</script>

<header class="border-b">
  <div class="container mx-auto flex h-16 items-center justify-between px-4">
    <div class="flex items-center gap-6">
      <a href="/" class="flex items-center gap-2 font-semibold">
        <img src="/logo.svg" alt="Logo" class="h-8 w-8" />
        <span>VideoProcessor</span>
      </a>
      <nav class="hidden md:flex">
        <ul class="flex gap-6">
          <li><a href="/dashboard" class="text-sm font-medium">Dashboard</a></li>
          <li><a href="/process" class="text-sm font-medium">Process Video</a></li>
        </ul>
      </nav>
    </div>
    
    <div class="flex items-center gap-4">
      {#if $user}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild let:builder>
            <Button 
              variant="ghost" 
              class="relative h-8 w-8 rounded-full"
              builders={[builder]}
            >
              <Avatar class="h-8 w-8">
                {#if $user.photoURL}
                  <AvatarImage src={$user.photoURL} alt={$user.displayName || ''} />
                {/if}
                <AvatarFallback>{getInitials($user.displayName || $user.email)}</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenu.Trigger>
          <DropdownMenu.Content class="w-56" align="end" forceMount>
            <DropdownMenu.Label class="font-normal">
              <div class="flex flex-col space-y-1">
                <p class="text-sm font-medium leading-none">{$user.displayName || 'User'}</p>
                <p class="text-xs leading-none text-muted-foreground">{$user.email}</p>
              </div>
            </DropdownMenu.Label>
            <DropdownMenu.Separator />
            <DropdownMenu.Group>
              <DropdownMenu.Item>
                <a href="/account" class="flex w-full">Account</a>
              </DropdownMenu.Item>
              <DropdownMenu.Item>
                <a href="/dashboard" class="flex w-full">Dashboard</a>
              </DropdownMenu.Item>
            </DropdownMenu.Group>
            <DropdownMenu.Separator />
            <DropdownMenu.Item onclick={handleSignOut}>
              Log out
            </DropdownMenu.Item>
          </DropdownMenu.Content>
        </DropdownMenu.Root>
      {:else}
        <Button href="/sign-in" variant="ghost">Sign In</Button>
        <Button href="/sign-up">Sign Up</Button>
      {/if}
    </div>
  </div>
</header>