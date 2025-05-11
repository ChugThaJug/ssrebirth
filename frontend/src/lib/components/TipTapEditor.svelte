<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Editor } from '@tiptap/core';
    import Document from '@tiptap/extension-document';
    import Paragraph from '@tiptap/extension-paragraph';
    import Text from '@tiptap/extension-text';
    import HardBreak from '@tiptap/extension-hard-break';
  
    export let content = '';
    export let onUpdate: (newContent: string) => void;
  
    let element: HTMLElement;
    let editor: Editor;
  
    onMount(() => {
      editor = new Editor({
        element: element,
        extensions: [
          Document,
          Paragraph,
          Text,
          HardBreak,
        ],
        content: content,
        editorProps: {
          attributes: {
            class: 'prose prose-sm max-w-none focus:outline-none',
          },
        },
        onUpdate: ({ editor }) => {
          const newContent = editor.getText();
          onUpdate(newContent);
        },
      });
    });
  
    onDestroy(() => {
      if (editor) {
        editor.destroy();
      }
    });
  </script>
  
  <div bind:this={element} class="border border-gray-300 rounded-md p-2 min-h-[200px]" />
  
  <style>
    :global(.ProseMirror p) {
      margin: 0;
    }
  </style>