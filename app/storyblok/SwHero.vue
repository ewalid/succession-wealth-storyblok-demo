<script setup>
const props = defineProps({ blok: Object, index: Number });

const image = computed(() => getOptimizedImage(props.blok?.image, 1800, 1000));
const primary = computed(() => getLinkUrl(props.blok?.primary_cta_link) || '#lead-form');
const secondary = computed(() => getLinkUrl(props.blok?.secondary_cta_link) || '/planners');
</script>

<template>
  <section
    v-editable="blok"
    class="relative isolate min-h-[min(70vh,640px)] overflow-hidden bg-primary-dark"
  >
    <img
      v-if="image"
      :src="image"
      :alt="blok?.image?.alt || ''"
      class="absolute inset-0 size-full object-cover"
    />
    <div class="absolute inset-0 bg-black/25"></div>

    <div class="container relative flex min-h-[min(70vh,640px)] items-center py-24 md:py-28">
      <div class="max-w-xl rounded-[6px] bg-black/65 p-7 text-white shadow-lg backdrop-blur-[2px] sm:p-10">
        <h1 class="font-display text-[2rem] font-normal leading-tight tracking-tight sm:text-[2.75rem]">
          {{ blok?.headline || 'Helping you build and protect your wealth' }}
        </h1>
        <p v-if="blok?.intro" class="mt-4 text-base leading-relaxed text-white/90 sm:text-lg">
          {{ blok.intro }}
        </p>
        <div class="mt-7 flex flex-col gap-3 sm:flex-row sm:gap-4">
          <a
            :href="primary"
            class="inline-flex items-center justify-center rounded-[5px] bg-primary-highlight px-8 py-3 text-sm font-semibold text-white transition hover:bg-highlight-2"
          >
            {{ blok?.primary_cta_label || 'Book a meeting' }}
          </a>
          <a
            :href="secondary"
            class="inline-flex items-center justify-center rounded-[5px] border border-white px-8 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
          >
            {{ blok?.secondary_cta_label || 'Explore solutions' }}
          </a>
        </div>
      </div>
    </div>
  </section>
</template>
