<script setup>
const props = defineProps({ blok: Object, index: Number });

const image = computed(() => getOptimizedImage(props.blok?.image, 1000, 800));
const cta = computed(() => getLinkUrl(props.blok?.cta_link) || '/planners');
const reverse = computed(() => !!props.blok?.image_left);
</script>

<template>
  <section
    v-editable="blok"
    class="bg-white py-16 md:py-24"
  >
    <div
      class="container grid items-center gap-10 lg:grid-cols-2 lg:gap-16"
      :class="reverse ? 'lg:[&>*:first-child]:order-2' : ''"
    >
      <div>
        <p
          v-if="blok?.eyebrow"
          class="mb-3 text-xs font-semibold uppercase tracking-[0.14em] text-primary-highlight"
        >
          {{ blok.eyebrow }}
        </p>
        <h2 class="font-display text-3xl font-normal leading-snug text-[#121213] md:text-[2.5rem]">
          {{ blok?.headline }}
        </h2>
        <p v-if="blok?.body" class="mt-5 max-w-xl text-base leading-relaxed text-[#121213]/80 md:text-lg">
          {{ blok.body }}
        </p>
        <a
          v-if="blok?.cta_label"
          :href="cta"
          class="mt-8 inline-flex items-center justify-center rounded-[5px] bg-primary-highlight px-8 py-3 text-sm font-semibold text-white transition hover:bg-highlight-2"
        >
          {{ blok.cta_label }}
        </a>
      </div>
      <div class="overflow-hidden rounded-[6px]">
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
