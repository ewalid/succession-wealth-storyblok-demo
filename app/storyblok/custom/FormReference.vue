<script setup>
const props = defineProps({ blok: Object });

const primaryForm = computed(() => {
  if (props.blok.form && typeof props.blok.form === 'object' && !Array.isArray(props.blok.form)) {
    return props.blok.form;
  }
  if (Array.isArray(props.blok.forms) && props.blok.forms.length) {
    return props.blok.forms[0];
  }
  return undefined;
});

const formFields = computed(() => {
  const inlineFields = Array.isArray(props.blok.fields) ? props.blok.fields : [];
  const formContentFields = primaryForm.value?.content?.fields ?? primaryForm.value?.fields ?? [];
  return [...inlineFields, ...formContentFields];
});

const buttonLabel = computed(() => {
  return props.blok.button_text
    || primaryForm.value?.content?.button_text
    || primaryForm.value?.button_text
    || 'Submit';
});
</script>

<template>
  <div v-editable="blok">
    <!-- Layout, image and intro come from the referenced Form; Title overrides its heading -->
    <FormLayout
      :settings="primaryForm?.content || primaryForm || {}"
      :fields="formFields"
      :button-text="buttonLabel"
      :headline="blok.title || ''"
    />
  </div>
</template>
