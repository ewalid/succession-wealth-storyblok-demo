<script setup>
const props = defineProps({ blok: Object });

watchEffect(() => {
  const title = props.blok?.title;
  const description = props.blok?.description;
  const og = props.blok?.og_image?.filename;
  const noindex = !!props.blok?.noindex;
  useHead({
    title: title || undefined,
    meta: [
      description ? { name: 'description', content: description } : null,
      og ? { property: 'og:image', content: og } : null,
      title ? { property: 'og:title', content: title } : null,
      description ? { property: 'og:description', content: description } : null,
      noindex ? { name: 'robots', content: 'noindex,nofollow' } : null,
    ].filter(Boolean),
  });
});
</script>

<template>
  <!-- Invisible SEO block — fields edit in the sidebar -->
  <div v-editable="blok" class="sr-only" aria-hidden="true">SEO</div>
</template>
