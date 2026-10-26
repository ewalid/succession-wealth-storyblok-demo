<script setup>
const props = defineProps({ blok: Object, uuid: String });

const optimizedArticleImage = computed(() =>
  getOptimizedImage(props.blok.image, 1600, 800),
);
</script>

<template>
  <article v-editable="blok">
    <div class="container">
      <header>
        <div class="mx-auto mb-12 max-w-2xl text-center">
          <CategoriesList v-if="blok?.categories?.length" :categories="blok.categories" class="mt-12 flex justify-center space-x-4" />
          <H1Headline
            v-if="blok.headline"
          >
            {{ blok.headline }}
          </H1Headline>
          <p v-if="blok?.author && typeof blok.author === 'object' && blok.author.content" class="mt-4 text-sm text-primary-dark/70">
            By
            <NuxtLink :to="`/${blok.author.full_slug || ''}`" class="font-semibold text-primary-highlight hover:underline">
              {{ [blok.author.content.first_name, blok.author.content.last_name].filter(Boolean).join(' ') || 'Succession Wealth' }}
            </NuxtLink>
          </p>
          <p v-else-if="blok?.author === '' || blok?.author === null" class="mt-4 text-sm text-primary-dark/70">
            By Succession Wealth
          </p>
        </div>
        <div v-if="optimizedArticleImage" class="px-4 lg:px-0">
          <div class="relative">
            <DecorationImageTopRight class="absolute right-0 top-0 origin-top-right translate-x-[20px] translate-y-[25px]  scale-50 md:translate-x-[40px] md:translate-y-[-50px] md:scale-100" />
            <img
              :src="optimizedArticleImage"
              :alt="blok.image?.alt"
              class="h-auto w-full rounded-xl"
            />
          </div>
        </div>
      </header>
      <main v-if="blok.text" class="prose prose-lg mx-auto my-12">
        <StoryblokRichText :document="blok.text" />
      </main>
    </div>
    <Banner
      v-if="blok?.call_to_action?.length"
      :blok="blok.call_to_action[0].content"
      :referenced="true"
    />
    <OnwardJourney v-if="blok?.onward?.[0]" :blok="blok.onward[0]" :uuid="uuid" />
  </article>
</template>
