<script setup>
const props = defineProps({ item: Object, reducedFontWeight: Boolean });

const { query } = useRoute();
const inEditor = computed(() => !!query._storyblok);

const url = computed(() => getLinkUrl(props.item?.link));
</script>

<template>
  <NuxtLink
    v-editable="item"
    :to="inEditor ? '' : url"
    class="focus-ring relative flex h-full cursor-pointer items-center text-base transition-colors"
    :class="props.reducedFontWeight ? 'font-normal' : 'font-medium'"
  >
    {{ item.label }}
  </NuxtLink>
</template>
