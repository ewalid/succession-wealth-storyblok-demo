<script setup>
const props = defineProps({
  blok: Object,
  showField: Function,
  fieldColumns: { type: String, default: '1' },
  plannerName: String,
  officeName: String,
  page: String,
  submitted: Boolean,
  submitting: Boolean,
  extraFields: { type: Array, default: () => [] },
  showAttribution: Boolean,
  formMode: { type: String, default: 'native' },
  tone: { type: String, default: 'light' },
  compact: Boolean,
  initialPostcode: { type: String, default: '' },
  initialTopics: { type: String, default: '' },
  initialPreference: { type: String, default: '' },
});

const emit = defineEmits(['submit']);

const form = reactive({
  first_name: '',
  surname: '',
  email: '',
  phone: '',
  postcode: props.initialPostcode || '',
  investment_value: '',
  hear_about: '',
  topics: props.initialTopics || '',
  preference: props.initialPreference || '',
  marketing_opt_out: false,
  privacy_consent: false,
  extras: {},
});

const isDark = computed(() => props.tone === 'dark');
const choiceStyle = computed(() => props.blok?.choice_style || 'radios');
const inputStyle = computed(() => props.blok?.input_style || 'placeholder');
const usePlaceholders = computed(() => inputStyle.value === 'placeholder');
const twoCol = computed(() => props.fieldColumns === '2' && !props.compact);

const labelClass = computed(() =>
  isDark.value ? 'mb-1 block text-sm font-medium text-white/90' : 'mb-1 block text-sm font-medium text-[#121213]',
);
const inputClass = computed(() =>
  isDark.value
    ? 'w-full rounded-[6px] border border-white/25 bg-white px-4 py-3.5 text-[#121213] outline-none placeholder:text-[#121213]/45 focus:border-[#8B6F4B]'
    : 'w-full rounded-[6px] border border-[#121213]/20 bg-white px-4 py-3.5 text-[#121213] outline-none placeholder:text-[#121213]/45 focus:border-[#8B6F4B]',
);
const mutedClass = computed(() =>
  isDark.value ? 'text-white/80' : 'text-[#121213]/75',
);
const gridClass = computed(() =>
  twoCol.value ? 'grid gap-4 sm:grid-cols-2' : 'grid gap-4',
);
const questionClass = computed(() =>
  isDark.value ? 'mb-3 block text-sm font-medium text-white' : 'mb-3 block text-sm font-medium text-[#121213]',
);

const investmentOptions = ['£250k - £500k', '£500k+'];
const heardOptions = [
  'Search engine',
  'Recommendation',
  'Social media',
  'Event',
  'Magazine',
  'I\'m already a client',
  'Other',
];

function onSubmit() {
  emit('submit', { ...form, extras: { ...form.extras } });
}
</script>

