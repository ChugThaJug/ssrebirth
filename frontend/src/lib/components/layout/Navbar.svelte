<script lang="ts">
	import { Button } from "bits-ui";
    import MobileNav from "../navigation/mobile-nav.svelte"
    import LightSwitch  from "../light-switch.svelte";


</script>

<header
	class="sticky top-0 z-50 overflow-x-hidden border-b border-border bg-background/75 backdrop-blur-md"
>
	<div class="container px-4">
		<div class="flex h-[70px] items-center justify-between gap-3">
			<div class="flex items-center gap-1.5">
				<MobileNav />
				<a
					href="/"
					class="ml-2 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background"
				>
                <h1 class="text-center text-4xl font-bold leading-tight tracking-tighter md:text-4xl lg:leading-[1.1]">stepify.tech</h1>
            </a>
			</div>
			<div class="flex items-center justify-end gap-2.5">
				<Button.Root
					target="_blank"
					rel="noopener noreferrer"
					class="inline-flex h-10 items-center
					justify-center whitespace-nowrap rounded-[9px] bg-muted px-4
					text-sm font-semibold text-foreground ring-offset-background transition-colors hover:bg-dark-10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background"
				>
					Report an issue
				</Button.Root>
				<LightSwitch />
			</div>
		</div>
	</div>
</header>