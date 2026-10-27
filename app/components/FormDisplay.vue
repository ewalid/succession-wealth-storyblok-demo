<script setup>
defineProps({
  fields: Array,
  buttonText: {
    type: String,
    default: 'Submit',
  },
  editable: Boolean,
  successMessage: { type: String, default: '' },
  buttonAlign: { type: String, default: 'left' },
});

const formStatus = ref('idle');
let submitTimer = null;
let resetTimer = null;

const submit = (event) => {
  if (formStatus.value === 'submitting') {
    return;
  }
  const form = event.target;
  formStatus.value = 'submitting';
  submitTimer = setTimeout(() => {
    formStatus.value = 'success';
    form.reset();
    resetTimer = setTimeout(() => {
      formStatus.value = 'idle';
    }, 4000);
  }, 500);
};

onBeforeUnmount(() => {
  clearTimeout(submitTimer);
  clearTimeout(resetTimer);
});
</script>

<template>
  <form
    v-if="fields?.length"
    class="grid grid-cols-12 gap-4"
    @submit.prevent="submit"
  >
    <FormFields :fields="fields" :editable="editable" />

    <p class="col-span-12 text-xs text-neutral-500">
      * indicates a required field
    </p>

    <button
      type="submit"
      :disabled="formStatus === 'submitting'"
      class="focus-ring col-span-12 inline-flex w-full items-center justify-center rounded-[5px] bg-[#8b6f4b] px-8 py-3 font-semibold tracking-wide text-white transition hover:bg-[#6f583c] disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
      :class="{ 'sm:justify-self-start': buttonAlign === 'left', 'sm:justify-self-center': buttonAlign === 'center', 'sm:w-full': buttonAlign === 'full' }"
    >
      {{ formStatus === 'submitting' ? 'Submitting\u2026' : buttonText }}
    </button>

    <Transition name="fade">
      <p
        v-if="formStatus === 'success'"
        class="col-span-12 text-sm font-medium text-green-700"
      >
        {{ successMessage || 'Thanks! Your submission has been received.' }}
      </p>
    </Transition>
  </form>
</template>
