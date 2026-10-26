<script setup>
/**
 * Lists every published event automatically. Upcoming events are sorted by
 * date; once an event has ended it moves to "Past events" with no editing.
 * Events ticked "Hide from events hub" never appear here.
 */
const props = defineProps({ blok: Object });
const api = useStoryblokApi();
const version = getVersion();
const events = ref([]);

async function load() {
  const filter = { hide_from_hub: { not_in: 'true' } };
  if (props.blok?.topic) {
    filter.specialisms = { any_in_array: props.blok.topic };
  }
  try {
    const { data } = await api.get('cdn/stories', { version, content_type: 'event', per_page: 50, filter_query: filter });
    events.value = data.stories ?? [];
  }
  catch {
    events.value = [];
  }
}

await load();
watch(() => props.blok?.topic, load);

const upcoming = computed(() => events.value.filter(e => !isPastEvent(e)).sort((a, b) => eventStart(a) - eventStart(b)));
const past = computed(() => events.value.filter(isPastEvent).sort((a, b) => eventStart(b) - eventStart(a)).slice(0, Number(props.blok?.past_limit) || 3));
</script>

<template>
  <section v-editable="blok" class="bg-primary-background py-14 md:py-20">
    <div class="container">
      <h1 class="font-display text-4xl text-primary-dark md:text-5xl">{{ blok?.title || 'Upcoming events' }}</h1>
      <p v-if="blok?.intro" class="mt-4 max-w-2xl text-lg text-primary-dark/75">{{ blok.intro }}</p>
      <div v-if="upcoming.length" class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <ContentCard v-for="e in upcoming" :key="e.uuid" :story="e" />
      </div>
      <p v-else class="mt-10 text-primary-dark/60">No upcoming events right now.</p>

      <template v-if="blok?.show_past !== false && past.length">
        <h2 class="mt-16 font-display text-2xl text-primary-dark">Past events</h2>
        <div class="mt-6 grid gap-6 opacity-80 sm:grid-cols-2 lg:grid-cols-3">
          <ContentCard v-for="e in past" :key="e.uuid" :story="e" />
        </div>
      </template>
    </div>
  </section>
</template>
