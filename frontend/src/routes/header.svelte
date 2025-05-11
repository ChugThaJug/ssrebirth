<script>
    export let title = "LocalXpose: The Most Useful Tool for Developers to Share Localhost Online";
    export let date = "October 18, 2024";
    export let category = "Web";
    export let subcategory = "Developer Tools";
    export let image = "/api/placeholder/800/400";
    
    // Share buttons data
    const shareButtons = [
      { platform: 'Facebook', icon: 'M16.707 5.293a1 1 0 0 1 0 1.414l-8 8a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 1.414-1.414L8 12.586l7.293-7.293a1 1 0 0 1 1.414 0z' },
      { platform: 'Reddit', icon: 'M16.707 5.293a1 1 0 0 1 0 1.414l-8 8a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 1.414-1.414L8 12.586l7.293-7.293a1 1 0 0 1 1.414 0z' },
      { platform: 'Twitter', icon: 'M16.707 5.293a1 1 0 0 1 0 1.414l-8 8a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 1.414-1.414L8 12.586l7.293-7.293a1 1 0 0 1 1.414 0z' },
      { platform: 'LinkedIn', icon: 'M16.707 5.293a1 1 0 0 1 0 1.414l-8 8a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 1.414-1.414L8 12.586l7.293-7.293a1 1 0 0 1 1.414 0z' },
      { platform: 'Email', icon: 'M16.707 5.293a1 1 0 0 1 0 1.414l-8 8a1 1 0 0 1-1.414 0l-4-4a1 1 0 0 1 1.414-1.414L8 12.586l7.293-7.293a1 1 0 0 1 1.414 0z' }
    ];
  </script>
  
  <div class="max-w-7xl mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="text-sm mb-4">
      <a href="/web" class="text-gray-600 hover:text-gray-900">{category}</a>
      <span class="mx-2 text-gray-400">/</span>
      <span class="text-gray-600">{title}</span>
    </nav>
  
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <div>
        <!-- Author info -->
        <div class="flex items-center mb-6">
          <div class="flex items-center text-blue-500">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
            </svg>
            <span class="ml-2 font-medium">SitePoint Sponsors</span>
          </div>
        </div>
  
        <!-- Date -->
        <time class="block text-gray-600 mb-4">{date}</time>
  
        <!-- Title -->
        <h1 class="text-4xl font-bold text-gray-900 mb-6">
          {title}
        </h1>
  
        <!-- Categories -->
        <div class="flex flex-wrap gap-2 mb-6">
          <span class="px-4 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
            Developer Tools
          </span>
          <span class="px-4 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            Web
          </span>
        </div>
  
        <!-- Share buttons -->
        <div class="flex items-center space-x-4">
          <span class="text-gray-600 text-sm">Share this article</span>
          <div class="flex space-x-2">
            {#each shareButtons as button}
              <button class="p-2 text-gray-500 hover:text-gray-700 rounded-full hover:bg-gray-100 transition-colors">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path d={button.icon}></path>
                </svg>
                <span class="sr-only">Share on {button.platform}</span>
              </button>
            {/each}
          </div>
        </div>
      </div>
  
      <!-- Featured image -->
      <div class="rounded-lg overflow-hidden shadow-lg">
        <img 
          src={image} 
          alt={title}
          class="w-full h-auto object-cover"
        />
      </div>
    </div>
  </div>
  
  <style>
    /* Smooth transitions */
    button {
      transition: all 0.2s ease-in-out;
    }
  
    /* Custom hover states for links */
    a:hover {
      text-decoration: underline;
    }
  
    /* Ensure images scale properly */
    img {
      max-width: 100%;
      height: auto;
    }
  </style>