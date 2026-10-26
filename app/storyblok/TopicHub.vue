<script setup>
/**
 * Uniform topic hub: the editor picks one Topic and the hub assembles itself
 * (planners, finder, latest content, events). Extra sections are free-form.
 */
const props = defineProps({ blok: Object, uuid: String });
const hero = computed(() => getOptimizedImage(props.blok?.hero_image, 1600, 700));
const seoBlok = computed(() => props.blok?.seo?.[0]);
const topic = computed(() => props.blok?.topic || '');
const labels = useDatasourceLabels('specialisms');
const topicLabel = computed(() => (topic.value ? labelFor(labels.value, topic.value) : ''));
</script>

<template>
  <div v-editable="blok">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <section class="relative overflow-hidden bg-primary-dark text-white">
      <img v-if="hero" :src="hero" alt="" class="absolute inset-0 size-full object-cover opacity-35" />
      <div class="container relative py-20 md:py-28">
        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-highlight-1">Topic hub<span v-if="topicLabel"> · {{ topicLabel }}</span></p>
        <h1 class="mt-3 max-w-3xl font-hero text-5xl font-extralight md:text-6xl">{{ blok?.title }}</h1>
        <p v-if="blok?.intro" class="mt-5 max-w-2xl text-lg text-white/85">{{ blok.intro }}</p>
      </div>
    </section>

    <template v-if="topic">
      <OnwardJourney
        v-if="blok?.show_content !== false"
        :blok="{ _uid: 'hub-content', component: 'onward_journey', title: `Latest on ${topicLabel.toLowerCase()}`, mode: 'latest', topic, content_types: ['article-page', 'video_page'], limit: '3' }"
        :uuid="uuid"
      />
      <PlannerGrid
        v-if="blok?.show_planners !== false"
        :blok="{ _uid: 'hub-planners', component: 'planner_grid', title: `Planners who specialise in ${topicLabel.toLowerCase()}`, mode: 'by_specialism', specialism: topic, sort: 'az', limit: '6' }"
      />
      <PlannerFinder
        v-if="blok?.show_finder !== false"
        :blok="{ _uid: 'hub-finder', component: 'planner_finder', title: 'Find the right planner for you', preset_specialism: topic, max_results: '3' }"
      />
      <EventsHub
        v-if="blok?.show_events !== false"
        :blok="{ _uid: 'hub-events', component: 'events_hub', title: 'Upcoming events', topic, show_past: false }"
      />
    </template>
    <div v-else class="container py-16 text-primary-dark/60">Pick a Topic to fill this hub automatically.</div>

    <StoryblokComponent v-for="b in blok?.body || []" :key="b._uid" :blok="b" />
  </div>
</template>
