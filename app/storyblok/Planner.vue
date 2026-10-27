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
const meetingLabels = useDatasourceLabels('meeting-preferences');
const firstName = computed(() => props.blok?.first_name || 'This planner');

// The site-config leaves the dark, bronze and cream tokens empty, so pin them here.
const brandVars = '--primary-dark:#121213;--primary-highlight:#8b6f4b;--primary-background:#f3f1ed;--color-primary-dark:#121213;--color-primary-highlight:#8b6f4b;--color-primary-background:#f3f1ed;';

// Preset copy uses [First name], [office] and [job title]; fill them from the profile.
const tokens = computed(() => ({
  '[First name]': props.blok?.first_name || 'This planner',
  '[office]': office.value?.content?.name || 'local',
  '[job title]': props.blok?.job_title || 'wealth planner',
}));
function fillTokens(node) {
  if (Array.isArray(node)) {
    return node.map(fillTokens);
  }
  if (!node || typeof node !== 'object') {
    return node;
  }
  const out = { ...node };
  if (typeof out.text === 'string') {
    out.text = Object.entries(tokens.value).reduce((t, [k, v]) => t.split(k).join(v), out.text);
  }
  if (out.content) {
    out.content = fillTokens(out.content);
  }
  return out;
}
const bio = computed(() => (hasRichText(props.blok?.bio) ? fillTokens(props.blok.bio) : null));

// Placeholder bio when the Full bio field is empty, built from the profile fields.
const placeholderBio = computed(() => {
  const b = props.blok || {};
  const specs = (b.specialisms || []).map(s => labelFor(specialismLabels, s).toLowerCase());
  const specText = specs.length > 1 ? `${specs.slice(0, -1).join(', ')} and ${specs.at(-1)}` : specs[0];
  return [
    `${firstName.value} is a ${(b.job_title || 'wealth planner').toLowerCase()}${office.value ? ` based in our ${office.value.content?.name} office` : ''}${specText ? `, helping clients with ${specText}` : ''}.`,
    'Every relationship starts with a conversation about what matters to you: your family, your plans and the life you want to lead. From there, we build a financial plan around those goals and review it with you every year.',
    'Biography coming soon. Add it in the Full bio field.',
  ];
});
</script>

<template>
  <article v-editable="blok" class="bg-primary-background" :style="brandVars">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />

    <div v-if="blok?.active === false" class="bg-highlight-1/40 px-4 py-2 text-center text-sm font-semibold text-primary-dark">
      This planner is inactive and hidden from listings on the live site.
    </div>

    <section class="border-b border-primary-dark/10 bg-white">
      <div class="container grid gap-8 py-12 lg:grid-cols-[280px_1fr] lg:items-start">
        <div class="mx-auto w-full max-w-xs overflow-hidden rounded-lg bg-background-2 lg:mx-0">
          <img v-if="photo" :src="photo" :alt="blok?.photo?.alt || name" class="aspect-[4/5] w-full object-cover object-top" />
          <div v-else class="flex aspect-[4/5] flex-col items-center justify-center gap-3 font-display text-5xl text-highlight-2">
            <template v-if="blok?.first_name || blok?.last_name">{{ (blok?.first_name?.[0] || '') + (blok?.last_name?.[0] || '') }}</template>
            <svg v-else viewBox="0 0 24 24" class="size-24 opacity-50" fill="currentColor" aria-hidden="true"><circle cx="12" cy="8" r="4" /><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7z" /></svg>
            <span class="font-body text-xs font-semibold uppercase tracking-[0.16em] opacity-70">Photo coming soon</span>
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

    <section class="container grid gap-10 py-12 lg:grid-cols-[1.2fr_0.8fr] lg:items-start">
      <div>
        <h2 class="font-display text-3xl text-primary-dark">About {{ blok?.first_name || 'this planner' }}</h2>
        <p v-if="blok?.short_bio" class="mt-4 border-l-2 border-[#8b6f4b] pl-4 font-display text-xl italic text-primary-dark/80">{{ blok.short_bio }}</p>
        <div v-if="bio" class="prose prose-lg mt-4 max-w-none text-primary-dark/85">
          <StoryblokRichText :document="bio" />
        </div>
        <div v-else class="mt-4 space-y-4 text-lg text-primary-dark/80">
          <p v-for="(line, i) in placeholderBio" :key="i" :class="i === placeholderBio.length - 1 ? 'text-sm italic text-primary-dark/50' : ''">{{ line }}</p>
        </div>

        <div class="mt-10 grid gap-4 sm:grid-cols-3">
          <div class="rounded-sm border border-primary-dark/10 bg-white p-5">
            <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#6b5434]">How we can meet</p>
            <ul class="mt-3 space-y-1 text-sm text-primary-dark/80">
              <li v-for="m in (blok?.meeting_preferences?.length ? blok.meeting_preferences : ['office', 'digital'])" :key="m">{{ labelFor(meetingLabels, m) }}</li>
            </ul>
          </div>
          <div class="rounded-sm border border-primary-dark/10 bg-white p-5">
            <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#6b5434]">Home visits</p>
            <p class="mt-3 text-sm text-primary-dark/80">{{ Number(blok?.home_visit_radius_miles) > 0 ? `Within ${blok.home_visit_radius_miles} miles of ${office?.content?.name || 'the office'}` : 'Office and video meetings' }}</p>
          </div>
          <div class="rounded-sm border border-primary-dark/10 bg-white p-5">
            <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#6b5434]">First meeting</p>
            <p class="mt-3 text-sm text-primary-dark/80">Free, confidential and with no obligation</p>
          </div>
        </div>

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
        v-if="blok?.form?.[0]"
        :blok="blok.form[0]"
        :planner="story"
        :office="office"
        :page-slug="story.full_slug"
      />
      <LeadForm
        v-else
        :blok="{
          component: 'lead_form',
          layout: 'dark_panel',
          background: 'navy',
          form_width: 'medium',
          field_columns: '2',
          form_mode: 'native',
          headline: 'Ready for a conversation?',
          intro: 'Share your details and we will arrange a confidential chat.',
          fields: ['first_name', 'surname', 'email', 'phone', 'postcode', 'investment_value', 'heard_about'],
          submit_label: 'Request a conversation',
          show_attribution_preview: true,
          _uid: 'profile-lead',
        }"
        :planner="story"
        :office="office"
        :page-slug="story.full_slug"
      />
    </div>
    <OnwardJourney v-if="blok?.onward?.[0]" :blok="blok.onward[0]" :uuid="story?.uuid" />
  </article>
</template>
