<script setup>
/**
 * Section around a Form: heading, intro, background and an optional image beside
 * or behind the fields. Settings come from the Form story (Layout tab).
 */
const props = defineProps({
  settings: { type: Object, default: () => ({}) },
  fields: { type: Array, default: () => [] },
  buttonText: { type: String, default: 'Submit' },
  headline: { type: String, default: '' },
  editable: Boolean,
});

const s = computed(() => props.settings || {});
const layout = computed(() => s.value.layout || 'stacked');
const image = computed(() => getOptimizedImage(s.value.side_image, 1200, 1400));
const hasImage = computed(() => layout.value !== 'stacked' && !!image.value);
const imageLeft = computed(() => s.value.image_position === 'left');
const BACKGROUNDS = { cream: '#f3f1ed', white: '#ffffff', dark: '#121213', bronze: '#6b5434' };
const bgColor = computed(() => BACKGROUNDS[s.value.background] || BACKGROUNDS.cream);
const darkBg = computed(() => ['dark', 'bronze'].includes(s.value.background));
const WIDTHS = { narrow: 'max-w-xl', medium: 'max-w-3xl', wide: 'max-w-5xl' };
const width = computed(() => WIDTHS[s.value.form_width] || WIDTHS.medium);
// On a dark background or over a photo the fields sit on a white card.
const carded = computed(() => darkBg.value || layout.value === 'image_background' || s.value.card);
const title = computed(() => props.headline || s.value.headline || '');
</script>

<template>
  <section class="relative isolate overflow-hidden" :style="{ background: bgColor }">
    <!-- Photo behind the form -->
    <template v-if="layout === 'image_background' && image">
      <img :src="image" :alt="settings?.side_image?.alt || ''" class="absolute inset-0 -z-10 size-full object-cover" />
      <div class="absolute inset-0 -z-10 bg-black/40"></div>
    </template>

    <div
      class="container py-14 md:py-20"
      :class="layout === 'image_side' && hasImage ? 'grid items-stretch gap-10 lg:grid-cols-2 lg:gap-16' : ''"
    >
      <!-- Photo beside the form -->
      <div
        v-if="layout === 'image_side' && hasImage"
        class="relative min-h-[260px] overflow-hidden rounded-sm lg:min-h-full"
        :class="imageLeft ? 'lg:order-first' : 'lg:order-last'"
      >
        <img :src="image" :alt="settings?.side_image?.alt || ''" class="absolute inset-0 size-full object-cover" />
      </div>

      <div
        class="mx-auto w-full"
        :class="[layout === 'image_side' && hasImage ? '' : width, carded ? 'rounded-sm bg-white p-6 shadow-lg sm:p-10' : '']"
      >
        <h2
          v-if="title"
          class="font-display text-3xl md:text-4xl"
          :class="!carded && darkBg ? 'text-white' : 'text-[#121213]'"
        >
          {{ title }}
        </h2>
        <RichText
          v-if="hasRichText(settings?.intro)"
          :value="settings.intro"
          class="mt-3 text-lg"
          :class="!carded && darkBg ? 'text-white/80' : 'text-[#121213]/75'"
        />
        <div :class="title || hasRichText(settings?.intro) ? 'mt-8' : ''">
          <FormDisplay
            :fields="fields"
            :button-text="buttonText"
            :success-message="settings?.success_message || ''"
            :button-align="settings?.button_align || 'left'"
            :editable="editable"
          />
          <p v-if="!fields.length" class="rounded-sm bg-[#f3f1ed] px-4 py-3 text-sm text-[#121213]/60">Add Form field blocks to build this form.</p>
        </div>
      </div>
    </div>
  </section>
</template>
