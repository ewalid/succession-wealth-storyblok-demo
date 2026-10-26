<script setup>
/**
 * Content library: articles and videos, filtered by topic (the specialisms
 * datasource, the same tags planners use) and by free-text search.
 */
defineProps({ blok: Object });

const storyblokApi = useStoryblokApi();
const topics = useDatasource('specialisms');

const searchTerm = ref('');
const checkedTopic = ref('');
const loading = ref(true);
const articles = ref([]);

const fetchArticles = async () => {
  loading.value = true;
  const filter = { component: { in: 'article-page,video_page' } };
  if (checkedTopic.value) {
    filter.specialisms = { any_in_array: checkedTopic.value };
  }
  try {
    const { data } = await storyblokApi.get('cdn/stories/', {
      version: getVersion(),
      search_term: searchTerm.value,
      filter_query: filter,
      sort_by: 'first_published_at:desc',
      per_page: 48,
    });
    articles.value = (data.stories ?? []).filter(story => story.is_startpage !== true);
  }
  catch {
    articles.value = [];
  }
  loading.value = false;
};

await fetchArticles();

// Only offer topics that have content, so no filter leads to an empty page.
const usedTopics = ref(new Set());
onMounted(async () => {
  try {
    const { data } = await storyblokApi.get('cdn/stories/', {
      version: getVersion(),
      filter_query: { component: { in: 'article-page,video_page' } },
      per_page: 100,
    });
    usedTopics.value = new Set((data.stories ?? []).flatMap(s => s.content?.specialisms || []));
  }
  catch {
    /* show every topic */
  }
});
const topicOptions = computed(() => topics.value.filter(t => !usedTopics.value.size || usedTopics.value.has(t.value)));

watch([searchTerm, checkedTopic], fetchArticles);
</script>

<template>
  <section v-editable="blok" class="container pt-12">
    <header>
      <H1Headline v-if="blok.headline">
        {{ blok.headline }}
      </H1Headline>
      <nav>
        <div class="mb-8 flex justify-center">
          <label for="search" class="sr-only">Search</label>
          <input
            id="search"
            v-model="searchTerm"
            type="search"
            name="search"
            placeholder="Search articles and videos"
            class="w-full max-w-xl rounded-sm border border-primary-dark/25 px-5 py-3 text-lg focus:border-primary-highlight focus:outline-none"
          />
        </div>
        <div class="mb-12 flex flex-wrap justify-center gap-2" role="radiogroup" aria-label="Filter by topic">
          <button
            type="button"
            class="rounded-sm border px-4 py-2 text-sm font-semibold"
            :class="!checkedTopic ? 'border-primary-dark bg-primary-dark text-white' : 'border-primary-dark/20 text-primary-dark'"
            @click="checkedTopic = ''"
          >
            All topics
          </button>
          <button
            v-for="t in topicOptions"
            :key="t.value"
            type="button"
            class="rounded-sm border px-4 py-2 text-sm font-semibold"
            :class="checkedTopic === t.value ? 'border-primary-dark bg-primary-dark text-white' : 'border-primary-dark/20 text-primary-dark'"
            @click="checkedTopic = t.value"
          >
            {{ t.name }}
          </button>
        </div>
      </nav>
    </header>
    <main class="pb-24">
      <section v-if="!loading && articles.length" class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <ContentCard v-for="article in articles" :key="article.uuid" :story="article" />
      </section>
      <section v-else-if="!loading" class="text-primary-dark/70">
        No articles or videos match these filters.
      </section>
    </main>
  </section>
</template>
