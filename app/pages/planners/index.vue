<script setup>
const api = useStoryblokApi();
const version = getVersion();
const offices = useOffices();
const specialisms = useDatasource('specialisms');

const q = ref('');
const officeFilter = ref('');
const specialismFilter = ref('');
const preferenceFilter = ref('');
const planners = ref([]);
const loading = ref(true);

async function load() {
  loading.value = true;
  try {
    let list = await loadAllPlanners(api, version);
    if (officeFilter.value) {
      list = list.filter((p) => {
        const o = officeFor(p);
        return o?.uuid === officeFilter.value || p.content?.office === officeFilter.value;
      });
    }
    if (specialismFilter.value) {
      list = list.filter(p => (p.content?.specialisms || []).includes(specialismFilter.value));
    }
    if (preferenceFilter.value) {
      list = list.filter(p => (p.content?.meeting_preferences || []).includes(preferenceFilter.value));
    }
    if (q.value.trim()) {
      const needle = q.value.trim().toLowerCase();
      list = list.filter(p => plannerFullName(p.content).toLowerCase().includes(needle));
    }
    planners.value = sortPlanners(list, { sort: 'az' });
  }
  finally {
    loading.value = false;
  }
}

watch([officeFilter, specialismFilter, preferenceFilter], load, { immediate: true });
let searchTimer;
watch(q, () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(load, 200);
});

useHead({ title: 'Our wealth planners | Succession Wealth' });
</script>

<template>
  <div class="bg-primary-background">
    <section class="bg-primary-dark text-white">
      <div class="container py-16 md:py-20">
        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-primary-highlight">About us</p>
        <h1 class="mt-3 font-display text-4xl font-medium md:text-5xl">Our wealth planners</h1>
        <p class="mt-4 max-w-2xl text-white/75">
          Find a trusted local adviser. Filter by office, specialism or how you prefer to meet.
        </p>
      </div>
    </section>

    <section class="container py-10">
      <div class="mb-8 grid gap-3 rounded-lg bg-white p-4 shadow-sm sm:grid-cols-2 lg:grid-cols-4">
        <label class="block text-sm">
          <span class="mb-1 block text-xs font-semibold uppercase tracking-wider text-highlight-2">Search</span>
          <input v-model="q" type="search" placeholder="Search by name" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2" />
        </label>
        <label class="block text-sm">
          <span class="mb-1 block text-xs font-semibold uppercase tracking-wider text-highlight-2">Office</span>
          <select v-model="officeFilter" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2">
            <option value="">All offices</option>
            <option v-for="o in offices" :key="o.uuid" :value="o.uuid">{{ o.content?.name || o.name }}</option>
          </select>
        </label>
        <label class="block text-sm">
          <span class="mb-1 block text-xs font-semibold uppercase tracking-wider text-highlight-2">Specialism</span>
          <select v-model="specialismFilter" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2">
            <option value="">All topics</option>
            <option v-for="s in specialisms" :key="s.value" :value="s.value">{{ s.name }}</option>
          </select>
        </label>
        <label class="block text-sm">
          <span class="mb-1 block text-xs font-semibold uppercase tracking-wider text-highlight-2">Meeting</span>
          <select v-model="preferenceFilter" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2">
            <option value="">Any preference</option>
            <option v-for="(label, value) in MEETING_LABELS" :key="value" :value="value">{{ label }}</option>
          </select>
        </label>
      </div>

      <p v-if="loading" class="text-sm text-primary-dark/60">Loading planners…</p>
      <p v-else-if="!planners.length" class="text-sm text-primary-dark/60">No planners match these filters.</p>
      <div v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <PlannerTile v-for="p in planners" :key="p.uuid" :planner="p" />
      </div>
    </section>

    <PlannerFinder
      :blok="{
        component: 'planner_finder',
        title: 'Not sure who to choose?',
        intro: 'Answer three short questions and we will match you with local planners.',
        max_results: 6,
        _uid: 'listing-finder',
      }"
    />
  </div>
</template>
