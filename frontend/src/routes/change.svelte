<script>
    import { onMount } from 'svelte';
    
    export let changelogs = [
      {
        id: "changelog-81042",
        title: "SAST vulnerabilities summary now available on the security overview dashboard",
        date: "October 31, 2024",
        summary: "Better manage and mitigate your security vulnerabilities with a new SAST vulnerabilities summary table.",
        labels: ["advanced-security", "code-scanning", "codeql", "security-and-compliance", "security-overview"],
        content: `Now you can better manage and mitigate your security vulnerabilities with a new SAST vulnerabilities summary table, available directly on the security overview dashboard. This feature highlights your top 10 CodeQL and third-party open alerts by count, grouped by vulnerability type.
  
  When prioritizing which alerts to address first, it's crucial to consider various factors. One significant factor is the number of instances of a vulnerability across your codebase. The more areas of code affected by a vulnerability, the higher the potential risk for exploitation.`,
        image: "/api/placeholder/800/400"
      },
      {
        id: "changelog-80903",
        title: "Actions Performance Metrics in public preview",
        date: "October 31, 2024",
        summary: "Get insights into your workflow performance with the new Actions Performance Metrics feature.",
        labels: ["actions"],
        content: `Today, Actions Performance Metrics is now in public preview for all users of GitHub Actions. Actions Performance Metrics is an observability UI that gives you insights into your workflow or job performance for your organizations or repositories.`,
        image: "/api/placeholder/800/400"
      }
    ];
  
    let activeChangelog = changelogs[0].id;
  
    onMount(() => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              activeChangelog = entry.target.id;
            }
          });
        },
        { 
          threshold: 0.5,
          rootMargin: '-20% 0px -20% 0px'
        }
      );
  
      document.querySelectorAll('.changelog-entry').forEach((entry) => {
        observer.observe(entry);
      });
  
      return () => observer.disconnect();
    });
  
    function scrollToChangelog(changelogId, event) {
      event.preventDefault();
      const element = document.getElementById(changelogId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  </script>
  
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="grid grid-cols-12 gap-16">
      <!-- Left timeline navigation -->
      <div class="col-span-4">
        <div class="sticky top-8">
          <h2 class="text-2xl font-semibold text-gray-900 mb-8">Recent Changes</h2>
          <div class="relative">
            <!-- Vertical timeline line - Now properly positioned -->
            <div class="absolute left-[11px] top-0 bottom-0 w-[2px] bg-gray-100"/>
            
            <nav class="relative space-y-8">
              {#each changelogs as changelog}
                <a
                  href="#{changelog.id}"
                  on:click={(e) => scrollToChangelog(changelog.id, e)}
                  class="group block relative pl-10"
                >
                  <!-- Timeline dot -->
                  <div 
                    class="absolute left-[5px] top-[10px] w-[14px] h-[14px] rounded-full border-2 border-white ring-2 transition-colors duration-200"
                    class:ring-blue-500={activeChangelog === changelog.id}
                    class:bg-blue-500={activeChangelog === changelog.id}
                    class:ring-gray-200={activeChangelog !== changelog.id}
                    class:bg-white={activeChangelog !== changelog.id}
                  />
                  
                  <div class="group-hover:bg-gray-50 rounded-lg p-4 transition-colors duration-200">
                    <time class="text-sm text-gray-500">{changelog.date}</time>
                    <h3 class="mt-2 font-medium text-gray-900 leading-tight">
                      {changelog.title}
                    </h3>
                    <p class="mt-2 text-sm text-gray-600">
                      {changelog.summary}
                    </p>
                    
                    <div class="flex flex-wrap gap-2 mt-3">
                      {#each changelog.labels.slice(0, 3) as label}
                        <span class="inline-flex text-sm text-blue-600 hover:text-blue-700">
                          {label}
                        </span>
                      {/each}
                      {#if changelog.labels.length > 3}
                        <span class="inline-flex text-sm text-gray-500">
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
      </div>
  
      <!-- Main content -->
      <div class="col-span-8">
        {#each changelogs as changelog}
          <article 
            id={changelog.id} 
            class="changelog-entry mb-24 scroll-mt-8"
          >
            <time class="text-sm text-blue-600 font-medium">
              {changelog.date}
            </time>
            
            <h2 class="mt-2 text-3xl font-semibold text-gray-900">
              {changelog.title}
            </h2>
            
            <div class="flex flex-wrap gap-2 mt-6">
              {#each changelog.labels as label}
                <span class="px-4 py-1.5 rounded-full text-sm font-medium bg-blue-500 text-white">
                  {label}
                </span>
              {/each}
            </div>
  
            {#if changelog.image}
              <div class="mt-8">
                <img
                  src={changelog.image}
                  alt="Changelog illustration"
                  class="w-full rounded-lg"
                  loading="lazy"
                />
              </div>
            {/if}
  
            <div class="prose prose-lg mt-8">
              {#each changelog.content.split('\n\n') as paragraph}
                <p>{paragraph}</p>
              {/each}
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
  
    .prose {
      max-width: none;
    }
  </style>