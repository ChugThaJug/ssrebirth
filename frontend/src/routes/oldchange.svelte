<script>
    import { onMount } from 'svelte';
    
    // Enhanced changelog data structure
    export let changelogs = [
      {
        id: "changelog-81042",
        title: "SAST vulnerabilities summary now available on the security overview dashboard",
        date: "October 31, 2024",
        labels: ["advanced-security", "code-scanning", "codeql", "security-and-compliance", "security-overview"],
        summary: "Better manage and mitigate your security vulnerabilities with a new SAST vulnerabilities summary table.",
        content: `Now you can better manage and mitigate your security vulnerabilities with a new SAST vulnerabilities summary table, available directly on the security overview dashboard. This feature highlights your top 10 CodeQL and third-party open alerts by count, grouped by vulnerability type.
  
  When prioritizing which alerts to address first, it's crucial to consider various factors. One significant factor is the number of instances of a vulnerability across your codebase. The more areas of code affected by a vulnerability, the higher the potential risk for exploitation.`,
        image: "/api/placeholder/800/400"
      },
      {
        id: "changelog-80903",
        title: "Actions Performance Metrics in public preview",
        date: "October 31, 2024",
        labels: ["actions"],
        summary: "Get insights into your workflow performance with the new Actions Performance Metrics feature.",
        content: `Today, Actions Performance Metrics is now in public preview for all users of GitHub Actions. Actions Performance Metrics is an observability UI that gives you insights into your workflow or job performance for your organizations or repositories.
  
  Performance metrics can help you answer these commonly asked questions about your Actions workflow runs:
  • How long does it take for my workflows or jobs to complete?
  • How long are my workflows or jobs waiting to run?
  • Which of my workflows or jobs are consistently failing?
  • Where are my longest running workflows or jobs originating from?`,
        image: "/api/placeholder/800/400"
      }
    ];
  
    let activeChangelog = '';
    let isInViewport = new Set();
  
    // Enhanced intersection observer with better tracking
    onMount(() => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              isInViewport.add(entry.target.id);
              activeChangelog = entry.target.id;
            } else {
              isInViewport.delete(entry.target.id);
            }
          });
          // If no entries are intersecting, find the closest one above viewport
          if (isInViewport.size === 0) {
            const elements = [...document.querySelectorAll('.changelog-entry')]
              .map(el => ({
                id: el.id,
                top: el.getBoundingClientRect().top
              }))
              .filter(el => el.top < 0)
              .sort((a, b) => b.top - a.top);
            
            if (elements.length > 0) {
              activeChangelog = elements[0].id;
            }
          }
        },
        {
          threshold: [0, 0.25, 0.5, 0.75, 1],
          rootMargin: '-20% 0px -20% 0px'
        }
      );
  
      document.querySelectorAll('.changelog-entry').forEach((entry) => {
        observer.observe(entry);
      });
  
      return () => observer.disconnect();
    });
  
    // Smooth scroll handler
    function scrollToChangelog(changelogId, event) {
      event.preventDefault();
      const element = document.getElementById(changelogId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  </script>
  
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="grid grid-cols-12 gap-12">
      <!-- Left timeline navigation - Now wider -->
      <div class="col-span-5">
        <div class="sticky top-8 pr-8">
          <h2 class="text-xl font-bold mb-8 text-gray-900">Recent Changes</h2>
          <nav class="flex flex-col space-y-1">
            {#each changelogs as changelog}
              <a
                href="#{changelog.id}"
                on:click={(e) => scrollToChangelog(changelog.id, e)}
                class="group relative pl-12 py-6 transition-all duration-200 rounded-lg hover:bg-gray-50"
                class:bg-gray-50={activeChangelog === changelog.id}
                class:text-gray-600={activeChangelog !== changelog.id}
              >
                <!-- Vertical timeline line -->
                <div 
                  class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200 group-hover:bg-gray-300"
                  class:bg-blue-100={activeChangelog === changelog.id}
                />
                
                <!-- Timeline dot -->
                <div 
                  class="absolute left-[14px] top-8 w-3 h-3 rounded-full border-2 transition-all duration-200"
                  class:border-blue-600={activeChangelog === changelog.id}
                  class:bg-blue-600={activeChangelog === changelog.id}
                  class:border-gray-300={activeChangelog !== changelog.id}
                  class:bg-white={activeChangelog !== changelog.id}
                />
                
                <div class="space-y-2">
                  <time class="block text-sm text-gray-500">{changelog.date}</time>
                  <h3 class="text-base font-medium text-gray-900 group-hover:text-blue-600 line-clamp-2">
                    {changelog.title}
                  </h3>
                  <p class="text-sm text-gray-600 line-clamp-2">{changelog.summary}</p>
                  
                  <div class="flex flex-wrap gap-2 pt-2">
                    {#each changelog.labels.slice(0, 3) as label}
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                        {label}
                      </span>
                    {/each}
                    {#if changelog.labels.length > 3}
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                        +{changelog.labels.length - 3} more
                      </span>
                    {/if}
                  </div>
                </div>
              </a>
            {/each}
          </nav>
        </div>
      </div>
  
      <!-- Main content - Adjusted width -->
      <div class="col-span-7">
        {#each changelogs as changelog}
          <article 
            id={changelog.id} 
            class="changelog-entry mb-24 scroll-mt-8 relative"
          >
            <!-- Header section -->
            <div class="mb-8">
              <time class="block text-sm font-medium text-blue-600 mb-3">{changelog.date}</time>
              <h2 class="text-3xl font-bold text-gray-900 mb-6">{changelog.title}</h2>
              
              <div class="flex flex-wrap gap-2 mb-6">
                {#each changelog.labels as label}
                  <span class="px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
                    {label}
                  </span>
                {/each}
              </div>
            </div>
  
            <!-- Content section -->
            {#if changelog.image}
              <div class="mb-8 rounded-xl overflow-hidden shadow-lg">
                <img
                  src={changelog.image}
                  alt="Changelog illustration"
                  class="w-full h-auto"
                  loading="lazy"
                />
              </div>
            {/if}
  
            <div class="prose prose-lg max-w-none">
              {#each changelog.content.split('\n\n') as paragraph}
                <p>{paragraph}</p>
              {/each}
            </div>
  
            <!-- Footer section -->
            <div class="mt-12 pt-6 border-t border-gray-200">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <button class="inline-flex items-center space-x-2 text-gray-600 hover:text-blue-600">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
                    </svg>
                    <span>Share</span>
                  </button>
                  <button class="inline-flex items-center space-x-2 text-gray-600 hover:text-blue-600">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
                    </svg>
                    <span>Save</span>
                  </button>
                </div>
                <button class="inline-flex items-center space-x-2 text-gray-600 hover:text-blue-600">
                  <span>Learn more</span>
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
          </article>
        {/each}
      </div>
    </div>
  </div>
  
  <style>
    :global(html) {
      scroll-behavior: smooth;
    }
  
    :global(.prose) {
      max-width: none;
    }
  
    :global(.prose p) {
      margin-top: 1.25em;
      margin-bottom: 1.25em;
    }
  
    .line-clamp-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>