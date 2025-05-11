<!-- src/lib/components/navigation/Sidebar.svelte -->
<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import {
        Sheet,
        SheetContent,
        SheetHeader,
        SheetTitle,
        SheetTrigger,
    } from "$lib/components/ui/sheet";
    import { 
        Package2, 
        Home,
        Settings,
        Search,
        User,
        Menu
    } from "lucide-svelte";
    import { cn } from "$lib/utils";

    // Navigation items configuration
    const navigationItems = [
        {
            title: "Home",
            icon: Home,
            href: "/"
        },
        {
            title: "Videos",
            icon: Package2,
            href: "/videos"
        },
        {
            title: "Settings",
            icon: Settings,
            href: "/settings"
        }
    ];

    let isMobileOpen = false;
</script>

{#if isMobileOpen}
    <!-- Mobile Sidebar -->
    <Sheet bind:open={isMobileOpen}>
        <SheetTrigger asChild let:builder>
            <Button 
                builders={[builder]}
                variant="ghost" 
                size="icon" 
                class="lg:hidden"
            >
                <Menu class="h-5 w-5" />
                <span class="sr-only">Toggle Menu</span>
            </Button>
        </SheetTrigger>
        <SheetContent side="left" class="w-[240px] p-0">
        </SheetContent>
    </Sheet>
{/if}

<!-- Desktop Sidebar -->
<aside class="hidden lg:flex w-[240px] flex-col border-r">
</aside>

<!-- Separate the content into its own component -->
<script context="module" lang="ts">
    function SidebarContent() {
        return `
            <div class="flex h-full flex-col gap-4">
                <div class="flex h-14 items-center border-b px-4">
                    <span class="font-semibold">Menu</span>
                </div>

                <ScrollArea class="flex-1 px-2">
                    <div class="space-y-2">
                        {#each navigationItems as item}
                            <Button
                                variant="ghost"
                                class="w-full justify-start gap-2"
                                href={item.href}
                            >
                                <svelte:component this={item.icon} class="h-5 w-5" />
                                {item.title}
                            </Button>
                        {/each}
                    </div>
                </ScrollArea>

                <div class="border-t p-4">
                    <Button 
                        variant="ghost" 
                        class="w-full justify-start gap-2"
                        href="/profile"
                    >
                        <User class="h-5 w-5" />
                        Profile
                    </Button>
                </div>
            </div>
        `;
    }
</script>

<style>
    :global(.dark) {
        color-scheme: dark;
    }
</style>