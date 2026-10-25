<script setup>
const props = defineProps({ blok: Object, index: Number });

const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);

const mode = computed(() => props.blok?.mode || 'manual');
const officeValue = computed(() => props.blok?.office || '');

// A grid with nothing configured renders nothing on the live site; in the
// Visual Editor it shows a plain-English "what to do next" instead.
const configured = computed(() => {
  if (mode.value === 'by_office') {
    return !!officeValue.value;
  }
  if (mode.value === 'by_specialism') {
    return !!props.blok?.specialism;
  }
  return !!props.blok?.planners?.length;
});
</script>

<template>
  <section
    v-if="inEditor || configured"
    v-editable="blok"
    class="page-section planner-grid-section bg-primary-background"
  >
    <div class="container">
      <header v-if="blok?.title" class="mb-8 max-w-2xl md:mb-10">
        <h2 class="font-display text-3xl font-medium leading-tight text-primary-dark md:text-4xl">
          {{ blok.title }}
        </h2>
      </header>
      <PlannerListing
        :mode="mode"
        :office="officeValue"
        :planners="blok?.planners ?? []"
        :specialism="blok?.specialism || ''"
        :sort="blok?.sort || 'pinned_then_az'"
        :limit="blok?.limit"
      />
    </div>
  </section>
</template>
