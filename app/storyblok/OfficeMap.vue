<script setup>
import { onBeforeUnmount, watchEffect } from 'vue';

const props = defineProps({ blok: Object, index: Number });
const api = useStoryblokApi();
const version = getVersion();
const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);

const mapEl = ref(null);
const office = ref(null);
const planner = ref(null);
let map;
let leaflet;

const officeKey = computed(() => {
  const v = props.blok?.office;
  return typeof v === 'string' ? v : v?.uuid || '';
});
const plannerKey = computed(() => {
  const v = props.blok?.planner;
  return typeof v === 'string' ? v : v?.uuid || '';
});

watch(
  () => [officeKey.value, plannerKey.value],
  async () => {
    office.value = await resolveStory(api, props.blok?.office, { version });
    planner.value = await resolveStory(api, props.blok?.planner, {
      version,
      resolve_relations: 'planner.office',
    });
  },
  { immediate: true },
);

const coords = computed(() => officeCoordinates(office.value));
const radius = computed(() => toNumber(planner.value?.content?.home_visit_radius_miles));
const directionsUrl = computed(() => {
  if (!coords.value) {
    return '';
  }
  return `https://www.google.com/maps/dir/?api=1&destination=${coords.value.lat},${coords.value.lng}`;
});

async function ensureLeaflet() {
  if (leaflet) {
    return leaflet;
  }
  leaflet = await import('leaflet');
  await import('leaflet/dist/leaflet.css');
  // Fix default marker icons under Vite
  delete leaflet.Icon.Default.prototype._getIconUrl;
  leaflet.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  });
  return leaflet;
}

watchEffect(async (onCleanup) => {
  if (!import.meta.client || !mapEl.value || !coords.value) {
    return;
  }
  const L = await ensureLeaflet();
  if (map) {
    map.remove();
    map = null;
  }
  map = L.map(mapEl.value, { scrollWheelZoom: false, attributionControl: true });
  map.setView([coords.value.lat, coords.value.lng], 11);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 18,
  }).addTo(map);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 18,
    pane: 'shadowPane',
  }).addTo(map);
  L.marker([coords.value.lat, coords.value.lng]).addTo(map);
  if (radius.value) {
    L.circle([coords.value.lat, coords.value.lng], {
      radius: radius.value * 1609.34,
      color: '#8b6f4b',
      fillColor: '#8b6f4b',
      fillOpacity: 0.12,
      weight: 2,
    }).addTo(map);
  }
  onCleanup(() => {
    if (map) {
      map.remove();
      map = null;
    }
  });
});

onBeforeUnmount(() => {
  if (map) {
    map.remove();
    map = null;
  }
});
</script>

<template>
  <section
    v-if="inEditor || officeKey"
    v-editable="blok"
    class="page-section bg-primary-background"
  >
    <div class="container">
      <div
        v-if="!officeKey"
        class="rounded-lg border border-dashed border-primary-highlight bg-white p-8 text-center"
      >
        <p class="font-display text-2xl text-primary-dark">Pick an office in the sidebar</p>
        <p class="mt-2 text-sm text-primary-dark/70">The map uses the office latitude and longitude from Storyblok.</p>
      </div>
      <div v-else class="overflow-hidden rounded-lg border border-primary-dark/10 bg-white">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-primary-dark/10 px-5 py-4">
          <div>
            <h3 class="font-display text-2xl text-primary-dark">
              {{ office?.content?.name || 'Office' }}
            </h3>
            <p v-if="office?.content?.address" class="mt-1 whitespace-pre-line text-sm text-primary-dark/70">
              {{ office.content.address }}
            </p>
            <p v-if="radius" class="mt-1 text-sm font-semibold text-primary-highlight">
              Home visits within about {{ radius }} miles
            </p>
          </div>
          <a
            v-if="blok?.show_directions !== false && directionsUrl"
            :href="directionsUrl"
            target="_blank"
            rel="noopener"
            class="rounded-sm bg-primary-dark px-4 py-2 text-sm font-semibold text-white hover:bg-highlight-2"
          >
            Get directions
          </a>
        </div>
        <div ref="mapEl" class="h-72 w-full sm:h-96"></div>
        <p class="border-t border-primary-dark/10 px-5 py-2 text-xs text-primary-dark/55">
          Map behaviour is frontend work (tiles, pin, radius). Storyblok stores the coordinates and radius.
        </p>
      </div>
    </div>
  </section>
</template>
