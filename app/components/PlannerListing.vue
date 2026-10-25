<script setup>
/**
 * Fetches and lays out planners for a grid or an office hub.
 *
 * The same component backs the PlannerGrid block (manual, by office, by
 * specialism) and the office page, so "create a planner and every list updates"
 * holds in one place. Only active, published planners ever reach the screen.
 */
const props = defineProps({
  mode: { type: String, default: 'manual' },
  office: { type: [String, Object], default: '' },
  planners: { type: Array, default: () => [] },
  specialism: { type: String, default: '' },
  sort: { type: String, default: 'pinned_then_az' },
  limit: { type: [String, Number], default: '' },
  // Overrides the office's own pinned planners (used by the office page, where
  // the editor is changing them live).
  pinned: { type: Array, default: undefined },
  columns: { type: Number, default: 3 },
  ctaLabel: { type: String, default: '' },
  showViewAll: { type: Boolean, default: true },
});

const api = useStoryblokApi();
const version = getVersion();
const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);
const specialismLabels = useDatasourceLabels('specialisms');

const loading = ref(true);
const failed = ref(false);
const list = ref([]);
const officeStory = ref(null);
let requestId = 0;

const officeUuid = computed(() =>
  typeof props.office === 'string' ? props.office : props.office?.uuid || '',
);
const manualKey = computed(() =>
  (props.planners ?? []).map(item => (typeof item === 'string' ? item : item?.uuid)).join(','),
);

async function load() {
  const current = ++requestId;
  loading.value = true;
  failed.value = false;
  try {
    let result = [];
    let office = null;
    if (props.mode === 'by_office') {
      if (officeUuid.value) {
        [result, office] = await Promise.all([
          fetchPlanners(api, { version, office: officeUuid.value }),
          resolveStory(api, props.office, { version }),
        ]);
      }
    }
    else if (props.mode === 'by_specialism') {
      if (props.specialism) {
        result = await fetchPlanners(api, { version, specialism: props.specialism });
      }
    }
    else {
      result = await fetchPlannersByRelation(api, props.planners, { version });
    }
    if (current !== requestId) {
      return;
    }
    list.value = result;
    officeStory.value = office;
  }
  catch {
    if (current === requestId) {
      failed.value = true;
      list.value = [];
    }
  }
  finally {
    if (current === requestId) {
      loading.value = false;
    }
  }
}

watch(
  () => [props.mode, officeUuid.value, props.specialism, manualKey.value],
  load,
  { immediate: true },
);

const pinnedList = computed(() => props.pinned ?? officeStory.value?.content?.pinned_planners ?? []);

const ordered = computed(() => {
  if (props.mode === 'manual') {
    return list.value;
  }
  return sortPlanners(list.value, {
    sort: props.mode === 'by_office' ? props.sort : 'az',
    pinned: pinnedList.value,
  });
});

const max = computed(() => {
  const value = toNumber(props.limit);
  return value && value > 0 ? value : null;
});
const visible = computed(() => (max.value ? ordered.value.slice(0, max.value) : ordered.value));
const hiddenCount = computed(() => ordered.value.length - visible.value.length);

const viewAllLink = computed(() => {
  if (!props.showViewAll || !hiddenCount.value) {
    return null;
  }
  if (props.mode === 'by_office' && officeStory.value?.full_slug) {
    return { to: `/${officeStory.value.full_slug}`, label: `See all ${ordered.value.length} planners in ${officeStory.value.content?.name ?? 'this office'}` };
  }
  if (props.mode === 'by_specialism') {
    return {
      to: { path: '/planners', query: { specialism: props.specialism } },
      label: `See all ${ordered.value.length} planners for ${labelFor(specialismLabels.value, props.specialism).toLowerCase()}`,
    };
  }
  return null;
});

const needsSetup = computed(() => {
  if (props.mode === 'by_office') {
    return !officeUuid.value ? 'Pick an office in the sidebar and the planners based there appear here automatically.' : '';
  }
  if (props.mode === 'by_specialism') {
    return !props.specialism ? 'Pick a specialism in the sidebar and every active planner with that topic appears here automatically.' : '';
  }
  return !props.planners?.length ? 'Pick planners in the sidebar, or switch "How to choose planners" to fill the grid automatically.' : '';
});

const gridClass = computed(() =>
  props.columns >= 4
    ? 'sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
    : 'sm:grid-cols-2 lg:grid-cols-3',
);
</script>

<template>
  <div>
    <!-- Marketer-friendly setup hint. Only ever shown in the Visual Editor. -->
    <div
      v-if="needsSetup && inEditor"
      class="rounded-lg border border-dashed border-primary-highlight bg-white/70 p-8 text-center"
    >
      <p class="font-display text-2xl text-primary-dark">
        Nothing to show yet
      </p>
      <p class="mx-auto mt-2 max-w-md text-sm text-primary-dark/70">
        {{ needsSetup }}
      </p>
    </div>

    <div v-else-if="loading" class="grid gap-5" :class="gridClass" aria-hidden="true">
      <div
        v-for="n in 3"
        :key="n"
        class="flex h-44 animate-pulse overflow-hidden rounded-lg border border-primary-dark/10 bg-white sm:h-96 sm:flex-col"
      >
        <div class="w-28 bg-background-2 sm:h-3/5 sm:w-full"></div>
        <div class="flex-1 space-y-3 p-4">
          <div class="h-3 w-2/3 rounded bg-background-2"></div>
          <div class="h-5 w-1/2 rounded bg-background-2"></div>
        </div>
      </div>
    </div>

    <p v-else-if="failed" class="rounded-lg border border-primary-dark/10 bg-white p-6 text-primary-dark/70">
      We could not load our planners just now. Please refresh the page.
    </p>

    <div
      v-else-if="!visible.length && !needsSetup"
      class="rounded-lg border border-dashed border-primary-dark/20 bg-white/70 p-8 text-center"
    >
      <p class="font-display text-2xl text-primary-dark">
        No planners to show here yet
      </p>
      <p class="mx-auto mt-2 max-w-md text-sm text-primary-dark/70">
        <template v-if="inEditor">
          No active, published planners match. Add a planner, or tick "Active" on an existing one, and they appear here without editing this page.
        </template>
        <template v-else>
          Our team here is growing. You can still
          <NuxtLink to="/planners" class="font-semibold text-primary-highlight underline underline-offset-2">browse all our planners</NuxtLink>.
        </template>
      </p>
    </div>

    <template v-else-if="visible.length">
      <ul class="grid gap-5" :class="gridClass">
        <li v-for="planner in visible" :key="planner.uuid" class="flex min-w-0">
          <PlannerTile :planner="planner" :cta-label="ctaLabel" class="w-full" />
        </li>
      </ul>
      <p v-if="viewAllLink" class="mt-8">
        <NuxtLink
          :to="viewAllLink.to"
          class="focus-ring inline-flex items-center gap-2 border-b border-primary-highlight pb-0.5 text-sm font-semibold text-primary-dark hover:text-highlight-2"
        >
          {{ viewAllLink.label }}
          <span aria-hidden="true">→</span>
        </NuxtLink>
      </p>
    </template>
  </div>
</template>
