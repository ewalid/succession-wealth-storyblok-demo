<script setup>
const props = defineProps({
  blok: Object,
  index: Number,
  planner: Object,
  office: Object,
  pageSlug: String,
});

const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);
const answers = readFinderAnswers();
const attribution = captureAttribution();

const layout = computed(() => props.blok?.layout || 'stacked');
const background = computed(() => props.blok?.background || 'cream');
const formMode = computed(() => props.blok?.form_mode || 'native');
const fieldColumns = computed(() => String(props.blok?.field_columns || '1'));
const formWidth = computed(() => props.blok?.form_width || 'medium');
const imagePosition = computed(() => props.blok?.image_position || 'right');
/** Full-width form vs half form + side image (marketer-facing control). */
const isSplit = computed(() =>
  props.blok?.page_layout === 'split' || props.blok?.layout === 'split_image',
);

const selectedFields = computed(() => {
  const raw = props.blok?.fields;
  if (Array.isArray(raw) && raw.length) {
    return raw;
  }
  if (typeof raw === 'string' && raw) {
    return raw.split(',').map(s => s.trim()).filter(Boolean);
  }
  return ['first_name', 'surname', 'email', 'phone', 'postcode', 'investment_value', 'heard_about'];
});

function showField(name) {
  if (['first_name', 'surname', 'email'].includes(name)) {
    return true;
  }
  return selectedFields.value.includes(name);
}

const submitted = ref(false);
const submitting = ref(false);

const plannerName = computed(() => plannerFullName(props.planner?.content) || props.planner?.name || '');
const officeName = computed(() => props.office?.content?.name || props.office?.name || '');
const page = computed(() => props.pageSlug || route.path);

const sideImage = computed(() => getOptimizedImage(props.blok?.side_image, 900, 1100));
const bgImage = computed(() => getOptimizedImage(props.blok?.background_image, 1800, 1000));

const widthClass = computed(() => ({
  narrow: 'max-w-lg',
  medium: 'max-w-2xl',
  wide: 'max-w-4xl',
}[formWidth.value] || 'max-w-2xl'));

const sectionTone = computed(() => {
  if (layout.value === 'dark_panel' || background.value === 'navy') {
    return 'dark';
  }
  if (background.value === 'bronze') {
    return 'bronze';
  }
  return 'light';
});

const sectionClass = computed(() => {
  const map = {
    cream: 'bg-primary-background text-primary-dark',
    white: 'bg-white text-primary-dark',
    navy: 'bg-primary-dark text-white',
    bronze: 'bg-primary-highlight text-white',
    image: 'bg-primary-dark text-white',
  };
  return map[background.value] || map.navy;
});

const showAttribution = computed(() =>
  inEditor.value || !!props.blok?.show_attribution_preview,
);

const extraFields = computed(() => props.blok?.extra_fields || []);
const fieldTone = computed(() => (sectionTone.value === 'light' ? 'light' : 'dark'));

async function onSubmit(payload) {
  if (!payload?.privacy_consent) {
    return;
  }
  submitting.value = true;
  try {
    if (import.meta.client) {
      window.sessionStorage.setItem('sw_lead_demo', JSON.stringify({
        ...payload,
        planner: plannerName.value,
        office: officeName.value,
        page: page.value,
        template: props.blok?.component || 'lead_form',
        layout: layout.value,
        ...attribution,
        at: new Date().toISOString(),
      }));
    }
    const thankYou = getLinkUrl(props.blok?.thank_you_page);
    if (thankYou) {
      await navigateTo(thankYou);
      return;
    }
    submitted.value = true;
  }
  finally {
    submitting.value = false;
  }
}
</script>

