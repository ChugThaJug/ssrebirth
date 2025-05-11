<script>
    let isMenuOpen = false;
    let isSearchOpen = false;
  
    const toggleMenu = () => {
      isMenuOpen = !isMenuOpen;
    };
  
    const toggleSearch = () => {
      isSearchOpen = !isSearchOpen;
    };
  </script>
  
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-[#24292e] text-white sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <a href="/" class="text-white font-bold text-xl">GitHub Blog</a>
          </div>
  
          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center space-x-8">
            <a href="#" class="text-gray-300 hover:text-white">AI & ML</a>
            <a href="#" class="text-gray-300 hover:text-white">Developer Skills</a>
            <a href="#" class="text-gray-300 hover:text-white">Engineering</a>
            <a href="#" class="text-gray-300 hover:text-white">Security</a>
          </nav>
  
          <!-- Mobile Menu Button -->
          <button 
            class="md:hidden p-2 text-gray-300 hover:text-white"
            on:click={toggleMenu}
          >
            <span class="text-2xl">☰</span>
          </button>
        </div>
  
        <!-- Mobile Menu -->
        {#if isMenuOpen}
          <nav class="md:hidden py-4 px-2 space-y-2">
            <a href="#" class="block text-gray-300 hover:text-white py-2">AI & ML</a>
            <a href="#" class="block text-gray-300 hover:text-white py-2">Developer Skills</a>
            <a href="#" class="block text-gray-300 hover:text-white py-2">Engineering</a>
            <a href="#" class="block text-gray-300 hover:text-white py-2">Security</a>
          </nav>
        {/if}
      </div>
    </header>
  
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-gray-50 to-gray-100 py-16">
      <div class="max-w-7xl mx-auto px-4">
        <div class="max-w-3xl">
          <h1 class="text-4xl font-bold text-gray-900 mb-4">
            Bringing developer choice to Copilot with Claude 3.5 Sonnet
          </h1>
          <div class="flex items-center text-gray-600 mb-8">
            <span>Thomas Dohmke</span>
            <span class="mx-2">·</span>
            <span>October 29, 2024</span>
            <span class="mx-2">·</span>
            <span>3 min read</span>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Main Content -->
    <main class="flex-grow max-w-7xl mx-auto px-4 py-12">
      <div class="flex flex-col lg:flex-row gap-12">
        <!-- Article Content -->
        <article class="lg:w-2/3">
          <div class="prose max-w-none">
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              GitHub Copilot has long leveraged different large language models (LLMs) 
              for different use cases. The first public version of Copilot was launched 
              using Codex, an early version of OpenAI GPT-3, specifically fine-tuned 
              for coding tasks.
            </p>
            <h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">
              Anthropic's Claude 3.5 Sonnet
            </h2>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              Anthropic's new Claude 3.5 Sonnet excels at coding tasks across the 
              entire software development lifecycle—from initial design to bug fixes, 
              maintenance to optimizations.
            </p>
          </div>
        </article>
  
        <!-- Sidebar -->
        <aside class="lg:w-1/3">
          <div class="sticky top-24">
            <div class="bg-gray-50 rounded-lg p-6">
              <h3 class="text-lg font-semibold mb-4">Table of Contents</h3>
              <nav class="space-y-2">
                <a href="#" class="block text-gray-600 hover:text-gray-900">
                  Anthropic's Claude 3.5 Sonnet
                </a>
                <a href="#" class="block text-gray-600 hover:text-gray-900">
                  Google's Gemini 1.5 Pro
                </a>
                <a href="#" class="block text-gray-600 hover:text-gray-900">
                  OpenAI's o1-preview
                </a>
              </nav>
            </div>
  
            <div class="mt-8 bg-gray-50 rounded-lg p-6">
              <h3 class="text-lg font-semibold mb-4">Related Posts</h3>
              <div class="space-y-4">
                <a href="#" class="block hover:bg-gray-100 rounded p-2">
                  <h4 class="font-medium text-gray-900">New from Universe 2024</h4>
                  <p class="text-sm text-gray-600">Get the latest previews and releases</p>
                </a>
                <a href="#" class="block hover:bg-gray-100 rounded p-2">
                  <h4 class="font-medium text-gray-900">Octoverse 2024</h4>
                  <p class="text-sm text-gray-600">AI leads Python to top language</p>
                </a>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </main>
  
    <!-- Newsletter Section -->
    <section class="bg-gray-50 py-12">
      <div class="max-w-7xl mx-auto px-4">
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
                class="flex-grow px-4 py-2 border rounded focus:ring-2 focus:ring-blue-500"
              />
              <button class="bg-[#24292e] text-white px-6 py-2 rounded hover:bg-gray-800">
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  
    <!-- Footer -->
    <footer class="bg-[#24292e] text-white mt-12">
      <div class="max-w-7xl mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">Product</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-300 hover:text-white">Features</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Security</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Enterprise</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Resources</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-300 hover:text-white">Documentation</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Community</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Support</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Company</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-300 hover:text-white">About</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Blog</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Careers</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Legal</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-300 hover:text-white">Privacy</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Terms</a></li>
              <li><a href="#" class="text-gray-300 hover:text-white">Cookie Policy</a></li>
            </ul>
          </div>
        </div>
  
        <div class="border-t border-gray-700 pt-8 mt-8 flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400 mb-4 md:mb-0">© 2024 GitHub, Inc.</p>
          <div class="flex space-x-6">
            <a href="#" class="text-gray-400 hover:text-white">Twitter</a>
            <a href="#" class="text-gray-400 hover:text-white">Facebook</a>
            <a href="#" class="text-gray-400 hover:text-white">LinkedIn</a>
            <a href="#" class="text-gray-400 hover:text-white">YouTube</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
  
  <style lang="postcss">
    :global(html) {
      background-color: white;
    }
    
    :global(body) {
      margin: 0;
      padding: 0;
    }
  </style>