<script setup>
const defaultFontFamilies = {
  // Sabon stand-in for section heads; thin Montserrat stands in for Aktiv Grotesk Thin on hero.
  '--font-family-display': '\'EB Garamond\', \'Palatino Linotype\', Palatino, serif',
  '--font-family-body': '\'Montserrat\', \'Hanken Grotesk\', system-ui, sans-serif',
  '--font-family-hero': '\'Montserrat\', system-ui, sans-serif',
};

// Succession Wealth palette. Bronze, cream and the accent yellow/teal come from
// successionwealth.co.uk; navy is the demo's dark anchor. This is only the
// fallback: the site-config story (use_custom_colors) overrides every value, so
// marketers can retune the brand without a deploy.
const defaultColors = {
  '--primary-highlight': '#8b6f4b',
  '--highlight-1': '#ffc40d',
  '--highlight-2': '#6b5434',
  '--highlight-3': '#4bc1ca',
  '--primary-background': '#f3f1ed',
  '--background-1': '#f7f5f1',
  '--background-2': '#e9e3d8',
  '--background-3': '#e4e8ef',
  '--background-4': '#d5dce8',
  '--background-5': '#efe6d6',
  '--background-6': '#f4efe4',
  '--background-7': '#dcebea',
  '--background-8': '#f4e8d6',
  '--background-9': '#ecddd2',
  '--background-10': '#e6eef0',
  '--primary-dark': '#121213',
};

// Small radii on purpose: a wealth brand reads as precise, not bubbly.
const defaultBorderRadiuses = {
  '--rounded_sm': '2px',
  '--rounded_default': '2px',
  '--rounded_md': '3px',
  '--rounded_lg': '4px',
  '--rounded_xl': '6px',
  '--rounded_2xl': '8px',
  '--rounded_3xl': '10px',
  '--rounded_full': '9999px',
};

const siteConfig = await getSiteConfig();

const cssVariables = computed(() => {
  if (!siteConfig.value) {
    return {
      ...defaultFontFamilies,
      ...defaultColors,
      ...defaultBorderRadiuses,
    };
  }

  const theme = {
    ...defaultFontFamilies,
    ...defaultColors,
    ...defaultBorderRadiuses,
  };

  if (siteConfig.value.content.use_custom_fonts) {
    if (siteConfig.value.content.custom_font_display) {
      theme['--font-family-display']
        = siteConfig.value.content.custom_font_display;
    }
    if (siteConfig.value.content.custom_font_body) {
      theme['--font-family-body'] = siteConfig.value.content.custom_font_body;
    }
  }
  else {
    Object.assign(theme, defaultFontFamilies);
  }
  if (siteConfig.value.content.use_custom_colors) {
    theme['--primary-highlight'] = siteConfig.value.content.primary_highlight_color?.color;
    theme['--highlight-1'] = siteConfig.value.content.highlight_1_color?.color;
    theme['--highlight-2'] = siteConfig.value.content.highlight_2_color?.color;
    theme['--highlight-3'] = siteConfig.value.content.highlight_3_color?.color;
    theme['--primary-background'] = siteConfig.value.content.primary_background_color?.color;
    theme['--background-1'] = siteConfig.value.content.background_1_color?.color;
    theme['--background-2'] = siteConfig.value.content.background_2_color?.color;
    theme['--background-3'] = siteConfig.value.content.background_3_color?.color;
    theme['--background-4'] = siteConfig.value.content.background_4_color?.color;
    theme['--background-5'] = siteConfig.value.content.background_5_color?.color;
    theme['--background-6'] = siteConfig.value.content.background_6_color?.color;
    theme['--background-7'] = siteConfig.value.content.background_7_color?.color;
    theme['--background-8'] = siteConfig.value.content.background_8_color?.color;
    theme['--background-9'] = siteConfig.value.content.background_9_color?.color;
    theme['--background-10'] = siteConfig.value.content.background_10_color?.color;
    theme['--primary-dark'] = siteConfig.value.content.primary_dark_color?.color;
    if (siteConfig.value.content.colored_headlines) {
      theme['--headline-color'] = siteConfig.value.content.primary_highlight_color?.color;
    }
    else {
      theme['--headline-color'] = siteConfig.value.content.primary_dark_color?.color;
    }
  }
  else {
    // TODO: enable colored headlines without changing colors
    Object.assign(theme, defaultColors);
    if (siteConfig.value.content.colored_headlines) {
      theme['--headline-color'] = defaultColors['--primary-highlight'];
    }
    else {
      theme['--headline-color'] = defaultColors['--primary-dark'];
    }
  }
  if (siteConfig.value.content.disable_rounded_corners) {
    for (const key in theme) {
      if (key.startsWith('--rounded_')) {
        theme[key] = 0;
      }
    }
  }
  else {
    Object.assign(theme, defaultBorderRadiuses);
  }
  const formattedVariables = Object.entries(theme)
    .map(([key, value]) => `${key}: ${value};`)
    .join('\n');

  return `:root {\n${formattedVariables}\n}`;
});

const viewingSiteConfig = useState('viewingSiteConfig');
// Set by the page from the campaign's "Hide site navigation" toggle.
const hideNavigation = useState('hideNavigation', () => false);

