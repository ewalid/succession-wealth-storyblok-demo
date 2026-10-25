<script setup>
const props = defineProps({ blok: Object, index: Number, planner: Object, office: Object, pageSlug: String });

const route = useRoute();
const answers = readFinderAnswers();
const attribution = captureAttribution();

const form = reactive({
  first_name: '',
  surname: '',
  email: '',
  phone: '',
  postcode: answers.postcode || '',
  investment_value: '',
  hear_about: '',
  topics: (answers.topics || []).join(', '),
  preference: answers.preference || '',
  marketing_opt_out: false,
  privacy_consent: false,
});

const submitted = ref(false);
const submitting = ref(false);

const plannerName = computed(() => plannerFullName(props.planner?.content) || props.planner?.name || '');
const officeName = computed(() => props.office?.content?.name || props.office?.name || '');
const page = computed(() => props.pageSlug || route.path);

async function onSubmit() {
  if (!form.privacy_consent) {
    return;
  }
  submitting.value = true;
  try {
    // Demo: no real Mailchimp — capture payload locally so the beat still works.
    if (import.meta.client) {
      window.sessionStorage.setItem('sw_lead_demo', JSON.stringify({
        ...form,
        planner: plannerName.value,
        office: officeName.value,
        page: page.value,
        template: props.blok?.component || 'lead_form',
        ...attribution,
        at: new Date().toISOString(),
      }));
    }
    submitted.value = true;
  }
  finally {
    submitting.value = false;
  }
}
</script>

<template>
  <section v-editable="blok" class="page-section bg-background-2">
    <div class="container max-w-2xl">
      <header class="mb-8">
        <h2 class="font-display text-3xl font-medium text-primary-dark md:text-4xl">
          {{ blok?.headline || 'Ready for a conversation?' }}
        </h2>
        <p class="mt-3 text-primary-dark/75">
          {{ blok?.intro || 'Share your details and a member of our team will be in touch.' }}
        </p>
        <p v-if="plannerName || officeName" class="mt-2 text-sm text-highlight-2">
          <span v-if="plannerName">About {{ plannerName }}</span>
          <span v-if="plannerName && officeName"> · </span>
          <span v-if="officeName">{{ officeName }} office</span>
        </p>
      </header>

      <div v-if="submitted" class="rounded-lg border border-primary-highlight/40 bg-white p-6">
        <p class="font-display text-2xl text-primary-dark">
          {{ blok?.thank_you_message || 'Thank you — we will be in touch shortly.' }}
        </p>
      </div>

      <form v-else class="space-y-4 rounded-lg bg-white p-5 shadow-sm sm:p-8" @submit.prevent="onSubmit">
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block text-sm">
            <span class="mb-1 block font-semibold">First name*</span>
            <input v-model="form.first_name" required class="w-full rounded-sm border border-primary-dark/15 px-3 py-2" />
          </label>
          <label class="block text-sm">
            <span class="mb-1 block font-semibold">Surname*</span>
            <input v-model="form.surname" required class="w-full rounded-sm border border-primary-dark/15 px-3 py-2" />
          </label>
          <label class="block text-sm sm:col-span-2">
            <span class="mb-1 block font-semibold">Email*</span>
            <input v-model="form.email" type="email" required class="w-full rounded-sm border border-primary-dark/15 px-3 py-2" />
          </label>
          <label class="block text-sm">
            <span class="mb-1 block font-semibold">Phone</span>
            <input v-model="form.phone" type="tel" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2" />
          </label>
          <label class="block text-sm">
            <span class="mb-1 block font-semibold">Postcode*</span>
            <input v-model="form.postcode" required class="w-full rounded-sm border border-primary-dark/15 px-3 py-2" />
          </label>
        </div>

        <label class="block text-sm">
          <span class="mb-1 block font-semibold">Investment and pension value</span>
          <select v-model="form.investment_value" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2">
            <option value="">Select a range</option>
            <option>£250k - £500k</option>
            <option>£500k+</option>
          </select>
        </label>

        <label class="block text-sm">
          <span class="mb-1 block font-semibold">Where did you hear about us?</span>
          <select v-model="form.hear_about" class="w-full rounded-sm border border-primary-dark/15 px-3 py-2">
            <option value="">Select</option>
            <option>Search engine</option>
            <option>Recommendation</option>
            <option>Social media</option>
            <option>Event</option>
            <option>Magazine</option>
            <option>I'm already a client</option>
            <option>Other</option>
          </select>
        </label>

        <!-- Hidden attribution fields (shown lightly in editor for demos) -->
        <div class="rounded-sm bg-primary-background px-3 py-2 text-xs text-primary-dark/60">
          <p class="font-semibold text-primary-dark/80">Attribution (auto-filled)</p>
          <p>Page: {{ page }} · Planner: {{ plannerName || '—' }} · Office: {{ officeName || '—' }}</p>
          <p v-if="form.topics">Topics: {{ form.topics }}</p>
          <p v-if="form.preference">Meeting preference: {{ form.preference }}</p>
          <p v-if="blok?.hidden_fields_note">{{ blok.hidden_fields_note }}</p>
        </div>

        <label class="flex items-start gap-2 text-sm">
          <input v-model="form.marketing_opt_out" type="checkbox" class="mt-1" />
          <span>I do not wish to receive marketing communications from Succession Wealth</span>
        </label>
        <label class="flex items-start gap-2 text-sm">
          <input v-model="form.privacy_consent" type="checkbox" required class="mt-1" />
          <span>
            I understand and accept the
            <a :href="getLinkUrl(blok?.privacy_url) || '#'" class="underline" target="_blank" rel="noopener">Privacy Policy</a>*
          </span>
        </label>

        <button
          type="submit"
          class="rounded-sm bg-primary-highlight px-5 py-2.5 text-sm font-semibold text-white hover:bg-highlight-2 disabled:opacity-60"
          :disabled="submitting"
        >
          {{ blok?.submit_label || 'Submit details' }}
        </button>
      </form>
    </div>
  </section>
</template>
