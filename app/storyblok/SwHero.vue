<script setup>
const props = defineProps({ blok: Object, index: Number });

const layout = computed(() => props.blok?.layout || 'overlay_card');
const mediaType = computed(() => props.blok?.media_type || 'image');
const mediaSide = computed(() => props.blok?.media_position || 'right');
const showVideo = computed(() =>
  mediaType.value === 'video' && Boolean(props.blok?.video?.filename),
);
const image = computed(() => {
  if (showVideo.value) {
    return '';
  }
  return getOptimizedImage(props.blok?.image, 1800, 1000);
});
const hasMedia = computed(() => showVideo.value || Boolean(image.value));
const primary = computed(() => getLinkUrl(props.blok?.primary_cta_link) || '#lead-form');
const secondary = computed(() => getLinkUrl(props.blok?.secondary_cta_link) || '/planners');

const isOverlay = computed(() =>
  layout.value === 'overlay_card' || layout.value === 'overlay_center' || layout.value === 'full_bleed',
);
const isSplit = computed(() => layout.value === 'split');
const isCentered = computed(() => layout.value === 'overlay_center' || layout.value === 'full_bleed');

const headline = computed(() => props.blok?.headline || 'Helping you build and protect your wealth');
</script>

<template>
  <section
    v-editable="blok"
    class="relative isolate overflow-hidden"
    :class="isOverlay ? 'bg-[#121213]' : 'bg-[#F3F1ED]'"
  >
    <!-- Full-bleed / overlay media -->
    <template v-if="isOverlay && hasMedia">
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
      <div
        class="absolute inset-0"
        :class="layout === 'full_bleed' ? 'bg-gradient-to-r from-black/70 via-black/45 to-black/20' : 'bg-black/20'"
      ></div>
    </template>

    <!-- Overlay layouts: card or free text on media -->
    <div
      v-if="isOverlay"
      class="relative mx-auto flex min-h-[522px] max-w-[1200px] items-center px-4 py-16 lg:px-6 lg:py-20"
      :class="isCentered ? 'justify-center text-center' : 'justify-start text-left'"
    >
      <!-- Dark card (Succession look / centered variant) -->
      <div
        v-if="layout === 'overlay_card' || layout === 'overlay_center'"
        class="w-full max-w-[454px] rounded-[5px] bg-black/65 px-8 py-9 text-white sm:px-10 sm:py-10"
        :class="layout === 'overlay_center' ? 'mx-auto' : ''"
      >
        <h1 class="font-[family-name:var(--font-family-hero)] text-[2rem] font-extralight leading-[1.2] tracking-[-0.01em] sm:text-[44px] sm:leading-[52.8px]">
          {{ headline }}
        </h1>
        <p
          v-if="blok?.intro"
          class="mt-4 text-base font-medium leading-relaxed text-white sm:text-lg"
        >
          {{ blok.intro }}
        </p>
        <div
          class="mt-6 flex flex-col gap-3 sm:flex-row sm:gap-4"
          :class="layout === 'overlay_center' ? 'sm:justify-center' : ''"
        >
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

      <!-- Full-bleed: text directly on media -->
      <div
        v-else
        class="w-full max-w-2xl text-white"
        :class="isCentered ? 'mx-auto' : ''"
      >
        <h1 class="font-[family-name:var(--font-family-hero)] text-[2rem] font-extralight leading-[1.2] tracking-[-0.01em] sm:text-[44px] sm:leading-[52.8px]">
          {{ headline }}
        </h1>
        <p
          v-if="blok?.intro"
          class="mt-4 text-base font-medium leading-relaxed text-white/95 sm:text-lg"
        >
          {{ blok.intro }}
        </p>
        <div
          class="mt-6 flex flex-col gap-3 sm:flex-row sm:gap-4"
          :class="isCentered ? 'sm:justify-center' : ''"
        >
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

    <!-- Split: text + media -->
    <div
      v-else-if="isSplit"
      class="mx-auto grid min-h-[522px] max-w-[1200px] items-stretch gap-0 lg:grid-cols-2"
    >
      <div
        class="flex flex-col justify-center px-6 py-14 text-[#121213] sm:px-10 lg:px-12 lg:py-20"
        :class="mediaSide === 'left' ? 'lg:order-2' : 'lg:order-1'"
      >
        <h1 class="font-[family-name:var(--font-family-hero)] text-[2rem] font-extralight leading-[1.2] tracking-[-0.01em] sm:text-[44px] sm:leading-[52.8px]">
          {{ headline }}
        </h1>
        <p
          v-if="blok?.intro"
          class="mt-4 max-w-md text-base font-medium leading-relaxed text-[#121213]/90 sm:text-lg"
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
            class="inline-flex items-center justify-center rounded-[5px] border border-[#121213] bg-transparent px-8 py-3 text-base font-medium text-[#121213] transition hover:bg-[#121213]/5"
          >
            {{ blok?.secondary_cta_label || 'Explore solutions' }}
          </a>
        </div>
      </div>
      <div
        class="relative min-h-[280px] bg-[#121213] lg:min-h-full"
        :class="mediaSide === 'left' ? 'lg:order-1' : 'lg:order-2'"
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
      </div>
    </div>
  </section>
</template>
