<script setup>
/**
 * The one planner card used everywhere: the PlannerCard block, grids, finder
 * results, office hubs and the /planners listing. Plain props, no Storyblok
 * blok, so a change here updates every place a planner appears.
 */
const props = defineProps({
  planner: { type: Object, required: true },
  ctaLabel: { type: String, default: '' },
  showSpecialisms: { type: Boolean, default: true },
  showOffice: { type: Boolean, default: true },
  distance: { type: Number, default: null },
  highlight: { type: Array, default: () => [] },
  maxChips: { type: Number, default: 3 },
});

useOffices();
const specialismLabels = useDatasourceLabels('specialisms');

const content = computed(() => props.planner?.content ?? {});
const name = computed(() => plannerFullName(content.value) || props.planner?.name || 'Planner');
const initials = computed(() =>
  [content.value.first_name, content.value.last_name]
    .filter(Boolean)
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase(),
);
const photo = computed(() => getOptimizedImage(content.value.photo, 480, 600));
const office = computed(() => officeFor(props.planner));
const officeName = computed(() => office.value?.content?.name || '');
const link = computed(() => storyPath(props.planner));

const chips = computed(() => (content.value.specialisms ?? []).map(value => ({
  value,
  label: labelFor(specialismLabels.value, value),
  matched: props.highlight.includes(value),
})));
const visibleChips = computed(() => {
  // Matched topics float to the front so the "why this planner" is visible.
  const ordered = [...chips.value].sort((a, b) => Number(b.matched) - Number(a.matched));
  return ordered.slice(0, props.maxChips);
});
const hiddenChipCount = computed(() => Math.max(0, chips.value.length - props.maxChips));
</script>

<template>
  <article
    class="group relative flex min-w-0 overflow-hidden rounded-lg border border-primary-dark/10 bg-white transition duration-300 hover:border-primary-highlight hover:shadow-[0_18px_36px_-24px_rgba(20,33,61,0.45)] sm:flex-col"
  >
    <div class="relative min-h-40 w-28 shrink-0 self-stretch overflow-hidden bg-background-2 sm:aspect-[4/5] sm:min-h-0 sm:w-full">
      <img
        v-if="photo"
        :src="photo"
        :alt="content.photo?.alt || name"
        width="480"
        height="600"
        loading="lazy"
        class="absolute inset-0 size-full object-cover object-top transition duration-500 group-hover:scale-[1.03]"
      />
      <div
        v-else
        class="absolute inset-0 flex items-center justify-center bg-background-2 font-display text-4xl text-highlight-2"
        aria-hidden="true"
      >
        {{ initials || '·' }}
      </div>
    </div>

    <div class="flex min-w-0 flex-1 flex-col p-4 sm:p-5">
      <p v-if="content.job_title" class="mb-1 text-xs font-semibold uppercase tracking-[0.14em] text-highlight-2">
        {{ content.job_title }}
      </p>
      <h3 class="font-display text-2xl font-medium leading-tight text-primary-dark sm:text-[1.65rem]">
        {{ name }}
      </h3>

      <p v-if="showOffice && officeName" class="mt-2 flex items-center gap-1.5 text-sm text-primary-dark/70">
        <svg class="size-4 shrink-0 text-primary-highlight" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18s6-5.3 6-10a6 6 0 1 0-12 0c0 4.7 6 10 6 10Zm0-7.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" clip-rule="evenodd" />
        </svg>
        <span class="truncate">{{ officeName }}</span>
      </p>

      <p v-if="distance !== null" class="mt-1 text-sm font-semibold text-primary-highlight">
        {{ formatMiles(distance) }} from you
      </p>

      <ul v-if="showSpecialisms && visibleChips.length" class="mt-4 flex flex-wrap gap-1.5">
        <li
          v-for="chip in visibleChips"
          :key="chip.value"
          class="rounded-full border px-2.5 py-0.5 text-xs"
          :class="chip.matched
            ? 'border-primary-highlight bg-primary-highlight/10 font-semibold text-highlight-2'
            : 'border-primary-dark/15 text-primary-dark/75'"
        >
          {{ chip.label }}
        </li>
        <li v-if="hiddenChipCount" class="px-1 py-0.5 text-xs text-primary-dark/55">
          +{{ hiddenChipCount }}
        </li>
      </ul>

      <NuxtLink
        :to="link"
        class="focus-ring mt-5 inline-flex items-center gap-2 text-sm font-semibold text-primary-dark after:absolute after:inset-0 after:content-[''] group-hover:text-highlight-2 sm:mt-auto sm:pt-5"
      >
        {{ ctaLabel || 'Meet your planner' }}
        <svg class="size-4 transition-transform duration-300 group-hover:translate-x-1" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
          <path d="M4 10h11m-4-4 4 4-4 4" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </NuxtLink>
    </div>
  </article>
</template>
