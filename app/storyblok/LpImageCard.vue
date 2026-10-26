<script setup>
const props = defineProps({ blok: Object, index: Number });
const t = useLocationTokens();
const image = computed(() => getOptimizedImage(props.blok?.image, 2000, 1000));
const ctaHref = computed(() => getLinkUrl(props.blok?.cta_link) || '#lead-form');
const justify = computed(() => ({ left: 'justify-start', center: 'justify-center', right: 'justify-end' })[props.blok?.card_position || 'right']);
</script>

<template>
  <section v-editable="blok" class="relative isolate overflow-hidden bg-[#e9e3d8]">
    <img v-if="image" :src="image" :alt="blok?.image?.alt || ''" class="absolute inset-0 -z-10 size-full object-cover" />
    <div class="mx-auto flex min-h-[560px] max-w-[1200px] items-center px-4 py-14 lg:px-6" :class="justify">
      <div class="w-full max-w-[520px] rounded-[16px] bg-white/90 p-7 backdrop-blur-sm sm:p-10">
        <h2 class="font-display text-[30px] leading-tight sm:text-[34px]">{{ t(blok?.headline) }}</h2>
        <RichText v-if="hasRichText(blok?.body)" :value="t(blok.body)" class="mt-4 text-[15px] leading-relaxed text-[#121213]/85" />
        <a
          v-if="blok?.cta_label"
          :href="ctaHref"
          class="mt-6 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]"
        >{{ blok.cta_label }}</a>
      </div>
    </div>
  </section>
</template>
