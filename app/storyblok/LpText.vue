<script setup>
const props = defineProps({ blok: Object, index: Number });
const t = useLocationTokens();
const image = computed(() => getOptimizedImage(props.blok?.image, 1200, 900));
const position = computed(() => (image.value ? props.blok?.image_position || 'none' : 'none'));
const ctaHref = computed(() => getLinkUrl(props.blok?.cta_link) || '#lead-form');
</script>

<template>
  <section v-editable="blok" :class="blok?.background === 'cream' ? 'bg-[#f3f1ed]' : 'bg-white'">
    <div
      class="mx-auto max-w-[1200px] px-4 py-16 lg:px-6 lg:py-20"
      :class="position === 'none' ? '' : 'grid items-center gap-10 md:grid-cols-2 lg:gap-16'"
    >
      <img
        v-if="position !== 'none'"
        :src="image"
        :alt="blok?.image?.alt || ''"
        class="aspect-[4/3] w-full rounded-[16px] object-cover"
        :class="position === 'right' ? 'md:order-2' : ''"
      />
      <div :class="position === 'none' ? 'max-w-[760px]' : ''">
        <h2 class="font-display text-[32px] leading-tight sm:text-[40px]">{{ t(blok?.headline) }}</h2>
        <RichText
          v-if="hasRichText(blok?.body)"
          :value="t(blok.body)"
          class="mt-5 text-base leading-relaxed text-[#121213]/85 [&_h3]:mt-6 [&_h3]:font-display [&_h3]:text-2xl"
        />
        <a
          v-if="blok?.cta_label"
          :href="ctaHref"
          class="mt-7 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]"
        >{{ blok.cta_label }}</a>
      </div>
    </div>
  </section>
</template>
