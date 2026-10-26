<script setup>
const props = defineProps({ blok: Object, uuid: String });
const hosts = computed(() => (props.blok?.hosts || []).filter(isResolvedStory));
const image = computed(() => getOptimizedImage(props.blok?.image, 1400, 700));
const booking = computed(() => getLinkUrl(props.blok?.booking_url));
const seoBlok = computed(() => props.blok?.seo?.[0]);
// Past status is computed from the date, so nobody has to edit old events.
const past = computed(() => isPastEvent({ content: props.blok }));
const officeUuid = computed(() => {
  const v = props.blok?.office;
  return typeof v === 'string' ? v : v?.uuid || '';
});
</script>

<template>
  <article v-editable="blok" class="bg-primary-background">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <div class="container py-12">
      <p class="text-xs font-semibold uppercase tracking-[0.16em] text-highlight-2">
        Event
        <span v-if="past" class="ml-2 rounded-sm bg-primary-dark px-2 py-1 text-white">Past event</span>
      </p>
      <h1 class="mt-2 font-display text-4xl text-primary-dark md:text-5xl">{{ blok?.title }}</h1>
      <p v-if="blok?.start" class="mt-3 text-primary-dark/70">
        {{ new Date(blok.start).toLocaleString('en-GB', { dateStyle: 'long', timeStyle: 'short' }) }}
        <span v-if="blok?.location"> · {{ blok.location }}</span>
      </p>
      <img v-if="image" :src="image" alt="" class="mt-8 w-full rounded-lg object-cover" />
      <div v-if="blok?.description" class="prose prose-lg mt-8 max-w-3xl">
        <StoryblokRichText :document="blok.description" />
      </div>
      <p v-if="past" class="mt-8 text-primary-dark/70">This event has taken place. See our upcoming events.</p>
      <a
        v-else-if="booking"
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
      <div v-if="officeUuid" class="mt-12">
        <h2 class="mb-6 font-display text-2xl text-primary-dark">Getting there</h2>
        <OfficeMap :blok="{ _uid: 'event-map', component: 'office_map', office: officeUuid, show_directions: true }" />
      </div>
    </div>
    <OnwardJourney v-if="blok?.onward?.[0]" :blok="blok.onward[0]" :uuid="uuid" />
  </article>
</template>