<template>
  <div :class="compact ? 'max-w-none' : 'mx-auto max-w-xl'">
    <header :class="compact ? 'mb-4' : 'mb-8'">
      <h2
        class="font-display font-normal leading-tight"
        :class="[
          compact ? 'text-2xl' : 'text-[2rem] md:text-[2.5rem]',
          isDark ? 'text-white' : 'text-[#121213]',
        ]"
      >
        {{ blok?.headline || 'Ready for a conversation?' }}
      </h2>
      <RichText
        v-if="hasRichText(blok?.intro)"
        :value="blok.intro"
        class="mt-4 text-base leading-relaxed"
        :class="mutedClass"
      />
      <p v-if="plannerName || officeName" class="mt-2 text-sm font-semibold text-[#8B6F4B]">
        <span v-if="plannerName">About {{ plannerName }}</span>
        <span v-if="plannerName && officeName"> · </span>
        <span v-if="officeName">{{ officeName }} office</span>
      </p>
    </header>

    <div
      v-if="submitted"
      class="rounded-[6px] border border-[#8B6F4B]/35 bg-white p-6 text-[#121213]"
    >
      <RichText v-if="hasRichText(blok?.thank_you_message)" :value="blok.thank_you_message" class="font-display text-2xl" />
      <p v-else class="font-display text-2xl">
        Thank you — we will be in touch shortly.
      </p>
    </div>

    <div
      v-else-if="formMode === 'mailchimp'"
      class="rounded-[6px] border border-dashed p-6"
      :class="isDark ? 'border-white/30 bg-white/10 text-white' : 'border-[#121213]/20 bg-white text-[#121213]'"
    >
      <p class="font-display text-xl">
        Mailchimp form
      </p>
      <p class="mt-2 text-sm opacity-80">
        Form ID: {{ blok?.mailchimp_form_id || 'Add a Mailchimp form ID in the sidebar' }}
      </p>
      <p v-if="blok?.mailchimp_tags" class="mt-1 text-sm opacity-80">
        Tags: {{ blok.mailchimp_tags }}
      </p>
    </div>

    <form v-else class="space-y-5" @submit.prevent="onSubmit">
      <div :class="gridClass">
        <label v-if="showField('first_name')" class="block">
          <span v-if="!usePlaceholders" :class="labelClass">First Name*</span>
          <input
            v-model="form.first_name"
            required
            :placeholder="usePlaceholders ? 'First Name*' : ''"
            :aria-label="usePlaceholders ? 'First Name' : undefined"
            :class="inputClass"
          />
        </label>
        <label v-if="showField('surname')" class="block">
          <span v-if="!usePlaceholders" :class="labelClass">Surname*</span>
          <input
            v-model="form.surname"
            required
            :placeholder="usePlaceholders ? 'Surname*' : ''"
            :aria-label="usePlaceholders ? 'Surname' : undefined"
            :class="inputClass"
          />
        </label>
        <label v-if="showField('email')" class="block" :class="twoCol ? 'sm:col-span-2' : ''">
          <span v-if="!usePlaceholders" :class="labelClass">Email address*</span>
          <input
            v-model="form.email"
            type="email"
            required
            :placeholder="usePlaceholders ? 'Email address*' : ''"
            :aria-label="usePlaceholders ? 'Email address' : undefined"
            :class="inputClass"
          />
        </label>
        <label v-if="showField('phone')" class="block">
          <span v-if="!usePlaceholders" :class="labelClass">Phone number</span>
          <input
            v-model="form.phone"
            type="tel"
            :placeholder="usePlaceholders ? 'Phone number' : ''"
            :aria-label="usePlaceholders ? 'Phone number' : undefined"
            :class="inputClass"
          />
        </label>
        <label v-if="showField('postcode')" class="block">
          <span v-if="!usePlaceholders" :class="labelClass">Postcode*</span>
          <input
            v-model="form.postcode"
            required
            :placeholder="usePlaceholders ? 'Postcode*' : ''"
            :aria-label="usePlaceholders ? 'Postcode' : undefined"
            :class="inputClass"
          />
        </label>

        <fieldset
          v-if="showField('investment_value')"
          class="min-w-0"
          :class="twoCol ? 'sm:col-span-2' : ''"
        >
          <legend :class="questionClass">
            What is your total investment and pension value?
          </legend>
          <div v-if="choiceStyle === 'radios'" class="flex flex-wrap gap-x-6 gap-y-2">
            <label
              v-for="opt in investmentOptions"
              :key="opt"
              class="inline-flex items-center gap-2 text-sm"
              :class="mutedClass"
            >
              <input v-model="form.investment_value" type="radio" name="investment_value" :value="opt" class="size-4 accent-[#8B6F4B]" />
              <span>{{ opt }}</span>
            </label>
          </div>
          <select v-else v-model="form.investment_value" :class="inputClass">
            <option value="">
              Select a range
            </option>
            <option v-for="opt in investmentOptions" :key="opt" :value="opt">
              {{ opt }}
            </option>
          </select>
        </fieldset>

        <fieldset
          v-if="showField('heard_about')"
          class="min-w-0"
          :class="twoCol ? 'sm:col-span-2' : ''"
        >
          <legend :class="questionClass">
            Where did you hear about us?
          </legend>
          <div v-if="choiceStyle === 'radios'" class="flex flex-wrap gap-x-6 gap-y-2">
            <label
              v-for="opt in heardOptions"
              :key="opt"
              class="inline-flex items-center gap-2 text-sm"
              :class="mutedClass"
            >
              <input v-model="form.hear_about" type="radio" name="hear_about" :value="opt" class="size-4 accent-[#8B6F4B]" />
              <span>{{ opt }}</span>
            </label>
          </div>
          <select v-else v-model="form.hear_about" :class="inputClass">
            <option value="">
              Select
            </option>
            <option v-for="opt in heardOptions" :key="opt" :value="opt">
              {{ opt }}
            </option>
          </select>
        </fieldset>

        <template v-for="field in extraFields" :key="field._uid">
          <label
            v-if="field.field_type !== 'checkbox'"
            class="block"
            :class="[
              twoCol && (field.width !== 'half' || field.field_type === 'textarea') ? 'sm:col-span-2' : '',
              !twoCol ? '' : '',
            ]"
          >
            <span v-if="!usePlaceholders || field.field_type === 'select' || field.field_type === 'radio' || field.field_type === 'textarea'" :class="labelClass">
              {{ field.label }}<span v-if="field.is_required">*</span>
            </span>
            <textarea
              v-if="field.field_type === 'textarea'"
              v-model="form.extras[field.name]"
              :required="!!field.is_required"
              :rows="field.rows || 4"
              :placeholder="field.placeholder || ''"
              :class="inputClass"
            ></textarea>
            <div
              v-else-if="(field.field_type === 'radio' || field.field_type === 'select') && choiceStyle === 'radios' && field.field_type === 'radio'"
              class="flex flex-wrap gap-x-6 gap-y-2"
            >
              <label
                v-for="opt in (field.options || [])"
                :key="opt._uid || opt.value || opt.label"
                class="inline-flex items-center gap-2 text-sm"
                :class="mutedClass"
              >
                <input
                  v-model="form.extras[field.name]"
                  type="radio"
                  :name="field.name"
                  :value="opt.value || opt.label"
                  class="size-4 accent-[#8B6F4B]"
                  :required="!!field.is_required"
                />
                <span>{{ opt.label || opt.value }}</span>
              </label>
            </div>
            <select
              v-else-if="field.field_type === 'select' || field.field_type === 'radio'"
              v-model="form.extras[field.name]"
              :required="!!field.is_required"
              :class="inputClass"
            >
              <option value="">
                Select
              </option>
              <option
                v-for="opt in (field.options || [])"
                :key="opt._uid || opt.value"
                :value="opt.value || opt.label"
              >
                {{ opt.label || opt.value }}
              </option>
            </select>
            <input
              v-else
              v-model="form.extras[field.name]"
              :type="field.field_type === 'email' ? 'email' : field.field_type === 'tel' ? 'tel' : 'text'"
              :required="!!field.is_required"
              :placeholder="usePlaceholders ? (field.placeholder || field.label) : (field.placeholder || '')"
              :class="inputClass"
            />
          </label>
          <label
            v-else
            class="flex items-start gap-2 text-sm"
            :class="[mutedClass, twoCol ? 'sm:col-span-2' : '']"
          >
            <input v-model="form.extras[field.name]" type="checkbox" class="mt-1 size-4 accent-[#8B6F4B]" :required="!!field.is_required" />
            <span>{{ field.label }}</span>
          </label>
        </template>
      </div>

      <div
        v-if="showAttribution"
        class="rounded-[6px] px-3 py-2 text-xs"
        :class="isDark ? 'bg-white/10 text-white/70' : 'bg-white text-[#121213]/60'"
      >
        <p class="font-semibold">
          Attribution (auto-filled)
        </p>
        <p>Page: {{ page }} · Planner: {{ plannerName || '—' }} · Office: {{ officeName || '—' }}</p>
      </div>

      <label class="flex items-start gap-2 text-sm" :class="mutedClass">
        <input v-model="form.marketing_opt_out" type="checkbox" class="mt-1 size-4 accent-[#8B6F4B]" />
        <span>I do not wish to receive marketing communications from Succession Wealth</span>
      </label>
      <label class="flex items-start gap-2 text-sm" :class="mutedClass">
        <input v-model="form.privacy_consent" type="checkbox" required class="mt-1 size-4 accent-[#8B6F4B]" />
        <span>
          Please tick this box to confirm you fully understand and accept the
          <a
            :href="getLinkUrl(blok?.privacy_url) || '#'"
            class="underline"
            target="_blank"
            rel="noopener"
          >Privacy Policy</a>*
        </span>
      </label>

      <button
        type="submit"
        class="rounded-[5px] bg-[#8B6F4B] px-8 py-3 text-base font-medium text-white transition hover:bg-[#6f583c] disabled:opacity-60"
        :disabled="submitting"
      >
        {{ blok?.submit_label || 'Submit details' }}
      </button>
    </form>
  </div>
</template>
