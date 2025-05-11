<script>
    import { onMount } from 'svelte';
  
    let isMenuOpen = false;
    let isSearchOpen = false;
    let isMobile = false;
  
    onMount(() => {
      const checkWidth = () => {
        isMobile = window.innerWidth < 768;
      };
      checkWidth();
      window.addEventListener('resize', checkWidth);
      return () => window.removeEventListener('resize', checkWidth);
    });
  
    const toggleMenu = () => isMenuOpen = !isMenuOpen;
    const toggleSearch = () => isSearchOpen = !isSearchOpen;
  
    const navigationItems = [
      { name: 'Changelog', href: '/changelog', external: false },
      { name: 'Docs', href: '/docs', external: true },
      { name: 'Customer stories', href: '/customer-stories', external: true }
    ];
  
    const breadcrumbs = [
      { name: 'Home', href: '/' },
      { name: 'News & insights', href: '/news-insights' },
      { name: 'Product', href: '/news-insights/product-news' }
    ];
  
    const tableOfContents = [
      { name: "Anthropic's Claude 3.5 Sonnet", href: '#anthropics-claude' },
      { name: "Google's Gemini 1.5 Pro", href: '#googles-gemini' },
      { name: "OpenAI's o1-preview", href: '#openais-preview' }
    ];
  
    const footerLinks = [
      {
        title: 'Product',
        links: [
          { name: 'Features', href: '/features' },
          { name: 'Security', href: '/security' },
          { name: 'Enterprise', href: '/enterprise' },
          { name: 'Customer stories', href: '/customer-stories' }
        ]
      },
      {
        title: 'Platform',
        links: [
          { name: 'Developer API', href: '/api' },
          { name: 'Partners', href: '/partners' },
          { name: 'Electron', href: '/electron' },
          { name: 'Desktop', href: '/desktop' }
        ]
      }
    ];
  </script>
  
  <div class="min-h-screen bg-white">
    <header class="fixed top-0 w-full bg-[#24292e] text-white z-50">
      <div class="max-w-[1280px] mx-auto px-4 md:px-6">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center space-x-3">
            <a href="/" class="text-white flex items-center">
              <span class="text-xl font-semibold">GitHub</span>
            </a>
            <span class="text-gray-500">/</span>
            <a href="/" class="text-white text-lg font-semibold">Blog</a>
          </div>
  
          <nav class="hidden md:flex items-center space-x-6">
            {#each navigationItems as item}
              <a 
                href={item.href} 
                class="text-gray-300 hover:text-white transition-colors duration-200"
                target={item.external ? "_blank" : "_self"}
                rel={item.external ? "noopener noreferrer" : ""}
              >
                {item.name}
              </a>
            {/each}
            <button 
              class="text-gray-300 hover:text-white"
              on:click={toggleSearch}
            >
              Search
            </button>
          </nav>
  
          <button 
            class="md:hidden p-2 text-gray-300 hover:text-white"
            on:click={toggleMenu}
          >
            <span class="sr-only">Open menu</span>
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
  
        {#if isMenuOpen}
          <div class="md:hidden py-4 border-t border-gray-700">
            <nav class="space-y-2">
              {#each navigationItems as item}
                <a 
                  href={item.href} 
                  class="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-700"
                >
                  {item.name}
                </a>
              {/each}
            </nav>
          </div>
        {/if}
      </div>
    </header>
  
    <main class="pt-16">
      <div class="max-w-[1280px] mx-auto px-4 md:px-6 py-12">
        <nav class="mb-8">
          <ol class="flex items-center space-x-2 text-sm">
            {#each breadcrumbs as crumb, index}
              <li>
                <a href={crumb.href} class="text-gray-600 hover:text-gray-900">
                  {crumb.name}
                </a>
                {#if index !== breadcrumbs.length - 1}
                  <span class="mx-2 text-gray-400">/</span>
                {/if}
              </li>
            {/each}
          </ol>
        </nav>
  
        <h1 class="text-4xl font-bold text-gray-900 mb-6 max-w-4xl">
          Bringing developer choice to Copilot with Anthropic's Claude 3.5 Sonnet, Google's Gemini 1.5 Pro, and OpenAI's o1-preview
        </h1>
  
        <div class="flex items-center text-sm text-gray-600 mb-8">
          <a href="/author/thomasd" class="font-medium hover:text-gray-900">Thomas Dohmke</a>
          <span class="mx-2">·</span>
          <time datetime="2024-10-29">October 29, 2024</time>
          <span class="mx-2">·</span>
          <span>3 min read</span>
        </div>
  
        <div class="mb-12">
          <img 
            src="hero-image-github-universe-2024.png"
            alt="GitHub Universe 2024"
            class="w-full rounded-lg shadow-lg"
          />
        </div>
      </div>
  
      <div class="max-w-[1280px] mx-auto px-4 md:px-6">
        <div class="flex flex-col lg:flex-row gap-12">
          <article class="lg:w-2/3">
            <div class="prose prose-lg max-w-none">
              <p>
                GitHub Copilot has long leveraged different large language models (LLMs) 
                for different use cases. The first public version of Copilot was launched 
                using Codex, an early version of OpenAI GPT-3, specifically fine-tuned 
                for coding tasks.
              </p>
  
              <h2 id="anthropics-claude">Anthropic's Claude 3.5 Sonnet</h2>
              <p>
                Anthropic's new Claude 3.5 Sonnet excels at coding tasks across the entire 
                software development lifecycle—from initial design to bug fixes, maintenance 
                to optimizations.
              </p>
  
              <h2 id="googles-gemini">Google's Gemini 1.5 Pro</h2>
              <p>
                The latest Gemini models from Google show high capabilities in coding scenarios. 
                Gemini 1.5 Pro features a two-million-token context window and is natively 
                multi-modal.
              </p>
            </div>
          </article>
  
          <aside class="lg:w-1/3">
            <div class="sticky top-24">
              <div class="bg-gray-50 rounded-lg p-6">
                <h2 class="text-lg font-semibold mb-4">Table of Contents</h2>
                <nav>
                  <ul class="space-y-2">
                    {#each tableOfContents as item}
                      <li>
                        <a 
                          href={item.href}
                          class="text-gray-600 hover:text-gray-900 block"
                        >
                          {item.name}
                        </a>
                      </li>
                    {/each}
                  </ul>
                </nav>
              </div>
            </div>
          </aside>
        </div>
      </div>
  
      <div class="bg-gray-50 mt-16 py-12">
        <div class="max-w-[1280px] mx-auto px-4 md:px-6">
          <div class="bg-white rounded-lg shadow-sm p-8">
            <div class="max-w-2xl mx-auto text-center">
              <h2 class="text-2xl font-bold mb-4">Stay up to date</h2>
              <p class="text-gray-600 mb-6">
                Get the latest GitHub news, updates, and developer insights 
                delivered to your inbox.
              </p>
              <form class="flex gap-4">
                <input
                  type="email"
                  placeholder="Enter your email"
                  class="flex-grow px-4 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <button 
                  type="submit" 
                  class="bg-[#24292e] text-white px-6 py-2 rounded-md hover:bg-gray-800 transition-colors"
                >
                  Subscribe
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  
    <footer class="bg-[#24292e] text-white mt-16">
      <div class="max-w-[1280px] mx-auto px-4 md:px-6 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          {#each footerLinks as section}
            <div>
              <h3 class="text-lg font-semibold mb-4">{section.title}</h3>
              <ul class="space-y-2">
                {#each section.links as link}
                  <li>
                    <a 
                      href={link.href}
                      class="text-gray-400 hover:text-white transition-colors"
                    >
                      {link.name}
                    </a>
                  </li>
                {/each}
              </ul>
            </div>
          {/each}
        </div>
  
        <div class="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400">© 2024 GitHub, Inc.</p>
          <div class="flex space-x-6 mt-4 md:mt-0">
            <a href="/twitter" class="text-gray-400 hover:text-white">Twitter</a>
            <a href="/facebook" class="text-gray-400 hover:text-white">Facebook</a>
            <a href="/linkedin" class="text-gray-400 hover:text-white">LinkedIn</a>
            <a href="/youtube" class="text-gray-400 hover:text-white">YouTube</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
  
  <style lang="postcss">
    :global(html) {
      scroll-behavior: smooth;
    }
  
    :global(body) {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  
    .prose {
      @apply text-gray-700;
    }
  
    .prose h2 {
      @apply text-2xl font-bold text-gray-900 mt-8 mb-4;
    }
  
    .prose p {
      @apply mb-6 leading-relaxed;
    }
  
    /* Custom scrollbar for webkit browsers */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
  
    ::-webkit-scrollbar-track {
      background: #f1f1f1;
    }
  
    ::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: 4px;
    }
  
    ::-webkit-scrollbar-thumb:hover {
      background: #555;
    }
  </style>