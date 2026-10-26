<script setup>
defineProps({ blok: Object, index: Number });

function cardImage(card) {
  return getOptimizedImage(card?.image, 700, 500);
}
function cardLink(card) {
  return getLinkUrl(card?.link) || '#';
}
</script>

<template>
  <section v-editable="blok" class="bg-[#F3F1ED] py-16 md:py-24">
    <div class="container">
      <div class="mx-auto max-w-3xl text-center">
        <h2 class="font-display text-3xl font-normal text-[#121213] md:text-[2.5rem]">
          {{ blok?.headline || 'Expert guides' }}
        </h2>
        <p v-if="blok?.intro" class="mt-4 text-base leading-relaxed text-[#121213]/80 md:text-lg">
          {{ blok.intro }}
        </p>
      </div>

      <div class="mt-12 grid gap-6 md:grid-cols-3">
        <a
          v-for="card in (blok?.cards || [])"
          :key="card._uid"
          v-editable="card"
          :href="cardLink(card)"
          class="group flex flex-col overflow-hidden rounded-[6px] bg-white shadow-sm transition hover:shadow-md"
        >
          <div class="aspect-[16/10] overflow-hidden">
            <img
              v-if="cardImage(card)"
              :src="cardImage(card)"
              :alt="card?.image?.alt || card?.title || ''"
              class="size-full object-cover transition duration-500 group-hover:scale-[1.03]"
            />
          </div>
          <div class="flex flex-1 flex-col bg-primary-highlight px-5 py-5 text-white">
            <h3 class="font-display text-xl font-normal leading-snug">
              {{ card.title }}
            </h3>
            <p v-if="card.subtitle" class="mt-2 text-sm leading-relaxed text-white/90">
              {{ card.subtitle }}
            </p>
            <span class="mt-auto pt-4 text-sm font-semibold underline-offset-2 group-hover:underline">
              {{ card.cta_label || 'Download' }}
            </span>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>
