<script setup>
const props = defineProps({ blok: Object, uuid: String, exclude: { type: Array, default: () => [] } });
const api = useStoryblokApi();
const version = getVersion();
const stories = ref([]);

const authorUuid = computed(() => {
  const v = props.blok?.author;
  return typeof v === 'string' ? v : v?.uuid || '';
});

async function load() {
  const b = props.blok || {};
  stories.value = b.mode === 'pinned'
    ? await fetchStoriesByUuids(api, (b.items || []).map(i => (typeof i === 'string' ? i : i?.uuid)), { version })
    : await fetchContentFeed(api, {
      version,
      topic: b.topic,
      author: authorUuid.value,
      types: b.content_types,
      limit: b.limit,
      exclude: [props.uuid, ...props.exclude].filter(Boolean),
    });
}

await load();
watch(() => JSON.stringify([props.blok?.mode, props.blok?.items, props.blok?.topic, authorUuid.value, props.blok?.content_types, props.blok?.limit]), load);
</script>

<template>
  <section v-editable="blok" class="bg-primary-background py-14">
    <div class="container">
      <h2 class="mb-8 font-display text-3xl text-primary-dark">{{ blok?.title || 'Where to go next' }}</h2>
      <div v-if="stories.length" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <ContentCard v-for="s in stories" :key="s.uuid" :story="s" :new-tab="!!blok?.open_in_new_tab" />
      </div>
      <p v-else class="text-primary-dark/60">No published content matches these settings yet.</p>
    </div>
  </section>
</template>
