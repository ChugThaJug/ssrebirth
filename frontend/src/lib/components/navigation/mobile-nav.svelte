<script lang="ts">
	import MobileLink from "./mobile-link.svelte";
	import { Logo } from "$lib/components/icons/index.js";
	import { Square } from "lucide-svelte"
	import { Button } from "$lib/components/ui/button/index.js";
	import * as Sheet from "$lib/components/ui/sheet/index.js";
	import { navigation } from "$lib/config/index.js";

	let open = false;
</script>

<Sheet.Root bind:open>
	<Sheet.Trigger asChild let:builder>
		<Button
			builders={[builder]}
			variant="ghost"
			class="mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 md:hidden"
		>
			<Square class="h-5 w-5" />
			<span class="sr-only">Toggle Menu</span>
		</Button>
	</Sheet.Trigger>
	<Sheet.Content side="left" class="pr-0">
		<MobileLink href="/" class="flex items-center" {open}>
			<Logo />
		</MobileLink>
		<div class="my-4 h-[calc(100vh-8rem)] overflow-auto pb-10 pl-6">
			<div class="flex flex-col space-y-2">
				{#each navigation.sidebar as navItem, index (index)}
					<div class="flex flex-col space-y-3 pt-6">
						<h4 class="font-medium">{navItem.title}</h4>
						{#if navItem?.items?.length}
							{#each navItem.items as item}
								{#if !item.disabled && item.href}
									<MobileLink href={item.href} bind:open>
										{item.title}
									</MobileLink>
								{/if}
							{/each}
						{/if}
					</div>
				{/each}
			</div>
		</div>
	</Sheet.Content>
</Sheet.Root>
