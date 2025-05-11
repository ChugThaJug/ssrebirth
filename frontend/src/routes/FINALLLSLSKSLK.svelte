<script>
    import { ArrowLeft } from 'lucide-svelte';
    
    // Sample data
    const post = {
      date: "October 8, 2024",
      title: "Step-by-Step Guide to Creating Your Own Custom Project",
      description: "If you're looking for the best software to create amazing projects, this platform is the solution for you.",
      author: {
        name: "Oliver McKeen",
        avatar: "/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Foliver.50626b09.png"
      },
      relatedPosts: [
        {
          title: "Protecting Your Data Online",
          description: "Learn about the best practices for keeping your information secure while creating content.",
          link: "#"
        },
        {
          title: "Top Examples: Industry Projects",
          description: "Explore how others are using our platform to create amazing content and build their brand.",
          link: "#"
        }
      ]
    };
  </script>
  
  <main class="max-w-6xl min-h-screen p-8 mx-auto">
    <!-- Back to Blog Link -->
    <div>
      <a 
        class="link !no-underline text-base-content/80 hover:text-base-content inline-flex items-center gap-1" 
        title="Back to Blog" 
        href="/blog"
      >
        <ArrowLeft class="w-5 h-5" />
        Back to Blog
      </a>
    </div>
  
    <article class="text-content-on-brand/60">
      <!-- Header Section -->
      <section class="my-12 md:my-20 max-w-[800px]">
        <div class="flex items-center gap-4 mb-6">
          <span class="text-content-on-brand/60" itemprop="datePublished">
            {post.date}
          </span>
        </div>
        
        <h1 class="mb-6 text-4xl font-extrabold tracking-tight md:text-5xl lg:text-6xl text-content-on-brand/100 md:mb-8">
          {post.title}
        </h1>
        
        <p class="text-content-on-brand/80 md:text-lg max-w-[700px]">
          {post.description}
        </p>
      </section>
  
      <!-- Main Content Layout -->
      <div class="flex flex-col md:flex-row">
        <!-- Sidebar -->
        <section class="max-md:pb-4 md:pl-12 max-md:border-b md:border-l md:order-last md:w-72 shrink-0 border-base-content/10">
          <p class="mb-2 text-sm text-content-on-brand/60 md:mb-3">Posted by</p>
          
          <a 
            title="Posts by {post.author.name}" 
            class="inline-flex items-center gap-2 group text-content-on-brand/80" 
            rel="author" 
            href="#"
          >
            <span itemprop="author">
              <img 
                alt="Avatar of {post.author.name}" 
                src={post.author.avatar}
                class="object-cover object-center rounded-full w-7 h-7" 
                width="28" 
                height="28"
              />
            </span>
            <span class="group-hover:underline">{post.author.name}</span>
          </a>
  
          <!-- Related Posts -->
          <div class="hidden mt-12 md:block">
            <p class="mb-2 text-sm text-content-on-brand/60 md:mb-3">Related reading</p>
            <div class="space-y-2 md:space-y-5">
              {#each post.relatedPosts as related}
                <div>
                  <p class="mb-0.5 text-content-on-brand/80">
                    <a 
                      class="font-medium link link-hover hover:link-primary" 
                      href={related.link}
                    >
                      {related.title}
                    </a>
                  </p>
                  <p class="max-w-full text-sm text-content-on-brand/60">
                    {related.description}
                  </p>
                </div>
              {/each}
            </div>
          </div>
        </section>
  
        <!-- Main Content -->
        <section class="w-full space-y-12 max-md:pt-4 md:pr-20 md:space-y-20">
          <div class="prose prose-lg max-w-none">
            <p>
              In the world of technology, creating your own projects has become
              easier and more accessible than ever. Thanks to modern tools and
              applications, anyone can create amazing content in just a few steps.
            </p>
  
            <h2 class="text-2xl lg:text-4xl font-bold tracking-tight mb-4 text-content-on-brand">
              Step 1: Choosing the Right Platform
            </h2>
  
            <p>
              When it comes to creating content, the first step is choosing the
              right tool. There are plenty of options on the market, but if you
              want quality and ease of use, our platform stands out as one of
              the best.
            </p>
  
            <!-- Additional content sections would go here -->
          </div>
        </section>
      </div>
    </article>
  </main>