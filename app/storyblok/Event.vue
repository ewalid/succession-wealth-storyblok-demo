<script setup>
const props = defineProps({ blok: Object, uuid: String });
const hosts = computed(() => (props.blok?.hosts || []).filter(isResolvedStory));
const image = computed(() => getOptimizedImage(props.blok?.image, 1400, 700));
const booking = computed(() => getLinkUrl(props.blok?.booking_url));
const seoBlok = computed(() => props.blok?.seo?.[0]);
</script>

<template>
  <article v-editable="blok" class="bg-primary-background">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <div class="container py-12">
      <p class="text-xs font-semibold uppercase tracking-[0.16em] text-highlight-2">Event</p>
      <h1 class="mt-2 font-display text-4xl text-primary-dark md:text-5xl">{{ blok?.title }}</h1>
      <p v-if="blok?.start" class="mt-3 text-primary-dark/70">
        {{ new Date(blok.start).toLocaleString('en-GB', { dateStyle: 'long', timeStyle: 'short' }) }}
        <span v-if="blok?.location"> · {{ blok.location }}</span>
      </p>
      <img v-if="image" :src="image" alt="" class="mt-8 w-full rounded-lg object-cover" />
      <div v-if="blok?.description" class="prose prose-lg mt-8 max-w-3xl">
        <StoryblokRichText :document="blok.description" />
      </div>
      <a
        v-if="booking"
        :href="booking"
        target="_blank"
        rel="noopener"
        class="mt-8 inline-flex rounded-sm bg-primary-highlight px-5 py-2.5 text-sm font-semibold text-white"
      >Book a place</a>
      <div v-if="hosts.length" class="mt-12">
        <h2 class="mb-6 font-display text-2xl text-primary-dark">Hosted by</h2>
        <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <PlannerTile v-for="h in hosts" :key="h.uuid" :planner="h" />
        </div>
      </div>
    </div>
  </article>
</template>
