<!-- src/routes/+page.svelte -->
<script>
  import { Button } from '$lib/components/ui/button';
  import { isAuthenticated } from '$lib/firebase';
</script>

<div class="bg-background">
  <div class="relative overflow-hidden">
    <!-- Hero Section -->
    <div class="pt-10 sm:pt-16 lg:overflow-hidden lg:pt-8 lg:pb-14">
      <div class="mx-auto max-w-7xl lg:px-8">
        <div class="lg:grid lg:grid-cols-2 lg:gap-8">
          <div class="mx-auto max-w-md px-4 sm:max-w-2xl sm:px-6 sm:text-center lg:flex lg:items-center lg:px-0 lg:text-left">
            <div class="lg:py-24">
              <h1 class="text-4xl font-bold tracking-tight text-black sm:mt-5 sm:text-6xl lg:mt-6 xl:text-6xl dark:text-white">
                <span class="block">Transform YouTube Videos</span>
                <span class="block text-primary">into Structured Content</span>
              </h1>
              <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl dark:text-gray-400">
                Convert any YouTube video into well-organized, readable content with AI-powered analysis. Get chapters, summaries, and more.
              </p>
              <div class="mt-10 sm:mt-12">
                {#if $isAuthenticated}
                  <Button href="/dashboard" size="lg" class="px-8">Go to Dashboard</Button>
                {:else}
                  <div class="sm:mx-auto sm:max-w-xl lg:mx-0">
                    <div class="sm:flex">
                      <div class="sm:mt-0 sm:ml-3">
                        <Button href="/sign-up" size="lg" class="px-8">Get Started</Button>
                      </div>
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          </div>
          <div class="mt-12 -mb-16 sm:-mb-48 lg:relative lg:m-0">
            <div class="mx-auto max-w-md px-4 sm:max-w-2xl sm:px-6 lg:max-w-none lg:px-0">
              <img
                class="w-full lg:absolute lg:inset-y-0 lg:left-0 lg:h-full lg:w-auto lg:max-w-none rounded-lg shadow-xl"
                src="/hero-image.jpg"
                alt="App screenshot"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="relative bg-gray-50 py-16 sm:py-24 lg:py-32 dark:bg-gray-900">
      <div class="mx-auto max-w-md px-4 text-center sm:max-w-3xl sm:px-6 lg:max-w-7xl lg:px-8">
        <h2 class="text-base font-semibold uppercase tracking-wider text-primary">Features</h2>
        <p class="mt-2 text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl dark:text-white">
          Everything you need to process videos
        </p>
        <p class="mx-auto mt-5 max-w-prose text-xl text-gray-500 dark:text-gray-400">
          Our AI-powered processing gives you everything you need to transform videos into useful content.
        </p>
        <div class="mt-12">
          <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div class="pt-6">
              <div class="rounded-lg bg-white px-6 pb-8 dark:bg-gray-800">
                <div class="-mt-6 flex justify-center">
                  <div class="inline-flex items-center justify-center rounded-md bg-primary p-3 shadow-lg">
                    <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
                    </svg>
                  </div>
                </div>
                <h3 class="mt-8 text-lg font-medium tracking-tight text-gray-900 dark:text-white">Structured Transcripts</h3>
                <p class="mt-5 text-base text-gray-500 dark:text-gray-400">
                  Get clean, organized transcripts with proper paragraphs and punctuation.
                </p>
              </div>
            </div>

            <div class="pt-6">
              <div class="rounded-lg bg-white px-6 pb-8 dark:bg-gray-800">
                <div class="-mt-6 flex justify-center">
                  <div class="inline-flex items-center justify-center rounded-md bg-primary p-3 shadow-lg">
                    <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                </div>
                <h3 class="mt-8 text-lg font-medium tracking-tight text-gray-900 dark:text-white">Auto Chapters</h3>
                <p class="mt-5 text-base text-gray-500 dark:text-gray-400">
                  AI-generated chapters that organize content into logical sections.
                </p>
              </div>
            </div>

            <div class="pt-6">
              <div class="rounded-lg bg-white px-6 pb-8 dark:bg-gray-800">
                <div class="-mt-6 flex justify-center">
                  <div class="inline-flex items-center justify-center rounded-md bg-primary p-3 shadow-lg">
                    <svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <h3 class="mt-8 text-lg font-medium tracking-tight text-gray-900 dark:text-white">Video Screenshots</h3>
                <p class="mt-5 text-base text-gray-500 dark:text-gray-400">
                  Automatic screenshots at key moments to illustrate the content.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- CTA Section -->
    <div class="bg-primary">
      <div class="mx-auto max-w-7xl py-12 px-4 sm:px-6 lg:flex lg:items-center lg:justify-between lg:py-24 lg:px-8">
        <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          <span class="block">Ready to get started?</span>
          <span class="block text-gray-200">Create your account today.</span>
        </h2>
        <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div class="inline-flex rounded-md shadow">
            <Button href="/sign-up" variant="default" size="lg" class="bg-white text-primary hover:bg-gray-100">
              Get Started
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>