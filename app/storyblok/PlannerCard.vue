<script setup>
const props = defineProps({ blok: Object, index: Number });

const api = useStoryblokApi();
const version = getVersion();
const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);

const planner = ref(null);
const loading = ref(false);
let requestId = 0;

const plannerKey = computed(() => {
  const value = props.blok?.planner;
  return typeof value === 'string' ? value : value?.uuid || '';
});

watch(
  () => [plannerKey.value, props.blok?.planner],
  async () => {
    const current = ++requestId;
    if (!plannerKey.value) {
      planner.value = null;
      return;
    }
    loading.value = true;
    const story = await resolveStory(api, props.blok?.planner, {
      version,
      resolve_relations: 'planner.office',
    });
    if (current === requestId) {
      planner.value = story;
      loading.value = false;
    }
  },
  { immediate: true },
);

const active = computed(() => isActivePlanner(planner.value));
// On the live site an empty, unpublished or inactive card renders nothing at
// all, so a half-finished block never leaves a hole in the page.
const visible = computed(() => inEditor.value || (!!planner.value && active.value));
</script>

<template>
  <section v-if="visible" v-editable="blok" class="py-8">
    <div class="container">
      <div class="mx-auto max-w-sm sm:max-w-xs">
        <div
          v-if="!plannerKey"
          class="rounded-lg border border-dashed border-primary-highlight bg-white/70 p-8 text-center"
        >
          <p class="font-display text-2xl text-primary-dark">
            Pick a planner in the sidebar
          </p>
          <p class="mt-2 text-sm text-primary-dark/70">
            Their photo, name, title and specialisms appear here automatically.
          </p>
        </div>

        <p
          v-else-if="loading && !planner"
          class="rounded-lg border border-primary-dark/10 bg-white p-6 text-sm text-primary-dark/60"
        >
          Loading planner…
        </p>

        <div
          v-else-if="!planner"
          class="rounded-lg border border-dashed border-primary-dark/30 bg-white/70 p-6 text-center text-sm text-primary-dark/70"
        >
          This planner is not published yet, so the card is hidden on the live site.
        </div>

        <template v-else>
          <p
            v-if="!active"
            class="mb-2 rounded-sm bg-highlight-1/30 px-3 py-2 text-xs font-semibold text-primary-dark"
          >
            This planner is inactive, so the card is hidden on the live site.
          </p>
          <PlannerTile
            :planner="planner"
            :cta-label="blok?.cta_label"
            :show-specialisms="blok?.show_specialisms !== false"
            :show-office="blok?.show_office !== false"
          />
        </template>
      </div>
    </div>
  </section>
</template>
