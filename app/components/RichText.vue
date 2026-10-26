<script setup>
/** Renders a rich-text field, or a legacy plain string, inheriting the parent's type styles. */
defineProps({ value: { type: [String, Object], default: null } });
</script>

<template>
  <p v-if="typeof value === 'string'" class="whitespace-pre-line">{{ value }}</p>
  <div
    v-else-if="value"
    class="rich-text [&_a]:underline [&_a]:underline-offset-2 [&_li]:mt-1 [&_ol]:list-decimal [&_ol]:pl-5 [&_p+p]:mt-3 [&_p:empty]:hidden [&_strong]:font-semibold [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:mt-3 [&_ol]:mt-3"
  >
    <StoryblokRichText :document="value" />
  </div>
</template>
