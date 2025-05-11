<script>
	import '../app.css';
	import Navbar from '$lib/components/navigation/main-nav.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import Hero from '$lib/components/layout/Hero.svelte';
	import SidebarNav from '$lib/components/navigation/sidebar-nav.svelte';
    import { ModeWatcher } from "mode-watcher";
    // import MainNavbar from '$lib/components/MainNavbar.svelte';

</script>

<div class="flex flex-col min-h-screen">
	<Navbar />
	<SidebarNav />

	<main class="flex-grow">
        <ModeWatcher />
		<slot />
	</main>
	<Footer />
</div>