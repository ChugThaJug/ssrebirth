<script>
    import { onMount } from 'svelte';
  
    // Main category filters
    const mainCategories = [
      { id: 'all', label: 'Show All' },
      { id: 'ai', label: 'AI', icon: '⚡' },
      { id: 'javascript', label: 'JavaScript', icon: '📊' },
      { id: 'computing', label: 'Computing', icon: '💻' },
      { id: 'design', label: 'Design & UX', icon: '🎨' },
      { id: 'html', label: 'HTML & CSS', icon: '🌐' },
      { id: 'entrepreneur', label: 'Entrepreneur', icon: '💼' },
      { id: 'web', label: 'Web', icon: '🌍' },
      { id: 'php', label: 'PHP', icon: '🐘' },
      { id: 'wordpress', label: 'WordPress', icon: '📝' },
      { id: 'mobile', label: 'Mobile', icon: '📱' },
      { id: 'programming', label: 'Programming', icon: '💻' },
      { id: 'python', label: 'Python', icon: '🐍' }
    ];
  
    // JavaScript subcategories
    const jsCategories = [
      { id: 'all', label: 'Show All' },
      { id: 'vanilla', label: 'Vanilla JS' },
      { id: 'react', label: 'React' },
      { id: 'node', label: 'Node' },
      { id: 'jquery', label: 'jQuery' },
      { id: 'angular', label: 'Angular' },
      { id: 'deno', label: 'Deno' },
      { id: 'tools', label: 'Tools & Libraries' },
      { id: 'npm', label: 'npm' },
      { id: 'es6', label: 'ES6' },
      { id: 'ember', label: 'Ember' },
      { id: 'engines', label: 'Engines' },
      { id: 'webgl', label: 'WebGL' },
      { id: 'coffeescript', label: 'CoffeeScript' },
      { id: 'ajax', label: 'Ajax' },
      { id: 'apis', label: 'APIs' }
    ];
  
    // Article data
    const articles = [
      {
        title: "LocalXpose: The Most Useful Tool for Developers to Share Localhost Online",
        author: "SitePoint Sponsors",
        image: "/api/placeholder/400/300",
        category: "Tools"
      },
      {
        title: "Comparing Docker and Podman: A Guide to Container Management Tools",
        author: "Vultr",
        image: "/api/placeholder/400/300",
        category: "Computing"
      },
      {
        title: "10 Zsh Tips & Tricks: Configuration, Customization & Usage",
        author: "James Hibbard",
        image: "/api/placeholder/400/300",
        category: "Tools"
      },
      {
        title: "How to Get Started With Google Cloud's Text-to-Speech API",
        author: "Matt Mickiewicz",
        image: "/api/placeholder/400/300",
        category: "AI"
      },
      {
        title: "Kubernetes vs Docker: A Closer Look for 2024",
        author: "Matt Mickiewicz",
        image: "/api/placeholder/400/300",
        category: "Computing"
      },
      {
        title: "Getting Started With Kubernetes on AWS Tutorial (2024 Update)",
        author: "Matt Mickiewicz",
        image: "/api/placeholder/400/300",
        category: "Computing"
      },
      {
        title: "The Best Free Version Control Software For 2024",
        author: "Matt Mickiewicz",
        image: "/api/placeholder/400/300",
        category: "Tools"
      },
      {
        title: "What is a Docker Container and How to Create One",
        author: "Matt Mickiewicz",
        image: "/api/placeholder/400/300",
        category: "Computing"
      }
    ];
  
    let selectedMainCategory = 'javascript';
    let selectedJsCategory = 'all';
    let filteredArticles = articles;
  
    $: {
      // Filter articles based on selected categories
      filteredArticles = articles.filter(article => {
        if (selectedMainCategory === 'all') return true;
        if (selectedJsCategory === 'all') return true;
        // Add more sophisticated filtering logic here
        return true;
      });
    }
  </script>
  
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="mb-12">
      <h1 class="text-4xl font-bold mb-8">Keep up to date on current trends and technologies</h1>
      
      <!-- Main category filters -->
      <div class="flex flex-wrap gap-2 mb-8">
        {#each mainCategories as category}
          <button
            class="px-4 py-2 rounded-full text-sm font-medium transition-colors
              {selectedMainCategory === category.id 
                ? 'bg-gray-900 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
            on:click={() => selectedMainCategory = category.id}
          >
            {#if category.icon}<span class="mr-1">{category.icon}</span>{/if}
            {category.label}
          </button>
        {/each}
      </div>
  
      <!-- JavaScript subcategory filters (shown when JavaScript is selected) -->
      {#if selectedMainCategory === 'javascript'}
        <div class="flex flex-wrap gap-2">
          {#each jsCategories as category}
            <button
              class="px-4 py-2 rounded-full text-sm font-medium transition-colors
                {selectedJsCategory === category.id 
                  ? 'bg-gray-900 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
              on:click={() => selectedJsCategory = category.id}
            >
              {category.label}
            </button>
          {/each}
        </div>
      {/if}
    </div>
  
    <!-- Articles grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {#each filteredArticles as article}
        <article class="group">
          <a href="#" class="block">
            <div class="relative aspect-[4/3] rounded-lg overflow-hidden mb-4">
              <img
                src={article.image}
                alt={article.title}
                class="w-full h-full object-cover transform transition-transform group-hover:scale-105"
              />
            </div>
            <h2 class="text-lg font-semibold mb-2 group-hover:text-blue-600">
              {article.title}
            </h2>
            <p class="text-sm text-gray-600">
              {article.author}
            </p>
          </a>
        </article>
      {/each}
    </div>
  </div>
  
  <style>
    /* Ensure smooth transitions */
    button {
      transition: all 0.2s ease-in-out;
    }
  
    /* Custom scrollbar for filter sections */
    :global(::-webkit-scrollbar) {
      width: 6px;
      height: 6px;
    }
  
    :global(::-webkit-scrollbar-track) {
      background: #f1f1f1;
      border-radius: 3px;
    }
  
    :global(::-webkit-scrollbar-thumb) {
      background: #888;
      border-radius: 3px;
    }
  
    :global(::-webkit-scrollbar-thumb:hover) {
      background: #555;
    }
  </style>