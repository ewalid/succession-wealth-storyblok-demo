<script setup>
defineProps({ blok: Object, index: Number });
</script>

<template>
  <section v-editable="blok" class="bg-white">
    <div class="mx-auto grid max-w-[1200px] gap-6 px-4 py-12 sm:grid-cols-2 lg:px-6">
      <div
        v-for="item in blok?.items || []"
        :key="item._uid"
        v-editable="item"
        class="rounded-[16px] border border-[#121213]/10 p-6"
      >
        <p class="text-xs font-semibold uppercase tracking-[0.14em] text-[#6b5434]">{{ item.provider }}</p>
        <p class="mt-2 font-display text-3xl">{{ item.rating }}</p>
        <p class="mt-3 text-sm leading-relaxed text-[#121213]/75">{{ item.description }}</p>
      </div>
    </div>
  </section>
</template>
