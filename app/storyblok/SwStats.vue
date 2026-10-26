<script setup>
defineProps({ blok: Object, index: Number });
</script>

<template>
  <section v-editable="blok" class="bg-[#8B6F4B] text-white">
    <div class="mx-auto max-w-[1200px] px-4 py-10 lg:px-6 lg:py-12">
      <div class="grid grid-cols-2 divide-x divide-white/35 sm:grid-cols-3 lg:grid-cols-6">
        <div
          v-for="stat in (blok?.stats || [])"
          :key="stat._uid"
          v-editable="stat"
          class="flex flex-col items-center justify-center px-3 py-5 text-center"
        >
          <p class="font-display text-3xl font-normal tracking-tight md:text-[2.35rem]">
            {{ stat.value }}
          </p>
          <p class="mt-2 text-[11px] font-medium uppercase tracking-[0.04em] text-white/95 md:text-xs md:normal-case md:tracking-normal">
            {{ stat.label }}
          </p>
        </div>

        <div
          v-if="blok?.show_vouchedfor !== false"
          class="col-span-2 flex flex-col items-center justify-center px-3 py-5 text-center sm:col-span-1 lg:col-span-1"
        >
          <p class="font-display text-lg font-normal tracking-wide md:text-xl">
            {{ blok?.vouchedfor_title || 'VouchedFor' }}
          </p>
          <div class="mt-2 flex items-center gap-0.5 text-[#4BC1CA]" aria-hidden="true">
            <svg v-for="n in 5" :key="n" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-4">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
          <p class="mt-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-white/95">
            {{ blok?.vouchedfor_reviews || '1206 verified reviews' }}
          </p>
        </div>
      </div>

      <p v-if="blok?.footnote" class="mt-4 text-left text-[11px] text-white/85">
        {{ blok.footnote }}
      </p>
    </div>
  </section>
</template>
