<script setup>
const props = defineProps({ blok: Object, uuid: String });
const route = useRoute();
const officeStory = computed(() => ({
  uuid: props.uuid,
  content: props.blok,
  full_slug: route.path.replace(/^\//, ''),
  name: props.blok?.name,
}));
const seoBlok = computed(() => props.blok?.seo?.[0]);
const hero = computed(() => getOptimizedImage(props.blok?.hero_image, 1600, 700));
</script>

<template>
  <article v-editable="blok" class="bg-primary-background">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <section class="relative overflow-hidden bg-primary-dark text-white">
      <img v-if="hero" :src="hero" alt="" class="absolute inset-0 size-full object-cover opacity-35" />
      <div class="container relative py-16 md:py-24">
        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-primary-highlight">Our offices</p>
        <h1 class="mt-3 font-display text-4xl font-medium md:text-5xl">{{ blok?.name || 'Office' }}</h1>
        <p v-if="blok?.address" class="mt-4 max-w-xl whitespace-pre-line text-white/80">{{ blok.address }}</p>
        <div class="mt-4 flex flex-wrap gap-4 text-sm">
          <a v-if="blok?.phone" :href="`tel:${blok.phone}`" class="hover:text-primary-highlight">{{ blok.phone }}</a>
          <a v-if="blok?.email" :href="`mailto:${blok.email}`" class="hover:text-primary-highlight">{{ blok.email }}</a>
        </div>
      </div>
    </section>

    <section v-if="blok?.intro" class="container prose prose-lg max-w-3xl py-12">
      <StoryblokRichText :document="blok.intro" />
    </section>

    <OfficeMap
      :blok="{ component: 'office_map', office: officeStory, show_directions: true, _uid: 'office-map' }"
    />

    <section class="page-section">
      <div class="container">
        <h2 class="mb-8 font-display text-3xl text-primary-dark">Wealth planners in {{ blok?.name }}</h2>
        <PlannerListing
          mode="by_office"
          :office="officeStory"
          :pinned="blok?.pinned_planners || []"
          sort="pinned_then_az"
        />
      </div>
    </section>

    <ComponentCheck
      v-for="(b, i) in (blok?.body || [])"
      :key="b._uid"
      :blok="b"
      :index="i"
    />
  </article>
</template>
