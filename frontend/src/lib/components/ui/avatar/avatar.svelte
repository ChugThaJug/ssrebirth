<!-- src/lib/components/ui/avatar/avatar.svelte -->
<script lang="ts">
  let className = '';
  export { className as class };
</script>

<div class={`relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full ${className}`}>
  <slot />
</div>