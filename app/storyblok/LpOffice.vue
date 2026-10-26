<script setup>
/** "Our nearest office to you": address from the page's Office, map as image or interactive. */
const props = defineProps({ blok: Object, index: Number });
const t = useLocationTokens();
const location = useLocationContext();
const officeUuid = computed(() => location?.value?.officeUuid || '');
const address = computed(() => location?.value?.address || '');
const mapImage = computed(() => getOptimizedImage(props.blok?.map_image, 1200, 800));
const ctaHref = computed(() => getLinkUrl(props.blok?.cta_link) || '#lead-form');
</script>

<template>
  <section v-editable="blok" class="bg-white">
    <div class="mx-auto grid max-w-[1200px] items-center gap-10 px-4 py-16 md:grid-cols-2 lg:gap-16 lg:px-6 lg:py-20">
      <div class="overflow-hidden rounded-[16px] bg-[#f3f1ed]">
        <img v-if="blok?.map_type === 'image' && mapImage" :src="mapImage" :alt="blok?.map_image?.alt || ''" class="aspect-[3/2] w-full object-cover" />
        <OfficeMap
          v-else-if="officeUuid"
          :key="officeUuid"
          :blok="{ _uid: `lp-office-map-${blok?._uid}`, component: 'office_map', office: officeUuid, show_directions: true }"
        />
      </div>
      <div>
        <h2 class="font-display text-[32px] leading-tight sm:text-[40px]">{{ t(blok?.headline) || 'Our nearest office to you' }}</h2>
        <p v-if="address" class="mt-4 font-medium">{{ address }}</p>
        <RichText v-if="hasRichText(blok?.body)" :value="t(blok.body)" class="mt-4 text-base leading-relaxed text-[#121213]/85" />
        <a
          v-if="blok?.cta_label"
          :href="ctaHref"
          class="mt-7 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]"
        >{{ blok.cta_label }}</a>
      </div>
    </div>
  </section>
</template>
