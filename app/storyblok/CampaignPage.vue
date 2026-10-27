<script setup>
const props = defineProps({ blok: Object, uuid: String });
const hero = computed(() => getOptimizedImage(props.blok?.hero_image, 1600, 900));
const seoBlok = computed(() => props.blok?.seo?.[0]);
const office = computed(() => (isResolvedStory(props.blok?.office) ? props.blok.office : null));

// Location sections (lp-*) can be used on campaigns too: fill their {city}/{phone}/{address}
// tokens and the office map from this campaign's Office.
provideLocationTokens(computed(() => {
  const c = office.value?.content || {};
  const address = (c.address || '').split('\n').map(s => s.trim()).filter(Boolean).join(', ');
  return {
    city: c.name || '',
    phone: c.phone || '',
    address: c.postcode ? `${address}, ${c.postcode}` : address,
    officeUuid: office.value?.uuid || '',
  };
}));

// Hero: one of five layouts, with an image, an uploaded video or a YouTube film.
const layout = computed(() => props.blok?.hero_layout || 'overlay_card');
const mediaType = computed(() => props.blok?.hero_media_type || 'image');
const videoUrl = computed(() => (mediaType.value === 'video' ? props.blok?.hero_video?.filename || '' : ''));
const youtubeId = computed(() => {
  if (mediaType.value !== 'youtube') {
    return '';
  }
  const raw = (props.blok?.hero_youtube || '').trim();
  const match = raw.match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([\w-]{11})/);
  return match ? match[1] : (/^[\w-]{11}$/.test(raw) ? raw : '');
});
// Falls back to the image when the chosen video is missing, so the hero is never empty.
const media = computed(() => {
  if (layout.value === 'text_only') {
    return 'none';
  }
  if (youtubeId.value) {
    return 'youtube';
  }
  if (videoUrl.value) {
    return 'video';
  }
  return hero.value ? 'image' : 'none';
});
const youtubeSrc = computed(() => {
  const id = youtubeId.value;
  return `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&mute=1&loop=1&playlist=${id}&controls=0&modestbranding=1&playsinline=1&rel=0`;
});
const ctaLabel = computed(() => props.blok?.hero_cta_label ?? '');
const ctaHref = computed(() => getLinkUrl(props.blok?.hero_cta_link) || '#lead-form');
const isBackground = computed(() => ['overlay_card', 'centered', 'compact'].includes(layout.value));
</script>

<template>
  <article v-editable="blok" class="bg-primary-background">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />

    <!-- Background-media layouts: overlay card, centred, compact strip -->
    <section
      v-if="isBackground"
      class="relative isolate overflow-hidden bg-primary-dark text-white"
      :class="layout === 'compact' ? 'min-h-[280px]' : 'min-h-[52vh]'"
    >
      <img v-if="media === 'image'" :src="hero" :alt="blok?.hero_image?.alt || ''" class="absolute inset-0 -z-10 size-full object-cover" :class="layout === 'overlay_card' ? 'opacity-40' : 'opacity-55'" />
      <video v-else-if="media === 'video'" :src="videoUrl" :poster="hero || undefined" class="absolute inset-0 -z-10 size-full object-cover opacity-60" autoplay muted loop playsinline></video>
      <div v-else-if="media === 'youtube'" class="pointer-events-none absolute inset-0 -z-10 overflow-hidden opacity-60">
        <!-- Oversized so YouTube's own chrome stays out of frame -->
        <iframe :src="youtubeSrc" title="" allow="autoplay; encrypted-media" class="absolute left-1/2 top-1/2 h-[130%] w-[130%] min-h-[56.25vw] min-w-[177.77vh] -translate-x-1/2 -translate-y-1/2" tabindex="-1"></iframe>
      </div>
      <div v-if="layout !== 'overlay_card'" class="absolute inset-0 -z-10 bg-black/35"></div>

      <div
        class="container relative flex"
        :class="{
          'min-h-[52vh] items-end py-16': layout === 'overlay_card',
          'min-h-[52vh] items-center justify-center py-20 text-center': layout === 'centered',
          'min-h-[280px] items-center py-10': layout === 'compact',
        }"
      >
        <div
          :class="{
            'max-w-2xl rounded-sm bg-black/45 p-6 backdrop-blur-sm sm:p-8': layout === 'overlay_card',
            'max-w-3xl': layout === 'centered',
            'flex w-full flex-col gap-6 md:flex-row md:items-center md:justify-between': layout === 'compact',
          }"
        >
          <div>
            <h1 class="font-display font-medium" :class="{ 'text-3xl md:text-4xl': layout === 'compact', 'text-4xl md:text-5xl': layout === 'overlay_card', 'text-4xl md:text-6xl': layout === 'centered' }">{{ blok?.headline || 'Campaign' }}</h1>
            <RichText v-if="hasRichText(blok?.intro)" :value="blok.intro" class="mt-4 text-lg text-white/85" :class="layout === 'centered' ? 'mx-auto max-w-2xl' : ''" />
            <p v-if="office" class="mt-3 text-sm text-white/80">Serving {{ office.content?.name }}</p>
          </div>
          <a
            v-if="ctaLabel"
            :href="ctaHref"
            class="inline-flex shrink-0 items-center justify-center rounded-[5px] border border-[#8B6F4B] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]"
            :class="layout === 'compact' ? '' : 'mt-7'"
          >{{ ctaLabel }}</a>
        </div>
      </div>
    </section>

    <!-- Split: text left, media right -->
    <section v-else-if="layout === 'split'" class="bg-primary-background">
      <div class="container grid items-center gap-10 py-14 md:grid-cols-2 md:py-20">
        <div>
          <h1 class="font-display text-4xl font-medium text-primary-dark md:text-5xl">{{ blok?.headline || 'Campaign' }}</h1>
          <RichText v-if="hasRichText(blok?.intro)" :value="blok.intro" class="mt-4 text-lg text-primary-dark/75" />
          <p v-if="office" class="mt-3 text-sm font-semibold text-[#8B6F4B]">Serving {{ office.content?.name }}</p>
          <a v-if="ctaLabel" :href="ctaHref" class="mt-7 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]">{{ ctaLabel }}</a>
        </div>
        <div v-if="media !== 'none'" class="relative aspect-[4/3] overflow-hidden rounded-sm bg-background-2">
          <img v-if="media === 'image'" :src="hero" :alt="blok?.hero_image?.alt || ''" class="size-full object-cover" />
          <video v-else-if="media === 'video'" :src="videoUrl" :poster="hero || undefined" class="size-full object-cover" autoplay muted loop playsinline controls></video>
          <iframe v-else :src="youtubeSrc.replace('&controls=0', '&controls=1')" title="Campaign video" allow="autoplay; encrypted-media; fullscreen" allowfullscreen class="size-full"></iframe>
        </div>
      </div>
    </section>

    <!-- Text only -->
    <section v-else class="bg-primary-dark text-white">
      <div class="container py-16 md:py-20">
        <h1 class="max-w-3xl font-display text-4xl font-medium md:text-5xl">{{ blok?.headline || 'Campaign' }}</h1>
        <RichText v-if="hasRichText(blok?.intro)" :value="blok.intro" class="mt-4 max-w-2xl text-lg text-white/85" />
        <p v-if="office" class="mt-3 text-sm text-white/80">Serving {{ office.content?.name }}</p>
        <a v-if="ctaLabel" :href="ctaHref" class="mt-7 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]">{{ ctaLabel }}</a>
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
