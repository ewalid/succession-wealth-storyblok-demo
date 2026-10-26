<script setup>
defineProps({ blok: Object });
</script>

<template>
  <div v-editable="blok" class="hidden"></div>
</template>
