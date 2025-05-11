<script>
    import { onMount } from 'svelte';
    import { user } from '$lib/stores/user';
    import { api } from '$lib/utils/api';
  
    let name = '';
    let bio = '';
    let message = '';
  
    onMount(async () => {
      if ($user) {
        name = $user.name || '';
        bio = $user.bio || '';
      }
    });
  
    async function updateProfile() {
      try {
        const updatedUser = await api.put('/users/me', { name, bio });
        user.set(updatedUser);
        message = 'Profile updated successfully!';
      } catch (error) {
        message = 'Failed to update profile. Please try again.';
      }
    }
  </script>
  
  <main class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-4">Your Profile</h1>
    <form on:submit|preventDefault={updateProfile} class="max-w-md">
      <div class="mb-4">
        <label for="name" class="block mb-2">Name</label>
        <input type="text" id="name" bind:value={name} class="w-full px-3 py-2 border rounded">
      </div>
      <div class="mb-4">
        <label for="bio" class="block mb-2">Bio</label>
        <textarea id="bio" bind:value={bio} rows="4" class="w-full px-3 py-2 border rounded"></textarea>
      </div>
      <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
        Update Profile
      </button>
    </form>
    {#if message}
      <p class="mt-4 text-green-500">{message}</p>
    {/if}
  </main>