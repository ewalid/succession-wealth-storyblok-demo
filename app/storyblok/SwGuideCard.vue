<script setup>
defineProps({ blok: Object });
</script>

<template>
  <!-- Nestable item rendered only inside SwGuides -->
  <div v-editable="blok" class="hidden"></div>
</template>
