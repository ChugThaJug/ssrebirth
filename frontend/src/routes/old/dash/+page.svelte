<script lang="ts">
  import { Search, ChevronDown, Copy } from 'lucide-svelte';
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import * as Accordion from "$lib/components/ui/accordion";

  let searchQuery = "";
  let filterQuery = "";
  let sortOrder = "Newest";

  const models = [
    {
      name: "xAI: Grok 2 mini",
      description: "Grok 2 Mini is xAI's fast, lightweight language model that offers a balance between speed and answer quality. To use the stronger model, see Grok 2. For more information, see the launch ...",
      creator: "x-ai",
      contextLength: "33K context",
      inputTokens: "$4.2/M input tokens",
      outputTokens: "$6.9/M output tokens",
      totalTokens: "5.39M tokens"
    },
    {
      name: "xAI: Grok 2",
      description: "Grok 2 is xAI's frontier language model with state-of-the-art reasoning capabilities, best for complex and multi-step use cases. To use a faster version, see Grok 2 Mini. For more information...",
      creator: "x-ai",
      contextLength: "33K context",
      inputTokens: "$4.2/M input tokens",
      outputTokens: "$6.9/M output tokens",
      totalTokens: "42.7M tokens"
    },
    {
      name: "Inflection: Inflection 3 Productivity",
      description: "Inflection 3 Productivity is a powerful language model designed for...",
      creator: "Inflection",
      contextLength: "32K context",
      inputTokens: "$4.0/M input tokens",
      outputTokens: "$6.5/M output tokens",
      totalTokens: "3.75M tokens"
    }
  ];

  function copyModelName(name: string) {
    navigator.clipboard.writeText(name);
    // You might want to add a toast notification here
  }
</script>

<div class="flex h-screen bg-white">
  <!-- Sidebar -->
  <aside class="w-64 border-r p-4">
    <Accordion.Root type="single" collapsible>
      <Accordion.Item value="modality">
        <Accordion.Trigger class="flex w-full items-center justify-between">
          Modality
          <ChevronDown class="h-4 w-4" />
        </Accordion.Trigger>
        <Accordion.Content>
          <div class="mt-2 space-y-2">
            <label class="flex items-center">
              <input type="checkbox" class="mr-2" />
              Text to Text
            </label>
            <label class="flex items-center">
              <input type="checkbox" class="mr-2" />
              Text & Image to Text
            </label>
          </div>
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="context-length">
        <Accordion.Trigger class="flex w-full items-center justify-between">
          Context length
          <ChevronDown class="h-4 w-4" />
        </Accordion.Trigger>
        <Accordion.Content>
          <input type="range" class="w-full" min="4000" max="1000000" step="1000" />
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="prompt-pricing">
        <Accordion.Trigger class="flex w-full items-center justify-between">
          Prompt pricing
          <ChevronDown class="h-4 w-4" />
        </Accordion.Trigger>
        <Accordion.Content>
          <input type="range" class="w-full" min="0" max="10" step="0.1" />
        </Accordion.Content>
      </Accordion.Item>

      <Accordion.Item value="series">
        <Accordion.Trigger class="flex w-full items-center justify-between">
          Series
          <ChevronDown class="h-4 w-4" />
        </Accordion.Trigger>
        <Accordion.Content>
          <div class="mt-2 space-y-2">
            <label class="flex items-center">
              <input type="checkbox" class="mr-2" />
              GPT
            </label>
            <label class="flex items-center">
              <input type="checkbox" class="mr-2" />
              Claude
            </label>
            <label class="flex items-center">
              <input type="checkbox" class="mr-2" />
              Gemini
            </label>
          </div>
        </Accordion.Content>
      </Accordion.Item>
    </Accordion.Root>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 p-8">
    <header class="mb-8 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <h1 class="text-2xl font-bold">OpenRouter</h1>
        <div class="relative">
          <Search class="absolute left-2 top-1/2 h-4 w-4 -translate-y-1/2 transform text-gray-400" />
          <Input type="text" placeholder="Search models" class="pl-8" bind:value={searchQuery} />
        </div>
      </div>
      <nav class="flex items-center space-x-4">
        <a href="" class="text-blue-600">Browse</a>
        <a href="" class="text-gray-600">Chat</a>
        <a href="" class="text-gray-600">Rankings</a>
        <a href="" class="text-gray-600">Docs</a>
        <Button>Sign in</Button>
      </nav>
    </header>

    <div class="mb-4 flex items-center justify-between">
      <h2 class="text-xl font-semibold">Models</h2>
      <span class="text-sm text-gray-500">250 models</span>
    </div>

    <div class="mb-4 flex items-center justify-between">
      <Input type="text" placeholder="Filter models" class="w-64" bind:value={filterQuery} />
      <select bind:value={sortOrder} class="rounded border p-2">
        <option>Newest</option>
        <option>Oldest</option>
        <option>Most popular</option>
      </select>
    </div>

    <div class="space-y-4">
      {#each models as model}
        <div class="rounded border p-4">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="text-lg font-semibold">{model.name}</h3>
              <p class="mt-1 text-sm text-gray-600">{model.description}</p>
            </div>
            <Button variant="outline" size="sm" on:click={() => copyModelName(model.name)}>
              <Copy class="mr-2 h-4 w-4" />
              Copy
            </Button>
          </div>
          <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500">
            <span>by {model.creator}</span>
            <span>{model.contextLength}</span>
            <span>{model.inputTokens}</span>
            <span>{model.outputTokens}</span>
          </div>
          <div class="mt-2 text-right text-sm font-semibold">{model.totalTokens}</div>
        </div>
      {/each}
    </div>
  </main>
</div>