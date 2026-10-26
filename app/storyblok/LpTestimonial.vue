<script setup>
const props = defineProps({ blok: Object, index: Number });
const t = useLocationTokens();
const link = computed(() => getLinkUrl(props.blok?.link));
const ctaHref = computed(() => getLinkUrl(props.blok?.cta_link) || '#lead-form');
</script>

<template>
  <section v-editable="blok" class="bg-white">
    <div class="mx-auto max-w-[1200px] px-4 py-16 lg:px-6 lg:py-20">
      <h2 class="font-display text-[32px] leading-tight sm:text-[40px]">{{ t(blok?.headline) }}</h2>
      <a v-if="link && blok?.link_label" :href="link" target="_blank" rel="noopener" class="mt-2 inline-block font-medium underline underline-offset-2">{{ blok.link_label }}</a>
      <blockquote v-if="blok?.quote" class="mt-10 max-w-[640px] border-l-2 border-[#8B6F4B] pl-6 font-display text-[22px] leading-snug text-[#121213]/85 sm:ml-20">
        {{ t(blok.quote) }}
        <footer v-if="blok?.attribution" class="mt-4 font-body text-sm text-[#6b5434]">{{ blok.attribution }}</footer>
      </blockquote>
      <a
        v-if="blok?.cta_label"
        :href="ctaHref"
        class="mt-10 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]"
      >{{ blok.cta_label }}</a>
    </div>
  </section>
</template>
