<script setup>
/**
 * Location landing page (their /financial-advice-<city> pages). The Office field
 * localises everything: city, phone, address, map and planners.
 */
const props = defineProps({ blok: Object, uuid: String });
const api = useStoryblokApi();
const version = getVersion();
const office = ref(null);

const officeUuid = computed(() => {
  const v = props.blok?.office;
  return typeof v === 'string' ? v : v?.uuid || '';
});
watch(officeUuid, async () => {
  office.value = officeUuid.value ? await resolveStory(api, props.blok?.office, { version }) : null;
}, { immediate: true });

const city = computed(() => office.value?.content?.name || '');
const phone = computed(() => props.blok?.tracking_phone || office.value?.content?.phone || '');
const address = computed(() => (office.value?.content?.address || '').split('\n').map(s => s.trim()).filter(Boolean).join(', ')
  + (office.value?.content?.postcode ? `, ${office.value.content.postcode}` : ''));
const tokenValues = computed(() => ({ city: city.value, phone: phone.value, address: address.value, officeUuid: officeUuid.value }));
provideLocationTokens(tokenValues);
const t = useLocationTokens();

const hero = computed(() => getOptimizedImage(props.blok?.hero_image, 2000, 1000));
const ctaHref = computed(() => getLinkUrl(props.blok?.cta_link) || '#lead-form');
const seoBlok = computed(() => props.blok?.seo?.[0]);

// Planner and map blocks with no office of their own use the page's office.
const sections = computed(() => (props.blok?.body || []).map((b) => {
  if (['planner_grid', 'office_map'].includes(b.component) && !b.office && officeUuid.value) {
    return { ...b, office: officeUuid.value, title: t(b.title) };
  }
  return b.component === 'planner_grid' ? { ...b, title: t(b.title) } : b;
}));
</script>

<template>
  <article v-editable="blok" class="bg-white text-[#121213]">
    <SeoMeta v-if="seoBlok" :blok="seoBlok" />

    <div class="border-b border-[#121213]/10">
      <div class="mx-auto max-w-[1200px] px-4 py-3 text-sm text-[#6b5434] lg:px-6">
        Financial Advice {{ city }}
      </div>
    </div>

    <section class="relative isolate overflow-hidden bg-[#121213]">
      <img v-if="hero" :src="hero" :alt="blok?.hero_image?.alt || ''" class="absolute inset-0 -z-10 size-full object-cover" />
      <div class="mx-auto flex min-h-[620px] max-w-[1200px] items-center px-4 py-12 lg:px-6 lg:py-16">
        <div class="w-full max-w-[520px] rounded-[16px] bg-white/95 p-7 shadow-[0_20px_40px_-24px_rgba(0,0,0,0.5)] sm:p-10">
          <h1 class="font-display text-[34px] leading-tight sm:text-[40px]">{{ t(blok?.headline) }}</h1>
          <RichText v-if="hasRichText(blok?.hero_body)" :value="t(blok.hero_body)" class="mt-5 text-[15px] leading-relaxed text-[#121213]/85" />
          <p v-if="phone" class="mt-5 text-[15px]">
            Call us directly on
            <a :href="`tel:${phone.replace(/\s/g, '')}`" class="font-semibold underline underline-offset-2">{{ phone }}</a>
            or
          </p>
          <a
            v-if="blok?.cta_label"
            :href="ctaHref"
            class="mt-4 inline-flex items-center justify-center rounded-[5px] bg-[#8B6F4B] px-7 py-3 font-medium text-white transition hover:bg-[#6f583c]"
          >{{ blok.cta_label }}</a>
        </div>
      </div>
    </section>

    <ComponentCheck
      v-for="(b, i) in sections"
      :key="b._uid"
      :blok="b"
      :index="i"
    />

    <section class="border-t border-[#121213]/10 bg-[#f3f1ed]">
      <div class="mx-auto max-w-[1200px] space-y-3 px-4 py-10 text-xs leading-relaxed text-[#121213]/70 lg:px-6">
        <p>Please note, the Financial Conduct Authority does not regulate advice on taxation, Trusts or Estate Planning. Succession Wealth is a trading style of Succession Wealth Management Limited, which is authorised and regulated by the Financial Conduct Authority. Financial Services Register number 588378.</p>
        <p>Succession Wealth Management Limited is registered in England &amp; Wales at The Apex, Brest Road, Derriford Business Park, Derriford, Plymouth PL6 5FL. Registered Number: 07882611.</p>
        <p v-if="blok?.compliance_code" class="font-semibold">{{ blok.compliance_code }}</p>
      </div>
    </section>
  </article>
</template>
