<script setup>
const props = defineProps({
  blok: Object,
  showField: Function,
  fieldColumns: { type: String, default: '2' },
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
const labelClass = computed(() =>
  isDark.value ? 'font-semibold text-white/90' : 'font-semibold text-primary-dark',
);
const inputClass = computed(() =>
  isDark.value
    ? 'w-full rounded-sm border border-white/25 bg-white/95 px-3 py-2 text-primary-dark outline-none focus:border-primary-highlight'
    : 'w-full rounded-sm border border-primary-dark/15 bg-white px-3 py-2 text-primary-dark outline-none focus:border-primary-highlight',
);
const mutedClass = computed(() =>
  isDark.value ? 'text-white/75' : 'text-primary-dark/75',
);
const gridClass = computed(() =>
  props.fieldColumns === '1' ? 'grid gap-4' : 'grid gap-4 sm:grid-cols-2',
);

function onSubmit() {
  emit('submit', { ...form, extras: { ...form.extras } });
}
</script>

<template>
  <div>
    <header :class="compact ? 'mb-4' : 'mb-6 sm:mb-8'">
      <h2
        class="font-display font-medium leading-tight"
        :class="[
          compact ? 'text-2xl' : 'text-3xl md:text-4xl',
          isDark ? 'text-white' : 'text-primary-dark',
        ]"
      >
        {{ blok?.headline || 'Ready for a conversation?' }}
      </h2>
      <p v-if="blok?.intro" class="mt-3" :class="mutedClass">
        {{ blok.intro }}
      </p>
      <p v-if="plannerName || officeName" class="mt-2 text-sm font-semibold text-primary-highlight">
        <span v-if="plannerName">About {{ plannerName }}</span>
        <span v-if="plannerName && officeName"> · </span>
        <span v-if="officeName">{{ officeName }} office</span>
      </p>
    </header>

    <div
      v-if="submitted"
      class="rounded-lg border border-primary-highlight/40 bg-white p-6 text-primary-dark"
    >
      <p class="font-display text-2xl">
        {{ blok?.thank_you_message || 'Thank you — we will be in touch shortly.' }}
      </p>
    </div>

    <div
      v-else-if="formMode === 'mailchimp'"
      class="rounded-lg border border-dashed p-6"
      :class="isDark ? 'border-white/30 bg-white/10 text-white' : 'border-primary-dark/20 bg-primary-background text-primary-dark'"
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
      <p class="mt-4 text-sm opacity-70">
        In production Kyan wires the real embed. Storyblok holds the form ID, tags and thank-you page.
      </p>
    </div>

    <form v-else class="space-y-4" @submit.prevent="onSubmit">
      <div :class="gridClass">
        <label v-if="showField('first_name')" class="block text-sm">
          <span class="mb-1 block" :class="labelClass">First name*</span>
          <input v-model="form.first_name" required :class="inputClass" />
        </label>
        <label v-if="showField('surname')" class="block text-sm">
          <span class="mb-1 block" :class="labelClass">Surname*</span>
          <input v-model="form.surname" required :class="inputClass" />
        </label>
        <label
          v-if="showField('email')"
          class="block text-sm"
          :class="fieldColumns === '2' ? 'sm:col-span-2' : ''"
        >
          <span class="mb-1 block" :class="labelClass">Email*</span>
          <input v-model="form.email" type="email" required :class="inputClass" />
        </label>
        <label v-if="showField('phone')" class="block text-sm">
          <span class="mb-1 block" :class="labelClass">Phone</span>
          <input v-model="form.phone" type="tel" :class="inputClass" />
        </label>
        <label v-if="showField('postcode')" class="block text-sm">
          <span class="mb-1 block" :class="labelClass">Postcode*</span>
          <input v-model="form.postcode" required :class="inputClass" />
        </label>
        <label
          v-if="showField('investment_value')"
          class="block text-sm"
          :class="fieldColumns === '2' ? 'sm:col-span-2' : ''"
        >
          <span class="mb-1 block" :class="labelClass">Investment and pension value</span>
          <select v-model="form.investment_value" :class="inputClass">
            <option value="">
              Select a range
            </option>
            <option>£250k - £500k</option>
            <option>£500k+</option>
          </select>
        </label>
        <label
          v-if="showField('heard_about')"
          class="block text-sm"
          :class="fieldColumns === '2' ? 'sm:col-span-2' : ''"
        >
          <span class="mb-1 block" :class="labelClass">Where did you hear about us?</span>
          <select v-model="form.hear_about" :class="inputClass">
            <option value="">
              Select
            </option>
            <option>Search engine</option>
            <option>Recommendation</option>
            <option>Social media</option>
            <option>Event</option>
            <option>Magazine</option>
            <option>I'm already a client</option>
            <option>Other</option>
          </select>
        </label>

        <template v-for="field in extraFields" :key="field._uid">
          <label
            v-if="field.field_type !== 'checkbox'"
            class="block text-sm"
            :class="fieldColumns === '2' && field.field_type === 'textarea' ? 'sm:col-span-2' : ''"
          >
            <span class="mb-1 block" :class="labelClass">
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
              :placeholder="field.placeholder || ''"
              :class="inputClass"
            />
          </label>
          <label
            v-else
            class="flex items-start gap-2 text-sm"
            :class="fieldColumns === '2' ? 'sm:col-span-2' : ''"
          >
            <input v-model="form.extras[field.name]" type="checkbox" class="mt-1" :required="!!field.is_required" />
            <span :class="mutedClass">{{ field.label }}</span>
          </label>
        </template>
      </div>

      <div
        v-if="showAttribution"
        class="rounded-sm px-3 py-2 text-xs"
        :class="isDark ? 'bg-white/10 text-white/70' : 'bg-primary-background text-primary-dark/60'"
      >
        <p class="font-semibold" :class="isDark ? 'text-white/85' : 'text-primary-dark/80'">
          Attribution (auto-filled)
        </p>
        <p>Page: {{ page }} · Planner: {{ plannerName || '—' }} · Office: {{ officeName || '—' }}</p>
        <p v-if="form.topics">
          Topics: {{ form.topics }}
        </p>
        <p v-if="form.preference">
          Meeting preference: {{ form.preference }}
        </p>
      </div>

      <label class="flex items-start gap-2 text-sm" :class="mutedClass">
        <input v-model="form.marketing_opt_out" type="checkbox" class="mt-1" />
        <span>I do not wish to receive marketing communications from Succession Wealth</span>
      </label>
      <label class="flex items-start gap-2 text-sm" :class="mutedClass">
        <input v-model="form.privacy_consent" type="checkbox" required class="mt-1" />
        <span>
          I understand and accept the
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
        class="rounded-sm bg-primary-highlight px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-highlight-2 disabled:opacity-60"
        :disabled="submitting"
      >
        {{ blok?.submit_label || 'Request a conversation' }}
      </button>
    </form>
  </div>
</template>
