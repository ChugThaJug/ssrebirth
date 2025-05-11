<script>
    import { onMount } from 'svelte';
    
    // Navigation items
    const navItems = [
      { title: 'Premium', href: '#' },
      { title: 'Forum', href: '#' },
      { title: 'Developer Jobs', href: '#' },
      { title: 'Tutorials', href: '#', hasDropdown: true },
      { title: 'Pricing', href: '#' },
      { title: 'Blog', href: '#', hasDropdown: true }
    ];
  
    // Table of contents
    const tableOfContents = [
      { title: 'What is LocalXpose?', href: '#what-is-localxpose' },
      { title: 'Why LocalXpose?', href: '#why-localxpose' },
      { title: 'Getting Started', href: '#getting-started' },
      { title: 'Further Settings', href: '#further-settings' },
      { title: 'Pricing and Plans', href: '#pricing-and-plans' },
      { title: 'Use Cases', href: '#use-cases' },
      { title: 'Resources', href: '#resources' },
      { title: 'Conclusion', href: '#conclusion' }
    ];
  
    // Social share buttons
    const shareButtons = [
      { platform: 'Facebook', icon: 'facebook' },
      { platform: 'Reddit', icon: 'reddit' },
      { platform: 'Twitter', icon: 'twitter' },
      { platform: 'LinkedIn', icon: 'linkedin' },
      { platform: 'Email', icon: 'mail' }
    ];
  
    let isSearchOpen = false;
    let activeSection = '';
  
    onMount(() => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              activeSection = entry.target.id;
            }
          });
        },
        { threshold: 0.5 }
      );
  
      document.querySelectorAll('section[id]').forEach((section) => {
        observer.observe(section);
      });
  
      return () => observer.disconnect();
    });
  </script>
  
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <header class="fixed top-0 w-full bg-white border-b border-gray-200 z-50">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex items-center">
            <a href="/" class="flex items-center">
              <img src="/api/placeholder/32/32" alt="SitePoint" class="h-8 w-auto" />
              <span class="ml-2 text-xl font-semibold">sitepoint</span>
            </a>
          </div>
  
          <!-- Navigation -->
          <nav class="hidden md:flex space-x-8">
            {#each navItems as item}
              <a 
                href={item.href}
                class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium flex items-center"
              >
                {item.title}
                {#if item.hasDropdown}
                  <svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M19 9l-7 7-7-7" />
                  </svg>
                {/if}
              </a>
            {/each}
          </nav>
  
          <!-- Right section -->
          <div class="flex items-center space-x-4">
            <button 
              class="text-gray-700 hover:text-gray-900"
              on:click={() => isSearchOpen = !isSearchOpen}
            >
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            <a href="/login" class="text-gray-700 hover:text-gray-900">Login</a>
            <a 
              href="/trial" 
              class="bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-purple-700"
            >
              Start Free Trial
            </a>
          </div>
        </div>
      </div>
    </header>
  
    <!-- Main content -->
    <main class="pt-16">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <!-- Breadcrumb -->
        <nav class="text-gray-500 text-sm mb-8">
          <a href="/web" class="hover:text-gray-900">Web</a>
          <span class="mx-2">/</span>
          <span>LocalXpose: The Most Useful Tool for Developers to Share Localhost Online</span>
        </nav>
  
        <div class="flex flex-col lg:flex-row gap-12">
          <!-- Left sidebar -->
          <div class="lg:w-64 flex-shrink-0">
            <div class="sticky top-24">
              <h2 class="text-lg font-semibold mb-4">Table of Contents</h2>
              <nav class="space-y-1">
                {#each tableOfContents as item}
                  <a 
                    href={item.href}
                    class="block py-2 text-gray-600 hover:text-gray-900 {activeSection === item.href.slice(1) ? 'text-purple-600' : ''}"
                  >
                    {item.title}
                  </a>
                {/each}
              </nav>
            </div>
          </div>
  
          <!-- Main content -->
          <div class="flex-1 max-w-3xl">
            <article>
              <!-- Article header -->
              <header class="mb-8">
                <div class="flex items-center mb-4">
                  <img src="/api/placeholder/40/40" alt="SitePoint" class="h-10 w-10 rounded-full" />
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">SitePoint Sponsors</p>
                    <p class="text-sm text-gray-500">October 18, 2024</p>
                  </div>
                </div>
  
                <h1 class="text-4xl font-bold text-gray-900 mb-4">
                  LocalXpose: The Most Useful Tool for Developers to Share Localhost Online
                </h1>
  
                <div class="flex flex-wrap gap-2">
                  <span class="px-3 py-1 rounded-full text-sm bg-purple-100 text-purple-800">
                    Developer Tools
                  </span>
                  <span class="px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                    Web
                  </span>
                </div>
              </header>
  
              <!-- Article content -->
              <div class="prose prose-lg max-w-none">
                <section id="introduction" class="mb-12">
                  <p class="text-gray-600">
                    Picture this: You're a developer, working hard on your latest project. 
                    You've just created an amazing new feature on your local machine, and 
                    you're bursting with excitement to show it off to your team or client. But 
                    then reality hits – they're not in the same room, or even the same 
                    country as you. How do you share your locally hosted masterpiece with 
                    them?
                  </p>
                </section>
  
                <section id="installation" class="mb-12">
                  <h2 class="text-2xl font-bold mb-4">Installation</h2>
                  <p class="mb-4">You can install the appropriate version for your operating system:</p>
                  
                  <div class="space-y-4">
                    <div class="rounded-lg bg-gray-50 p-4">
                      <h3 class="font-semibold">For Windows:</h3>
                      <p>Simply run the downloaded .exe file and follow the installation wizard.</p>
                    </div>
                    
                    <div class="rounded-lg bg-gray-50 p-4">
                      <h3 class="font-semibold">For macOS:</h3>
                      <p>Double-click the .dmg file, drag LocalXpose to your Applications folder, and you're done!</p>
                    </div>
                    
                    <div class="rounded-lg bg-gray-50 p-4">
                      <h3 class="font-semibold">For Linux:</h3>
                      <p>Use your package manager to install the downloaded package, or run the provided shell script.</p>
                    </div>
                  </div>
                </section>
  
                <!-- Additional sections would go here -->
              </div>
            </article>
          </div>
  
          <!-- Right sidebar -->
          <div class="lg:w-64 flex-shrink-0">
            <div class="sticky top-24">
              <div class="bg-gray-900 rounded-lg p-6 text-white">
                <h3 class="text-xl font-semibold mb-4">SitePoint Premium</h3>
                <p class="mb-4">Stay Relevant and Grow Your Career in Tech</p>
                <ul class="space-y-2 mb-6">
                  <li class="flex items-center">
                    <svg class="h-5 w-5 text-purple-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                    Hundreds of Courses and Books
                  </li>
                  <li class="flex items-center">
                    <svg class="h-5 w-5 text-purple-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                    Curated Learning Paths
                  </li>
                  <li class="flex items-center">
                    <svg class="h-5 w-5 text-purple-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/>
                    </svg>
                    Unlimited Access
                  </li>
                </ul>
                <button class="w-full bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700">
                  Start Free Trial
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
  
  <style>
    :global(html) {
      scroll-behavior: smooth;
    }
  
    .prose {
      max-width: none;
    }
  
    .sticky {
      position: sticky;
      top: 24px;
    }
  </style>