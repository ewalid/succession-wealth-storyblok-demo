<script setup>
const props = defineProps({ blok: Object, uuid: String });
const featured = computed(() => (props.blok?.featured_planners || []).filter(isResolvedStory));
const videoUrl = computed(() => props.blok?.video?.filename || getLinkUrl(props.blok?.video));
// A YouTube link in the Video field plays as an embed; anything else as a file.
const youtubeId = computed(() => (videoUrl.value || '').match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([\w-]{11})/)?.[1] || '');
const thumb = computed(() => getOptimizedImage(props.blok?.thumbnail, 1400, 788));
const seoBlok = computed(() => props.blok?.seo?.[0]);
</script>

<template>
  <article v-editable="blok" class="bg-primary-background" style="--primary-dark:#121213;--color-primary-dark:#121213;">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <div class="container py-12">
      <p class="text-xs font-semibold uppercase tracking-[0.16em] text-highlight-2">Video</p>
      <h1 class="mt-2 font-display text-4xl text-primary-dark md:text-5xl">{{ blok?.title }}</h1>
      <div class="mt-8 overflow-hidden rounded-lg bg-primary-dark">
        <iframe v-if="youtubeId" :src="`https://www.youtube-nocookie.com/embed/${youtubeId}?rel=0`" :title="blok?.title || 'Video'" allow="encrypted-media; fullscreen" allowfullscreen class="aspect-video w-full"></iframe>
        <video v-else-if="videoUrl" :src="videoUrl" :poster="thumb" controls class="aspect-video w-full"></video>
        <img v-else-if="thumb" :src="thumb" alt="" class="aspect-video w-full object-cover opacity-80" />
        <div v-else class="flex aspect-video items-center justify-center text-white/70">Add a video file or YouTube link in Storyblok</div>
      </div>
      <div v-if="blok?.description" class="prose prose-lg mt-8 max-w-3xl">
        <StoryblokRichText :document="blok.description" />
      </div>
      <div v-if="featured.length" class="mt-12">
        <h2 class="mb-6 font-display text-2xl text-primary-dark">Featured planners</h2>
        <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <PlannerTile v-for="p in featured" :key="p.uuid" :planner="p" />
        </div>
      </div>
    </div>
    <OnwardJourney v-if="blok?.onward?.[0]" :blok="blok.onward[0]" :uuid="uuid" />
  </article>
</template>
