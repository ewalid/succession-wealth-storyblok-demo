<script setup>
defineProps({
  logo: Object,
  // Campaign pages can hide the menu so visitors stay on the page (UC1).
  minimal: { type: Boolean, default: false },
});

const route = useRoute();
const inEditor = computed(() => route.query._storyblok !== undefined);
const openMenu = ref(null);
const mobileOpen = ref(false);
const searchQuery = ref('');

const utilityLinks = [
  { label: 'My Succession Wealth', href: 'https://succession.myfinance-hub.co.uk/clients/home/', external: true },
  { label: 'Platform Login', href: 'https://www.platformservices.co.uk/Sites/1/succession/Users/Account/LogOn', external: true },
  { label: 'Contact us', href: '/contact' },
];

const menus = [
  {
    label: 'About you',
    items: [
      { label: 'Your financial advice needs', href: '/topics/inheritance-tax-planning' },
      { label: 'Find a planner', href: '/planners' },
      { label: 'Inheritance tax', href: '/topics/inheritance-tax-planning' },
    ],
  },
  {
    label: 'About us',
    items: [
      { label: 'Our wealth planners', href: '/planners' },
      { label: 'Why choose us', href: '/home' },
      { label: 'Offices', href: '/offices/leeds' },
    ],
  },
  {
    label: 'Work with us',
    items: [
      { label: 'Careers', href: 'https://careers.successionwealth.co.uk/', external: true },
      { label: 'Contact', href: '/contact' },
    ],
  },
  {
    label: 'Specialist Divisions',
    items: [
      { label: 'Succession Sports', href: '/home' },
      { label: 'Campaigns', href: '/campaigns/leeds-retirement-planning' },
    ],
  },
  {
    label: 'Resources',
    items: [
      { label: 'Guides', href: '/form-layouts' },
      { label: 'Insights', href: '/articles' },
      { label: 'Events', href: '/events/retirement-income-evening-leeds' },
    ],
  },
];

function toggleMenu(label) {
  openMenu.value = openMenu.value === label ? null : label;
}

function closeMenus() {
  openMenu.value = null;
}

function onSearch() {
  const q = searchQuery.value.trim();
  navigateTo(q ? `/planners?search=${encodeURIComponent(q)}` : '/planners');
  mobileOpen.value = false;
}

onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!(e.target instanceof Element)) {
      return;
    }
    if (!e.target.closest('[data-sw-menu]')) {
      closeMenus();
    }
  });
});
</script>

<template>
  <header class="sticky top-0 z-[99] border-b border-[#121213]/08 bg-white">
    <div class="mx-auto max-w-[1200px] px-4 lg:px-6">
      <div class="flex items-start justify-between gap-4 py-3 lg:items-end lg:py-4">
        <NuxtLink
          :to="inEditor || minimal ? '' : '/'"
          class="flex shrink-0 flex-col items-center pt-1"
          aria-label="Return to homepage"
        >
          <img
            v-if="logo?.filename"
            :src="logo.filename"
            :alt="logo.alt || 'Succession Wealth'"
            class="h-auto w-[160px] object-contain lg:w-[220px]"
            width="220"
            height="65"
          />
          <span v-else class="font-display text-sm font-semibold tracking-[0.12em] text-[#121213]">
            SUCCESSION WEALTH
          </span>
        </NuxtLink>

        <div v-if="!minimal" class="hidden min-w-0 flex-1 flex-col lg:flex">
          <div class="mb-3 flex items-center justify-end gap-5">
            <a
              v-for="link in utilityLinks"
              :key="link.label"
              :href="link.href"
              :target="link.external ? '_blank' : undefined"
              :rel="link.external ? 'noopener noreferrer' : undefined"
              class="font-[family-name:var(--font-family-display)] text-[15px] text-[#8B6F4B] hover:underline"
            >
              {{ link.label }}
            </a>
            <form class="relative" @submit.prevent="onSearch">
              <input
                v-model="searchQuery"
                type="search"
                name="search"
                placeholder="Search a Planner by name"
                aria-label="Search a Planner by name"
                class="h-9 w-56 rounded-sm border border-[#121213]/20 bg-white px-3 pr-9 text-sm text-[#121213] outline-none placeholder:text-[#121213]/45 focus:border-[#8B6F4B]"
              />
              <button
                type="submit"
                class="absolute right-2 top-1/2 -translate-y-1/2 text-[#8B6F4B]"
                aria-label="Search"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-4">
                  <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                </svg>
              </button>
            </form>
          </div>

          <nav class="flex w-full items-center justify-between gap-2" aria-label="Primary">
            <div
              v-for="menu in menus"
              :key="menu.label"
              data-sw-menu
              class="relative"
            >
              <button
                type="button"
                class="inline-flex items-center gap-1.5 py-2 text-[15px] font-medium text-[#121213] hover:text-[#8B6F4B]"
                :aria-expanded="openMenu === menu.label"
                @click.stop="toggleMenu(menu.label)"
              >
                {{ menu.label }}
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" viewBox="0 0 12 8" class="opacity-70" aria-hidden="true">
                  <path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.5" />
                </svg>
              </button>
              <div
                v-if="openMenu === menu.label"
                class="absolute left-0 top-full z-50 min-w-56 border border-[#121213]/10 bg-white py-2 shadow-lg"
              >
                <a
                  v-for="item in menu.items"
                  :key="item.label"
                  :href="item.href"
                  :target="item.external ? '_blank' : undefined"
                  :rel="item.external ? 'noopener noreferrer' : undefined"
                  class="block px-4 py-2.5 text-sm text-[#121213] hover:bg-[#F3F1ED] hover:text-[#8B6F4B]"
                  @click="closeMenus"
                >
                  {{ item.label }}
                </a>
              </div>
            </div>
          </nav>
        </div>

        <button
          v-if="!minimal"
          type="button"
          class="mt-2 inline-flex flex-col gap-1.5 p-2 lg:hidden"
          aria-label="Open menu"
          @click="mobileOpen = !mobileOpen"
        >
          <span class="block h-0.5 w-6 bg-[#121213]"></span>
          <span class="block h-0.5 w-6 bg-[#121213]"></span>
          <span class="block h-0.5 w-6 bg-[#121213]"></span>
        </button>
      </div>
    </div>

    <div v-if="mobileOpen && !minimal" class="border-t border-[#121213]/10 bg-white lg:hidden">
      <div class="space-y-4 px-4 py-5">
        <form class="flex gap-2" @submit.prevent="onSearch">
          <input
            v-model="searchQuery"
            type="search"
            placeholder="Search a Planner by name"
            class="h-10 flex-1 rounded-sm border border-[#121213]/20 px-3 text-sm"
          />
          <button type="submit" class="rounded-sm bg-[#8B6F4B] px-4 text-sm font-semibold text-white">
            Search
          </button>
        </form>
        <div v-for="menu in menus" :key="menu.label">
          <p class="mb-1 text-xs font-semibold uppercase tracking-wide text-[#8B6F4B]">
            {{ menu.label }}
          </p>
          <a
            v-for="item in menu.items"
            :key="item.label"
            :href="item.href"
            class="block py-2 text-sm text-[#121213]"
            @click="mobileOpen = false"
          >
            {{ item.label }}
          </a>
        </div>
        <a
          v-for="link in utilityLinks"
          :key="link.label"
          :href="link.href"
          class="block py-2 text-sm text-[#8B6F4B]"
        >
          {{ link.label }}
        </a>
      </div>
    </div>
  </header>
</template>
