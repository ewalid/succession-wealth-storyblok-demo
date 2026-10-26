<script setup>
const props = defineProps({ blok: Object, index: Number });

const mediaType = computed(() => props.blok?.media_type || 'image');
const showVideo = computed(() =>
  mediaType.value === 'video' && Boolean(props.blok?.video?.filename),
);
const image = computed(() => {
  if (showVideo.value) {
    return '';
  }
  return getOptimizedImage(props.blok?.image, 1800, 1000);
});
const primary = computed(() => getLinkUrl(props.blok?.primary_cta_link) || '#lead-form');
const secondary = computed(() => getLinkUrl(props.blok?.secondary_cta_link) || '/planners');
</script>

<template>
  <section
    v-editable="blok"
    class="relative isolate overflow-hidden bg-[#121213]"
  >
    <video
      v-if="showVideo"
      :src="blok.video.filename"
      class="absolute inset-0 size-full object-cover object-center"
      autoplay
      muted
      loop
      playsinline
    ></video>
    <img
      v-else-if="image"
      :src="image"
      :alt="blok?.image?.alt || ''"
      class="absolute inset-0 size-full object-cover object-center"
    />
    <div class="absolute inset-0 bg-black/20"></div>

    <div class="relative mx-auto flex min-h-[522px] max-w-[1200px] items-center px-4 py-16 lg:px-6 lg:py-20">
      <div class="w-full max-w-[454px] rounded-[5px] bg-black/65 px-8 py-9 text-white sm:px-10 sm:py-10">
        <h1 class="font-[family-name:var(--font-family-hero)] text-[2rem] font-extralight leading-[1.2] tracking-[-0.01em] sm:text-[44px] sm:leading-[52.8px]">
          {{ blok?.headline || 'Helping you build and protect your wealth' }}
        </h1>
        <p
          v-if="blok?.intro"
          class="mt-4 text-base font-medium leading-relaxed text-white sm:text-lg"
        >
          {{ blok.intro }}
        </p>
        <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:gap-4">
          <a
            :href="primary"
            class="inline-flex items-center justify-center rounded-[5px] border border-[#8B6F4B] bg-[#8B6F4B] px-8 py-3 text-base font-medium text-white transition hover:bg-[#6f583c]"
          >
            {{ blok?.primary_cta_label || 'Book a meeting' }}
          </a>
          <a
            :href="secondary"
            class="inline-flex items-center justify-center rounded-[5px] border border-white bg-transparent px-8 py-3 text-base font-medium text-white transition hover:bg-white/10"
          >
            {{ blok?.secondary_cta_label || 'Explore solutions' }}
          </a>
        </div>
      </div>
    </div>
  </section>
</template>
