<script setup>
const props = defineProps({ blok: Object, index: Number });

const image = computed(() => getOptimizedImage(props.blok?.image, 1000, 800));
const cta = computed(() => getLinkUrl(props.blok?.cta_link) || '/planners');
const reverse = computed(() => !!props.blok?.image_left);
</script>

<template>
  <section v-editable="blok" class="bg-white py-14 md:py-20">
    <div
      class="mx-auto grid max-w-[1200px] items-center gap-10 px-4 lg:grid-cols-2 lg:gap-16 lg:px-6"
      :class="reverse ? 'lg:[&>*:first-child]:order-2' : ''"
    >
      <div class="max-w-xl">
        <p
          v-if="blok?.eyebrow"
          class="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-[#8B6F4B]"
        >
          {{ blok.eyebrow }}
        </p>
        <h2 class="font-display text-[1.875rem] font-normal leading-snug text-[#121213] md:text-[40px] md:leading-[1.25]">
          {{ blok?.headline }}
        </h2>
        <RichText v-if="hasRichText(blok?.body)" :value="blok.body" class="mt-5 text-base leading-relaxed text-[#121213]/80 md:text-lg" />
        <a
          v-if="blok?.cta_label"
          :href="cta"
          class="mt-8 inline-flex items-center justify-center rounded-[5px] border border-[#8B6F4B] bg-[#8B6F4B] px-8 py-3 text-base font-medium text-white transition hover:bg-[#6f583c]"
        >
          {{ blok.cta_label }}
        </a>
      </div>
      <div class="overflow-hidden rounded-[5px]">
        <img
          v-if="image"
          :src="image"
          :alt="blok?.image?.alt || ''"
          class="aspect-[5/4] w-full object-cover"
        />
      </div>
    </div>
  </section>
</template>
