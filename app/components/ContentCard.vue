<script setup>
/** One card for an article, video or event, wherever content is listed. */
const props = defineProps({
  story: { type: Object, required: true },
  newTab: { type: Boolean, default: false },
});

const specialismLabels = useDatasourceLabels('specialisms');
const kind = computed(() => contentKind(props.story));
const title = computed(() => contentTitle(props.story));
const image = computed(() => getOptimizedImage(contentImage(props.story), 720, 405));
const past = computed(() => kind.value === 'Event' && isPastEvent(props.story));
const meta = computed(() => {
  if (kind.value === 'Event') {
    const d = eventStart(props.story);
    const when = d ? d.toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' }) : '';
    return [when, props.story.content?.location].filter(Boolean).join(' · ');
  }
  return (props.story.content?.specialisms || []).slice(0, 2).map(v => labelFor(specialismLabels.value, v)).join(' · ');
});
</script>

<template>
  <NuxtLink
    :to="`/${story.full_slug}`"
    :target="newTab ? '_blank' : undefined"
    class="group flex h-full flex-col overflow-hidden rounded-lg border border-primary-dark/10 bg-white transition hover:border-primary-highlight"
  >
    <div class="relative aspect-video overflow-hidden bg-background-2">
      <img v-if="image" :src="image" alt="" class="size-full object-cover transition duration-500 group-hover:scale-[1.03]" />
      <div v-else class="flex size-full items-center justify-center font-display text-3xl text-highlight-2">{{ kind }}</div>
      <span
        class="absolute left-3 top-3 rounded-sm px-2 py-1 text-[11px] font-semibold uppercase tracking-[0.14em]"
        :class="past ? 'bg-primary-dark/80 text-white' : 'bg-white text-primary-dark'"
      >{{ past ? 'Past event' : kind }}</span>
    </div>
    <div class="flex flex-1 flex-col p-5">
      <h3 class="font-display text-xl text-primary-dark group-hover:text-primary-highlight">{{ title }}</h3>
      <p v-if="meta" class="mt-2 text-sm text-primary-dark/65">{{ meta }}</p>
    </div>
  </NuxtLink>
</template>
