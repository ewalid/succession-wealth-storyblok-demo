<script setup>
const props = defineProps({ blok: Object, uuid: String });
const api = useStoryblokApi();
const version = getVersion();
const route = useRoute();

useOffices();
const specialismLabels = useDatasourceLabels('specialisms');
const qualificationLabels = useDatasourceLabels('qualifications');

const story = computed(() => ({
  uuid: props.uuid,
  content: props.blok,
  full_slug: route.path.replace(/^\//, ''),
  name: plannerFullName(props.blok),
}));

const office = computed(() => officeFor(story.value));
const photo = computed(() => getOptimizedImage(props.blok?.photo, 720, 900));
const name = computed(() => plannerFullName(props.blok) || 'Planner');
const booking = computed(() => getLinkUrl(props.blok?.booking_url));
const fca = computed(() => getLinkUrl(props.blok?.fca_register_url));
const related = ref([]);

onMounted(async () => {
  if (props.uuid) {
    related.value = await fetchContentByPlanner(api, props.uuid, { version });
  }
});

const seoBlok = computed(() => props.blok?.seo?.[0]);
</script>

<template>
  <article v-editable="blok" class="bg-primary-background">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />

    <div v-if="blok?.active === false" class="bg-highlight-1/40 px-4 py-2 text-center text-sm font-semibold text-primary-dark">
      This planner is inactive and hidden from listings on the live site.
    </div>

    <section class="border-b border-primary-dark/10 bg-white">
      <div class="container grid gap-8 py-12 lg:grid-cols-[280px_1fr] lg:items-start">
        <div class="mx-auto w-full max-w-xs overflow-hidden rounded-lg bg-background-2 lg:mx-0">
          <img v-if="photo" :src="photo" :alt="blok?.photo?.alt || name" class="aspect-[4/5] w-full object-cover object-top" />
          <div v-else class="flex aspect-[4/5] items-center justify-center font-display text-5xl text-highlight-2">
            {{ (blok?.first_name?.[0] || '') + (blok?.last_name?.[0] || '') }}
          </div>
        </div>
        <div>
          <p v-if="blok?.job_title" class="text-xs font-semibold uppercase tracking-[0.16em] text-highlight-2">
            {{ blok.job_title }}
          </p>
          <h1 class="mt-2 font-display text-4xl font-medium text-primary-dark md:text-5xl">{{ name }}</h1>
          <p v-if="office" class="mt-3 text-primary-dark/70">
            Based in
            <NuxtLink :to="storyPath(office)" class="font-semibold text-primary-highlight hover:underline">
              {{ office.content?.name }}
            </NuxtLink>
          </p>
          <ul v-if="blok?.qualifications?.length" class="mt-4 flex flex-wrap gap-2">
            <li
              v-for="q in blok.qualifications"
              :key="q"
              class="rounded-full border border-primary-dark/15 px-3 py-1 text-xs font-semibold text-primary-dark/80"
            >
              {{ labelFor(qualificationLabels, q) }}
            </li>
          </ul>
          <ul v-if="blok?.specialisms?.length" class="mt-3 flex flex-wrap gap-2">
            <li
              v-for="s in blok.specialisms"
              :key="s"
              class="rounded-full bg-primary-highlight/15 px-3 py-1 text-xs font-semibold text-highlight-2"
            >
              {{ labelFor(specialismLabels, s) }}
            </li>
          </ul>
          <div class="mt-6 flex flex-wrap gap-3 text-sm">
            <a v-if="blok?.phone" :href="`tel:${blok.phone}`" class="font-semibold text-primary-dark hover:text-primary-highlight">{{ blok.phone }}</a>
            <a v-if="blok?.email" :href="`mailto:${blok.email}`" class="font-semibold text-primary-dark hover:text-primary-highlight">{{ blok.email }}</a>
            <a v-if="fca" :href="fca" target="_blank" rel="noopener" class="font-semibold text-primary-highlight underline">FCA register</a>
          </div>
          <div class="mt-8 flex flex-wrap gap-3">
            <a
              v-if="booking"
              :href="booking"
              target="_blank"
              rel="noopener"
              class="rounded-sm bg-primary-highlight px-5 py-2.5 text-sm font-semibold text-white hover:bg-highlight-2"
            >Book a meeting</a>
            <a href="#lead-form" class="rounded-sm border border-primary-dark px-5 py-2.5 text-sm font-semibold text-primary-dark hover:border-primary-highlight">
              Request a call
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="container grid gap-10 py-12 lg:grid-cols-[1.2fr_0.8fr]">
      <div>
        <h2 class="font-display text-3xl text-primary-dark">About {{ blok?.first_name || 'this planner' }}</h2>
        <div v-if="blok?.bio" class="prose prose-lg mt-4 max-w-none text-primary-dark/85">
          <StoryblokRichText :document="blok.bio" />
        </div>
        <p v-else-if="blok?.short_bio" class="mt-4 text-lg text-primary-dark/80">{{ blok.short_bio }}</p>

        <div v-if="related.length" class="mt-12">
          <h3 class="font-display text-2xl text-primary-dark">Content by {{ blok?.first_name }}</h3>
          <ul class="mt-4 space-y-3">
            <li v-for="item in related" :key="item.story.uuid" class="rounded-lg border border-primary-dark/10 bg-white px-4 py-3">
              <span class="text-xs font-semibold uppercase tracking-wider text-highlight-2">{{ item.kind }}</span>
              <NuxtLink :to="storyPath(item.story)" class="mt-1 block font-semibold text-primary-dark hover:text-primary-highlight">
                {{ item.story.content?.title || item.story.content?.headline || item.story.name }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="space-y-6">
        <OfficeMap
          v-if="office"
          :blok="{ component: 'office_map', office, planner: story, show_directions: true, _uid: 'profile-map' }"
        />
      </div>
    </section>

    <div id="lead-form">
      <LeadForm
        :blok="{ component: 'lead_form', headline: 'Ready for a conversation?', intro: 'Share your details and we will arrange a confidential chat.', _uid: 'profile-lead' }"
        :planner="story"
        :office="office"
        :page-slug="story.full_slug"
      />
    </div>
  </article>
</template>
