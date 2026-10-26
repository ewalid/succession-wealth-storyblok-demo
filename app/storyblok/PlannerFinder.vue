<script setup>
const props = defineProps({ blok: Object, index: Number });

const api = useStoryblokApi();
const version = getVersion();
const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);
const specialisms = useDatasource('specialisms');

const stored = readFinderAnswers();
const postcode = ref(stored.postcode || '');
const preference = ref(
  stored.preference
  || props.blok?.default_preference
  || '',
);
const topics = ref(
  stored.topics?.length
    ? [...stored.topics]
    : (props.blok?.preset_specialism ? [props.blok.preset_specialism] : []),
);

const loading = ref(false);
const searched = ref(false);
const error = ref('');
const results = ref([]);
const fallback = ref(false);
const maxResults = computed(() => {
  const n = Number(props.blok?.max_results);
  return Number.isFinite(n) && n > 0 ? n : 6;
});

watch(
  () => props.blok?.preset_specialism,
  (value) => {
    if (value && !topics.value.includes(value)) {
      topics.value = [...topics.value, value];
    }
  },
);

function toggleTopic(value) {
  if (topics.value.includes(value)) {
    topics.value = topics.value.filter(t => t !== value);
  }
  else {
    topics.value = [...topics.value, value];
  }
}

async function search() {
  error.value = '';
  loading.value = true;
  searched.value = true;
  try {
    const pc = normalisePostcode(postcode.value);
    if (!pc) {
      error.value = 'Enter a UK postcode to find planners near you.';
      results.value = [];
      return;
    }
    let origin = null;
    try {
      origin = await geocodePostcode(pc);
    }
    catch (e) {
      error.value = e?.code === 'not-found'
        ? 'We could not find that postcode. Check it and try again.'
        : 'Postcode lookup is unavailable right now. Try again in a moment.';
      results.value = [];
      return;
    }

    saveFinderAnswers({
      postcode: pc,
      preference: preference.value,
      topics: topics.value,
    });
    captureAttribution();

    const planners = await loadAllPlanners(api, version);
    const scored = scorePlanners(planners, {
      origin,
      preference: preference.value,
      topics: topics.value,
    });
    fallback.value = scored.fallback;
    results.value = scored.results.slice(0, maxResults.value);
  }
  finally {
    loading.value = false;
  }
}

onMounted(() => {
  if (postcode.value) {
    search();
  }
});
</script>

<template>
  <section v-editable="blok" class="page-section bg-primary-dark text-white">
    <div class="container">
      <header class="mx-auto mb-10 max-w-2xl text-center">
        <h2 class="font-display text-3xl font-medium md:text-4xl">
          {{ blok?.title || 'Find the right planner' }}
        </h2>
        <RichText v-if="hasRichText(blok?.intro)" :value="blok.intro" class="mt-3 text-white/75" />
        <p v-else class="mt-3 text-white/75">
          Tell us your postcode, how you prefer to meet, and what you want help with.
        </p>
      </header>

      <form class="mx-auto max-w-3xl rounded-lg bg-white p-5 text-primary-dark shadow-xl sm:p-8" @submit.prevent="search">
        <div class="grid gap-5 sm:grid-cols-2">
          <label class="block sm:col-span-1">
            <span class="mb-1.5 block text-xs font-semibold uppercase tracking-[0.14em] text-highlight-2">Postcode</span>
            <input
              v-model="postcode"
              type="text"
              autocomplete="postal-code"
              placeholder="e.g. LS1 4AP"
              class="w-full rounded-sm border border-primary-dark/15 bg-primary-background px-3 py-2.5 text-base outline-none focus:border-primary-highlight"
              required
            />
          </label>

          <fieldset class="sm:col-span-1">
            <legend class="mb-1.5 text-xs font-semibold uppercase tracking-[0.14em] text-highlight-2">How would you like to meet?</legend>
            <div class="flex flex-wrap gap-2">
              <label
                v-for="(label, value) in MEETING_LABELS"
                :key="value"
                class="cursor-pointer rounded-full border px-3 py-1.5 text-sm"
                :class="preference === value
                  ? 'border-primary-highlight bg-primary-highlight/15 font-semibold text-highlight-2'
                  : 'border-primary-dark/15 text-primary-dark/80'"
              >
                <input v-model="preference" type="radio" class="sr-only" :value="value" />
                {{ label }}
              </label>
            </div>
          </fieldset>
        </div>

        <fieldset class="mt-5">
          <legend class="mb-2 text-xs font-semibold uppercase tracking-[0.14em] text-highlight-2">Topics of interest</legend>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="entry in specialisms"
              :key="entry.value"
              type="button"
              class="rounded-full border px-3 py-1.5 text-sm transition"
              :class="topics.includes(entry.value)
                ? 'border-primary-highlight bg-primary-highlight/15 font-semibold text-highlight-2'
                : 'border-primary-dark/15 text-primary-dark/80 hover:border-primary-highlight'"
              @click="toggleTopic(entry.value)"
            >
              {{ entry.name }}
            </button>
          </div>
          <p v-if="inEditor && !specialisms.length" class="mt-2 text-sm text-primary-dark/60">
            Specialisms load from the Storyblok datasource.
          </p>
        </fieldset>

        <div class="mt-6 flex flex-wrap items-center gap-3">
          <button
            type="submit"
            class="rounded-sm bg-primary-highlight px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-highlight-2 disabled:opacity-60"
            :disabled="loading"
          >
            {{ loading ? 'Searching…' : 'Find my planner' }}
          </button>
          <p v-if="error" class="text-sm font-medium text-red-700">{{ error }}</p>
        </div>
      </form>

      <div v-if="searched && !loading" class="mt-10">
        <p v-if="fallback" class="mb-4 text-center text-sm text-white/70">
          No exact topic matches nearby — showing the closest planners instead.
        </p>
        <p v-if="!results.length" class="text-center text-white/80">
          No planners matched. Try a different postcode, preference or topic.
        </p>
        <div v-else class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <PlannerTile
            v-for="row in results"
            :key="row.planner.uuid"
            :planner="row.planner"
            :distance="row.distance"
            :highlight="topics"
            cta-label="View profile"
          />
        </div>
      </div>
    </div>
  </section>
</template>
