<script setup>
const props = defineProps({ blok: Object, uuid: String });
const hero = computed(() => getOptimizedImage(props.blok?.hero_image, 1600, 800));
const seoBlok = computed(() => props.blok?.seo?.[0]);
const office = computed(() => (isResolvedStory(props.blok?.office) ? props.blok.office : null));
</script>

<template>
  <article v-editable="blok" class="bg-primary-background">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />
    <section class="relative min-h-[52vh] bg-primary-dark text-white">
      <img v-if="hero" :src="hero" alt="" class="absolute inset-0 size-full object-cover opacity-40" />
      <div class="container relative flex min-h-[52vh] items-end py-16">
        <div class="max-w-2xl rounded-sm bg-black/45 p-6 backdrop-blur-sm sm:p-8">
          <h1 class="font-display text-4xl font-medium md:text-5xl">{{ blok?.headline || 'Campaign' }}</h1>
          <p v-if="blok?.intro" class="mt-4 text-lg text-white/85">{{ blok.intro }}</p>
          <p v-if="office" class="mt-3 text-sm text-primary-highlight">Serving {{ office.content?.name }}</p>
        </div>
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