// Tracking IDs live in site-config (Tracking tab) so marketing can change them
// without a deploy. GTM is the recommended route: GA4, Hotjar and ad pixels are
// then managed inside Tag Manager. Never loaded inside the Visual Editor.
const trackingRoute = useRoute();
const trackingScripts = computed(() => {
  const c = siteConfig.value?.content || {};
  if (trackingRoute.query._storyblok !== undefined) {
    return [];
  }
  const scripts = [];
  if (/^GTM-[A-Z0-9]+$/.test(c.gtm_id || '')) {
    scripts.push({ key: 'gtm', children: `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','${c.gtm_id}');` });
  }
  if (/^G-[A-Z0-9]+$/.test(c.ga4_id || '')) {
    scripts.push({ key: 'ga4-src', src: `https://www.googletagmanager.com/gtag/js?id=${c.ga4_id}`, async: true });
    scripts.push({ key: 'ga4', children: `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${c.ga4_id}');` });
  }
  return scripts;
});
useHead({ script: trackingScripts });
const { customParent } = useRuntimeConfig().public;

onMounted(() => {
  useStoryblokBridge(
    siteConfig.value.id,
    evStory => (siteConfig.value = evStory),
    {
      preventClicks: true,
      customParent,
    },
  );
});

const headConfig = computed(() => ({
  style: [
    cssVariables.value,
  ],
  htmlAttrs: {
    lang: 'en',
  },
}));

useHead(headConfig);

const route = useRoute();
const currentSection = computed(() =>
  route.params.slug?.[0] || route.query.path?.split('/')[0] || '',
);

/**
 * The layout persists across client-side navigation, so re-resolve the
 * site-config (theme + nav) whenever the top-level section changes. Reuses
 * getSiteConfig so the nearest-ancestor walk, language, and release handling
 * stay identical to the initial load.
 */
watch(currentSection, async () => {
  siteConfig.value = (await getSiteConfig()).value;
});
</script>

<template>
  <main>
    <Header :logo="siteConfig.content.header_logo" :minimal="hideNavigation" />
    <div
      v-if="viewingSiteConfig && siteConfig.content.use_custom_colors"
      class="container py-12"
    >
      <h2 class="mb-8 text-4xl font-black text-(--headline-color)">Color Preview</h2>
      <div
        class="grid grid-cols-2 gap-8 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5"
      >
        <ColorPreview color="primary-highlight" />
        <ColorPreview color="highlight-1" />
        <ColorPreview color="highlight-2" />
        <ColorPreview color="highlight-3" />
        <ColorPreview color="primary-background" />
        <ColorPreview color="background-1" />
        <ColorPreview color="background-2" />
        <ColorPreview color="background-3" />
        <ColorPreview color="background-4" />
        <ColorPreview color="background-5" />
        <ColorPreview color="background-6" />
        <ColorPreview color="background-7" />
        <ColorPreview color="background-8" />
        <ColorPreview color="background-9" />
        <ColorPreview color="background-10" />
        <ColorPreview color="primary-dark" />
      </div>
    </div>
    <div
      v-if="viewingSiteConfig && siteConfig.content.use_custom_fonts"
      class="container py-12 text-primary-dark"
    >
      <h2 class="mb-4 text-4xl font-black text-(--headline-color)">Typography Preview</h2>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </p>
    </div>
    <slot></slot>
    <Footer
      :headline="siteConfig.content.footer_headline"
      :text-color="siteConfig.content.footer_text_color"
      :footer-light="siteConfig.content.footer_light"
      :decoration="siteConfig.content.footer_decoration"
      :logo="siteConfig.content.footer_logo"
      :about="siteConfig.content.footer_about"
      :nav-1-headline="siteConfig.content.footer_nav_1_headline"
      :nav-2-headline="siteConfig.content.footer_nav_2_headline"
      :nav-3-headline="siteConfig.content.footer_nav_3_headline"
      :nav-1="siteConfig.content.footer_nav_1"
      :nav-2="siteConfig.content.footer_nav_2"
      :nav-3="siteConfig.content.footer_nav_3"
      :x="siteConfig.content.x"
      :instagram="siteConfig.content.instagram"
      :youtube="siteConfig.content.youtube"
      :facebook="siteConfig.content.facebook"
      :minimal="hideNavigation"
    />
  </main>
</template>

<style>
@reference "~/assets/css/tailwind.css";

:root {
  --nav-background-color: #ffffff;
}

body {
  /* Sticky Succession header ~102px — no large fixed-header offset padding. */
  @apply text-[#121213] font-body antialiased overflow-x-clip;
}

section.page-section {
  @apply py-16 sm:py-20 md:py-24 lg:py-28 xl:py-32;
}

section.page-section.bg-white + section.page-section.bg-white,
section.page-section.bg-primary-background + section.page-section.bg-primary-background {
  @apply pt-0;
}
section.page-section.contact-form-section:last-child {
  /* Tailwind 4 removed the screen() function; lg is 64rem. */
  @media not all and (width >= 64rem) {
    @apply pb-0;
  }
}
</style>
