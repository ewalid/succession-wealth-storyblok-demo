<script setup>
defineProps({ blok: Object, index: Number });
</script>

<template>
  <section v-editable="blok" class="border-y border-[#121213]/10 bg-white py-12 md:py-16">
    <div class="mx-auto max-w-[1200px] px-4 lg:px-6">
      <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-5">
        <div
          v-for="stat in (blok?.stats || [])"
          :key="stat._uid"
          v-editable="stat"
          class="text-center"
        >
          <p class="font-[family-name:var(--font-family-hero)] text-4xl font-extralight text-[#8B6F4B] md:text-5xl">
            {{ stat.value }}
          </p>
          <p class="mt-2 text-sm font-medium text-[#121213]/75">
            {{ stat.label }}
          </p>
        </div>
      </div>
      <p v-if="blok?.footnote" class="mt-8 text-center text-xs text-[#121213]/55">
        {{ blok.footnote }}
      </p>
    </div>
  </section>
</template>
