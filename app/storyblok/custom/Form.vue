<script setup>
defineProps({ blok: Object });
</script>

<template>
  <div v-editable="blok">
    <FormLayout :settings="blok" :fields="blok.fields || []" :button-text="blok.button_text || 'Submit'" editable />
  </div>
</template>
