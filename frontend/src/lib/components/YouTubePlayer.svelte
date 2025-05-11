<script lang="ts">
    import { onMount, createEventDispatcher } from 'svelte';
    import type { SvelteComponentTyped } from "svelte";
  
    export let videoId: string;
  
    const dispatch = createEventDispatcher<{
      ready: { target: any };
      timeUpdate: number;
    }>();
  
    let playerElement: HTMLDivElement;
  
    declare global {
      interface Window {
        onYouTubeIframeAPIReady: () => void;
        YT: {
          Player: new (
            element: HTMLElement | string,
            config: {
              videoId: string;
              playerVars?: Record<string, any>;
              events?: Record<string, (event: any) => void>;
            }
          ) => any;
          PlayerState: {
            PLAYING: number;
          };
        };
      }
    }
  
    onMount(() => {
      let player: any;
      let timeUpdateInterval: NodeJS.Timer;
  
      function initPlayer() {
        player = new window.YT.Player(playerElement, {
          videoId,
          playerVars: {
            modestbranding: 1,
            playsinline: 1,
            rel: 0,
            autoplay: 0
          },
          events: {
            onReady: (event: any) => {
              dispatch('ready', { target: event.target });
            },
            onStateChange: (event: any) => {
              if (event.data === window.YT.PlayerState.PLAYING) {
                timeUpdateInterval = setInterval(() => {
                  const time = player.getCurrentTime();
                  dispatch('timeUpdate', time);
                }, 1000);
              } else {
                if (timeUpdateInterval) {
                  clearInterval(timeUpdateInterval);
                }
              }
            }
          }
        });
      }
  
      // Load YouTube IFrame API if not already loaded
      if (!window.YT) {
        const tag = document.createElement('script');
        tag.src = 'https://www.youtube.com/iframe_api';
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag);
        window.onYouTubeIframeAPIReady = initPlayer;
      } else {
        initPlayer();
      }
  
      return () => {
        if (timeUpdateInterval) {
          clearInterval(timeUpdateInterval);
        }
        if (player) {
          player.destroy();
        }
      };
    });
  </script>
  
  <div bind:this={playerElement} class="w-full h-full" />