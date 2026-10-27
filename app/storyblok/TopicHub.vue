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

// Hero style: editors pick layout, background colour, overlay strength and alignment
// so the headline stays readable on any photo.
const layout = computed(() => props.blok?.hero_layout || 'overlay');
const BACKGROUNDS = {
  dark: { rgb: '18, 18, 19', text: 'light' },
  bronze: { rgb: '107, 84, 52', text: 'light' },
  cream: { rgb: '243, 241, 237', text: 'dark' },
};
const OVERLAY = { strong: 0.8, medium: 0.6, light: 0.35, none: 0 };
const bg = computed(() => BACKGROUNDS[props.blok?.hero_background] || BACKGROUNDS.dark);
const centered = computed(() => props.blok?.hero_text_align === 'center');
const darkText = computed(() => bg.value.text === 'dark');
const overlayStyle = computed(() => {
  const a = OVERLAY[props.blok?.hero_overlay] ?? OVERLAY.strong;
  const c = bg.value.rgb;
  // Left-aligned text gets a gradient so the right of the photo stays visible.
  return centered.value
    ? { background: `rgba(${c}, ${a})` }
    : { background: `linear-gradient(90deg, rgba(${c}, ${a}) 0%, rgba(${c}, ${a * 0.85}) 45%, rgba(${c}, ${a * 0.35}) 100%)` };
});
const solidStyle = computed(() => ({ background: `rgb(${bg.value.rgb})` }));

// "[topic]" in the title or intro is replaced with the chosen topic.
function fillTopic(value) {
  if (typeof value === 'string') {
    return topicLabel.value ? value.split('[topic]').join(topicLabel.value.toLowerCase()) : value;
  }
  if (Array.isArray(value)) {
    return value.map(fillTopic);
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, k === 'text' || typeof v === 'object' ? fillTopic(v) : v]));
  }
  return value;
}
const title = computed(() => fillTopic(props.blok?.title || ''));
const intro = computed(() => fillTopic(props.blok?.intro));
</script>

<template>
  <div v-editable="blok">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <!-- Split: text on a solid colour, photo beside it -->
    <section v-if="layout === 'split'" :style="solidStyle" :class="darkText ? 'text-[#121213]' : 'text-white'">
      <div class="container grid items-center gap-10 py-14 md:grid-cols-2 md:py-20">
        <div :class="centered ? 'text-center' : ''">
          <p class="text-xs font-semibold uppercase tracking-[0.18em] opacity-75">Topic hub<span v-if="topicLabel"> · {{ topicLabel }}</span></p>
          <h1 class="mt-3 font-hero text-4xl font-light md:text-5xl">{{ title }}</h1>
          <RichText v-if="hasRichText(intro)" :value="intro" class="mt-5 text-lg opacity-90" />
        </div>
        <img v-if="hero" :src="hero" alt="" class="aspect-[4/3] w-full rounded-sm object-cover" />
      </div>
    </section>

    <!-- Overlay (photo behind text) or text only (solid colour) -->
    <section
      v-else
      class="relative isolate overflow-hidden"
      :style="solidStyle"
      :class="darkText ? 'text-[#121213]' : 'text-white'"
    >
      <template v-if="layout !== 'text_only' && hero">
        <img :src="hero" alt="" class="absolute inset-0 -z-10 size-full object-cover" />
        <div class="absolute inset-0 -z-10" :style="overlayStyle"></div>
      </template>
      <div class="container relative py-20 md:py-28" :class="centered ? 'text-center' : ''">
        <p class="text-xs font-semibold uppercase tracking-[0.18em] opacity-80" :class="darkText ? '' : 'drop-shadow'">Topic hub<span v-if="topicLabel"> · {{ topicLabel }}</span></p>
        <h1 class="mt-3 max-w-3xl font-hero text-5xl font-light md:text-6xl" :class="[centered ? 'mx-auto' : '', darkText ? '' : 'drop-shadow-md']">{{ title }}</h1>
        <RichText v-if="hasRichText(intro)" :value="intro" class="mt-5 max-w-2xl text-lg" :class="[centered ? 'mx-auto' : '', darkText ? 'opacity-85' : 'opacity-95 drop-shadow']" />
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
