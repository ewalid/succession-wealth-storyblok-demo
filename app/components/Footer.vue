<script setup>
const props = defineProps({
  headline: Array,
  footerLight: Boolean,
  decoration: Boolean,
  logo: Object,
  nav1Headline: String,
  nav1: Object,
  nav2Headline: String,
  nav2: Object,
  nav3Headline: String,
  nav3: Object,
  about: Object,
  x: Object,
  instagram: Object,
  youtube: Object,
  facebook: Object,
  minimal: { type: Boolean, default: false },
});

const textColor = computed(() => (props.footerLight ? 'text-[#121213]' : 'text-white'));
const muted = computed(() => (props.footerLight ? 'text-[#121213]/70' : 'text-white/70'));
const backgroundColor = computed(() => (props.footerLight ? 'bg-[#F3F1ED]' : 'bg-[#121213]'));
</script>

<template>
  <footer class="relative w-full" :class="backgroundColor">
    <div class="mx-auto max-w-[1200px] px-4 py-14 lg:px-6 lg:py-16">
      <div class="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
        <div class="lg:col-span-1">
          <img
            v-if="logo?.filename"
            :src="logo.filename"
            :alt="logo.alt || 'Succession Wealth'"
            class="mb-6 h-auto w-40 object-contain"
            :class="footerLight ? '' : 'brightness-0 invert'"
          />
          <div v-if="about" class="prose prose-sm max-w-none" :class="[textColor, muted]">
            <StoryblokRichText :document="about" />
          </div>
          <p v-else class="text-sm leading-relaxed" :class="muted">
            Succession Wealth is a trading style of Succession Wealth Management Limited,
            authorised and regulated by the Financial Conduct Authority. FRN 588378.
          </p>
        </div>
        <!-- Legal links stay on campaign pages (FCA); portals and Explore are hidden. -->
        <FooterNav v-if="nav1?.length" :nav="nav1" :headline="nav1Headline || 'Legal information'" :text-color="textColor" />
        <FooterNav v-if="!minimal && nav2?.length" :nav="nav2" :headline="nav2Headline || 'Client portals'" :text-color="textColor" />
        <FooterNav v-if="!minimal && nav3?.length" :nav="nav3" :headline="nav3Headline || 'Explore'" :text-color="textColor" />
      </div>

      <div class="mt-12 border-t pt-6" :class="footerLight ? 'border-[#121213]/15' : 'border-white/15'">
        <p class="text-xs leading-relaxed" :class="muted">
          The value of investments can go down as well as up and you may get back less than you invest.
          Past performance is not a reliable indicator of future results.
        </p>
      </div>
    </div>
  </footer>
</template>
