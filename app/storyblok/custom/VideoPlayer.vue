<script setup>
defineProps({ blok: Object });
</script>

<template>
  <div v-if="blok?.video?.filename" class="video-player" v-editable="blok">
    <video
      :src="blok.video.filename"
      controls
      class="w-full max-w-2xl rounded-xl shadow-lg"
    ></video>
  </div>
</template>

<style scoped>
.video-player {
  display: flex;
  justify-content: center;
  padding: 1rem;
}
</style>
