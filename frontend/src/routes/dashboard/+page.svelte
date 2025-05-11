<script lang="ts">
    import { Search, Bell } from 'lucide-svelte';
    import { Button } from "bits-ui";
    import { Input } from "$lib/components/ui/input";
    import { 
      Card, 
      CardContent, 
      CardHeader, 
      CardTitle 
    } from "$lib/components/ui/card";
  
    // Example data
    let recentVideos = [
      { id: 1, title: "Getting Started with Stepify", status: "completed", date: "2024-01-15" },
      { id: 2, title: "Advanced Video Processing", status: "processing", date: "2024-01-14" },
      { id: 3, title: "Understanding RAG Systems", status: "failed", date: "2024-01-13" }
    ];
  
    let stats = {
      processedVideos: 45,
      totalTokens: "1.2M",
      averageTime: "2.5 min"
    };
  </script>
  
  <div class="min-h-screen bg-background">
    <!-- Main Navigation -->
    <header class="sticky top-0 z-50 overflow-x-hidden border-b border-border bg-background/75 backdrop-blur-md">
      <div class="container px-4">
        <div class="flex h-[70px] items-center justify-between gap-3">
          <div class="flex items-center gap-1.5">
            <a href="/" class="ml-2 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background">
              <h1 class="text-center text-4xl font-bold leading-tight tracking-tighter md:text-4xl lg:leading-[1.1]">stepify.tech</h1>
            </a>
          </div>
          <div class="flex items-center justify-end gap-2.5">
            <Button.Root
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex h-10 items-center justify-center whitespace-nowrap rounded-[9px] bg-muted px-4 text-sm font-semibold text-foreground ring-offset-background transition-colors hover:bg-dark-10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Report an issue
            </Button.Root>
          </div>
        </div>
      </div>
    </header>
  
    <div class="flex min-h-[calc(100vh-70px)]">
      <!-- Sidebar Navigation -->
      <aside class="w-64 border-r bg-background">
        <nav class="p-4 space-y-1">
          <a 
            href="/dashboard" 
            class="flex items-center space-x-2 rounded-lg px-3 py-2 text-sm font-medium bg-accent"
          >
            <span>Dashboard</span>
          </a>
          <a 
            href="/videos" 
            class="flex items-center space-x-2 rounded-lg px-3 py-2 text-sm font-medium hover:bg-accent/50"
          >
            <span>Videos</span>
          </a>
          <a 
            href="/history" 
            class="flex items-center space-x-2 rounded-lg px-3 py-2 text-sm font-medium hover:bg-accent/50"
          >
            <span>History</span>
          </a>
        </nav>
      </aside>
  
      <!-- Main Content -->
      <main class="flex-1 p-6">
        <div class="max-w-6xl mx-auto">
          <!-- Search Bar -->
          <div class="mb-6">
            <div class="relative">
              <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search videos..."
                class="w-full pl-9"
              />
            </div>
          </div>
  
          <!-- Stats Grid -->
          <div class="grid gap-4 md:grid-cols-3 mb-8">
            <Card>
              <CardHeader>
                <CardTitle class="text-base font-medium">Processed Videos</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{stats.processedVideos}</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle class="text-base font-medium">Total Tokens Used</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{stats.totalTokens}</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle class="text-base font-medium">Average Processing Time</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">{stats.averageTime}</div>
              </CardContent>
            </Card>
          </div>
  
          <!-- Recent Videos -->
          <Card>
            <CardHeader>
              <CardTitle>Recent Videos</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-6">
                {#each recentVideos as video}
                  <div class="flex items-center justify-between">
                    <div>
                      <h3 class="font-medium">{video.title}</h3>
                      <p class="text-sm text-muted-foreground">{video.date}</p>
                    </div>
                    <div class="flex items-center gap-4">
                      <span class={`text-sm ${
                        video.status === 'completed' ? 'text-green-500' :
                        video.status === 'processing' ? 'text-blue-500' :
                        'text-red-500'
                      }`}>
                        {video.status}
                      </span>
                    </div>
                  </div>
                {/each}
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  </div>