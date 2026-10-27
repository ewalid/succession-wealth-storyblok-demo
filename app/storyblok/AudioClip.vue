<script setup>
/**
 * Audio or podcast episode: an uploaded audio file plays in the browser's own
 * player; a Spotify, Apple Podcasts or SoundCloud link plays as their embed.
 */
const props = defineProps({ blok: Object });
const file = computed(() => props.blok?.audio?.filename || '');
const embed = computed(() => {
  const url = (getLinkUrl(props.blok?.podcast_url) || '').trim();
  if (/open\.spotify\.com\//.test(url)) {
    return { src: url.replace('open.spotify.com/', 'open.spotify.com/embed/'), height: 152 };
  }
  if (/podcasts\.apple\.com\//.test(url)) {
    return { src: url.replace('podcasts.apple.com', 'embed.podcasts.apple.com'), height: 175 };
  }
  if (/soundcloud\.com\//.test(url)) {
    return { src: `https://w.soundcloud.com/player/?url=${encodeURIComponent(url)}&color=%238b6f4b&visual=false`, height: 166 };
  }
  return null;
});
</script>

<template>
  <section v-editable="blok" class="bg-primary-background">
    <div class="container max-w-3xl py-12">
      <div class="rounded-sm border border-[#121213]/10 bg-white p-6 md:p-8">
        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#6b5434]">{{ blok?.label || 'Listen' }}</p>
        <h2 v-if="blok?.title" class="mt-2 font-display text-2xl text-[#121213] md:text-3xl">{{ blok.title }}</h2>
        <p v-if="blok?.description" class="mt-3 text-[#121213]/75">{{ blok.description }}</p>
        <audio v-if="file" :src="file" controls preload="metadata" class="mt-6 w-full"></audio>
        <iframe
          v-else-if="embed"
          :src="embed.src"
          :height="embed.height"
          :title="blok?.title || 'Podcast'"
          allow="autoplay; clipboard-write; encrypted-media; fullscreen"
          loading="lazy"
          class="mt-6 w-full rounded-sm border-0"
        ></iframe>
        <p v-else class="mt-6 rounded-sm bg-[#f3f1ed] px-4 py-3 text-sm text-[#121213]/60">Add an audio file, or a Spotify, Apple Podcasts or SoundCloud link.</p>
        <p v-if="blok?.duration" class="mt-3 text-xs text-[#121213]/50">{{ blok.duration }}</p>
      </div>
    </div>
  </section>
</template>