<template>
  <section
    id="lead-form"
    v-editable="blok"
    class="relative overflow-hidden"
    :class="[
      sectionClass,
      layout === 'compact' ? 'py-8 md:py-10' : 'page-section',
    ]"
  >
    <img
      v-if="(background === 'image' || layout === 'full_bleed') && bgImage"
      :src="bgImage"
      alt=""
      class="absolute inset-0 size-full object-cover"
      :class="layout === 'full_bleed' ? 'opacity-45' : 'opacity-35'"
    />
    <div
      v-if="background === 'image' || layout === 'full_bleed'"
      class="absolute inset-0 bg-primary-dark/55"
    ></div>

    <div class="container relative" :class="isSplit ? 'max-w-6xl' : ''">
      <div
        v-if="isSplit"
        class="grid items-stretch gap-0 overflow-hidden rounded-lg bg-white text-primary-dark shadow-xl lg:grid-cols-2"
        :class="imagePosition === 'left' ? 'lg:[direction:rtl]' : ''"
      >
        <div class="p-6 sm:p-10 lg:[direction:ltr]">
          <LeadFormFields
            :blok="blok"
            :show-field="showField"
            :field-columns="fieldColumns"
            :planner-name="plannerName"
            :office-name="officeName"
            :page="page"
            :submitted="submitted"
            :submitting="submitting"
            :extra-fields="extraFields"
            :show-attribution="showAttribution"
            :form-mode="formMode"
            :initial-postcode="answers.postcode || ''"
            :initial-topics="(answers.topics || []).join(', ')"
            :initial-preference="answers.preference || ''"
            tone="light"
            @submit="onSubmit"
          />
        </div>
        <div class="relative min-h-72 bg-background-2 lg:min-h-full lg:[direction:ltr]">
          <img
            v-if="sideImage"
            :src="sideImage"
            :alt="blok?.side_image?.alt || ''"
            class="absolute inset-0 size-full object-cover"
          />
          <div
            v-else
            class="absolute inset-0 flex items-center justify-center bg-primary-dark p-8 text-center text-white/80"
          >
            <p class="font-display text-2xl">
              {{ inEditor ? 'Add a side image in the sidebar' : 'Succession Wealth' }}
            </p>
          </div>
        </div>
      </div>

      <div
        v-else-if="layout === 'compact'"
        class="mx-auto rounded-lg bg-white/95 p-5 text-primary-dark shadow-lg sm:p-6"
        :class="widthClass"
      >
        <LeadFormFields
          :blok="blok"
          :show-field="showField"
          :field-columns="fieldColumns"
          :planner-name="plannerName"
          :office-name="officeName"
          :page="page"
          :submitted="submitted"
          :submitting="submitting"
          :extra-fields="extraFields"
          :show-attribution="false"
          :form-mode="formMode"
          :initial-postcode="answers.postcode || ''"
          :initial-topics="(answers.topics || []).join(', ')"
          :initial-preference="answers.preference || ''"
          compact
          tone="light"
          @submit="onSubmit"
        />
      </div>

      <div
        v-else
        class="mx-auto"
        :class="[
          widthClass,
          layout === 'two_column_wide' ? 'max-w-4xl' : '',
        ]"
      >
        <!-- Dark/bronze panels keep a frosted card; cream/white Succession look is flush on the section. -->
        <div
          :class="sectionTone === 'dark' || sectionTone === 'bronze'
            ? 'rounded-lg bg-white/10 p-5 shadow-sm backdrop-blur-sm sm:p-8'
            : layout === 'stacked' ? 'py-2' : 'rounded-lg bg-white p-5 text-primary-dark shadow-sm sm:p-8'"
        >
          <LeadFormFields
            :blok="blok"
            :show-field="showField"
            :field-columns="fieldColumns"
            :planner-name="plannerName"
            :office-name="officeName"
            :page="page"
            :submitted="submitted"
            :submitting="submitting"
            :extra-fields="extraFields"
            :show-attribution="showAttribution"
            :form-mode="formMode"
            :initial-postcode="answers.postcode || ''"
            :initial-topics="(answers.topics || []).join(', ')"
            :initial-preference="answers.preference || ''"
            :tone="fieldTone"
            @submit="onSubmit"
          />
        </div>
      </div>
    </div>
  </section>
</template>
