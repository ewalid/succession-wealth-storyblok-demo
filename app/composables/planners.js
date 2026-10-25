/**
 * Shared data + scoring helpers for the Succession Wealth planner feature
 * (planner cards, grids, the finder, office hubs and the /planners listing).
 *
 * Everything here is client-side: the app runs with `ssr: false`, so module
 * state cannot leak between visitors. Caches are keyed by version so a draft
 * (Visual Editor) session never reuses published data.
 */
import { computed, reactive } from 'vue';

/**
 * Every relation the planner feature reads. Kept in one place so the catch-all
 * route, the Visual Editor bridge and the helpers below cannot drift apart.
 * `article-page.author` is the real component name for "article.author".
 */
export const PLANNER_RESOLVE_RELATIONS = [
  'planner.office',
  'planner_card.planner',
  'planner_grid.planners',
  'planner_grid.office',
  'office_map.office',
  'office_map.planner',
  'office.pinned_planners',
  'campaign-page.office',
  'article-page.author',
  'event.hosts',
  'video_page.featured_planners',
];

const store = reactive({ datasources: {}, offices: null, planners: null });
const inflight = new Map();

function once(key, fn) {
  if (!inflight.has(key)) {
    inflight.set(
      key,
      fn().catch((error) => {
        inflight.delete(key);
        throw error;
      }),
    );
  }
  return inflight.get(key);
}

/* ---------------------------------------------------------------- helpers */

export function prettifySlug(value) {
  if (!value) {
    return '';
  }
  const text = String(value).replace(/[-_]+/g, ' ').trim();
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/** A relation value is "resolved" when Storyblok swapped the uuid for a story. */
export function isResolvedStory(value) {
  return !!value && typeof value === 'object' && !!value.content;
}

export function plannerFullName(content) {
  return [content?.first_name, content?.last_name].filter(Boolean).join(' ').trim();
}

export function storyPath(story) {
  const slug = story?.full_slug;
  return slug ? `/${slug}` : '';
}

/** Accepts "25", 25, "", null. Returns a finite number or null. */
export function toNumber(value) {
  if (value === '' || value === null || value === undefined) {
    return null;
  }
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

export function haversineMiles(lat1, lng1, lat2, lng2) {
  const toRad = degrees => (degrees * Math.PI) / 180;
  const earthRadiusMiles = 3958.8;
  const dLat = toRad(lat2 - lat1);
  const dLng = toRad(lng2 - lng1);
  const a
    = Math.sin(dLat / 2) ** 2
      + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
  return 2 * earthRadiusMiles * Math.asin(Math.min(1, Math.sqrt(a)));
}

export function formatMiles(distance) {
  const rounded = distance < 10 ? Math.round(distance * 10) / 10 : Math.round(distance);
  const label = Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
  return `${label} ${rounded === 1 ? 'mile' : 'miles'}`;
}

/** A-Z by last name, then first name. */
export function compareByName(a, b) {
  const left = `${a.content?.last_name ?? ''} ${a.content?.first_name ?? ''}`.toLowerCase();
  const right = `${b.content?.last_name ?? ''} ${b.content?.first_name ?? ''}`.toLowerCase();
  return left.localeCompare(right, 'en-GB');
}

/** `active=false` hides a planner everywhere, even while the entry is published. */
export function isActivePlanner(story) {
  return !!story?.content && story.content.active !== false;
}

/**
 * Pinned planners first (in the order the editor pinned them), then everyone
 * else A-Z. Pinned uuids that are not in the list (inactive, unpublished or in
 * another office) are skipped rather than shown.
 */
export function sortPlanners(list, { sort = 'pinned_then_az', pinned = [] } = {}) {
  const sorted = [...list].sort(compareByName);
  if (sort !== 'pinned_then_az' || !pinned.length) {
    return sorted;
  }
  const pinnedUuids = pinned.map(item => (typeof item === 'string' ? item : item?.uuid)).filter(Boolean);
  const first = pinnedUuids
    .map(uuid => sorted.find(story => story.uuid === uuid))
    .filter(Boolean);
  const rest = sorted.filter(story => !pinnedUuids.includes(story.uuid));
  return [...first, ...rest];
}

/* ------------------------------------------------------------ datasources */

export function loadDatasource(api, name) {
  return once(`ds:${name}`, async () => {
    const { data } = await api.get('cdn/datasource_entries', {
      datasource: name,
      per_page: 1000,
    });
    store.datasources[name] = (data.datasource_entries ?? []).map(entry => ({
      name: entry.name,
      value: entry.value,
    }));
  });
}

/** Reactive list of `{ name, value }` for a datasource. Triggers the load once. */
export function useDatasource(name) {
  const api = useStoryblokApi();
  loadDatasource(api, name).catch(() => {});
  return computed(() => store.datasources[name] ?? []);
}

/** Reactive `{ value: name }` map, for turning slugs into labels. */
export function useDatasourceLabels(name) {
  const entries = useDatasource(name);
  return computed(() => Object.fromEntries(entries.value.map(entry => [entry.value, entry.name])));
}

export function labelFor(labels, value) {
  return labels?.[value] ?? prettifySlug(value);
}

/* ---------------------------------------------------------------- offices */

export function loadOffices(api, version) {
  return once(`offices:${version}`, async () => {
    const { data } = await api.get('cdn/stories', {
      version,
      content_type: 'office',
      starts_with: 'offices/',
      per_page: 100,
      sort_by: 'content.name:asc',
    });
    store.offices = data.stories ?? [];
  });
}

/** Reactive list of every office story, loaded once. */
export function useOffices() {
  const api = useStoryblokApi();
  const version = getVersion();
  loadOffices(api, version).catch(() => {});
  return computed(() => store.offices ?? []);
}

/**
 * The office story for a planner. Uses the resolved relation when Storyblok
 * provided it, otherwise looks the uuid up in the loaded office list.
 */
export function officeFor(planner) {
  const office = planner?.content?.office;
  if (isResolvedStory(office)) {
    return office;
  }
  if (typeof office === 'string' && office) {
    return (store.offices ?? []).find(story => story.uuid === office) ?? null;
  }
  return null;
}

export function officeCoordinates(office) {
  const lat = toNumber(office?.content?.lat);
  const lng = toNumber(office?.content?.lng);
  return lat === null || lng === null ? null : { lat, lng };
}

/* ---------------------------------------------------------------- stories */

/**
 * Returns a story for a relation value: the resolved story when we already have
 * one, otherwise a fetch by uuid. Returns null when it cannot be found, which
 * is what an unpublished story looks like on the live site.
 */
export async function resolveStory(api, value, { version, resolve_relations } = {}) {
  if (!value) {
    return null;
  }
  if (isResolvedStory(value)) {
    return value;
  }
  if (typeof value !== 'string') {
    return null;
  }
  try {
    const { data } = await api.get(`cdn/stories/${value}`, {
      version,
      find_by: 'uuid',
      resolve_relations,
    });
    return data.story ?? null;
  }
  catch {
    return null;
  }
}

/**
 * Active planners, optionally narrowed by office or specialism. The Content
 * Delivery API only returns published stories on the live site, so an
 * unpublished planner disappears with no extra work; `active` handles the
 * "leaves but stays published" case.
 */
export async function fetchPlanners(api, { version, office, specialism } = {}) {
  const filterQuery = { active: { is: 'true' } };
  if (office) {
    filterQuery.office = { in: office };
  }
  if (specialism) {
    filterQuery.specialisms = { any_in_array: specialism };
  }

  const stories = [];
  let page = 1;
  let total = Infinity;
  while (stories.length < total && page <= 10) {
    const response = await api.get('cdn/stories', {
      version,
      content_type: 'planner',
      starts_with: 'planners/',
      per_page: 100,
      page,
      resolve_relations: 'planner.office',
      filter_query: filterQuery,
    });
    stories.push(...(response.data.stories ?? []));
    total = response.total ?? stories.length;
    if (!response.data.stories?.length) {
      break;
    }
    page += 1;
  }

  return stories.filter(isActivePlanner);
}

/** All active planners, cached per version. Used by the finder and /planners. */
export async function loadAllPlanners(api, version) {
  await once(`planners:${version}`, async () => {
    store.planners = await fetchPlanners(api, { version });
  });
  return store.planners ?? [];
}

/** Planners from a list of uuids/resolved stories, preserving the editor's order. */
export async function fetchPlannersByRelation(api, values, { version } = {}) {
  const list = Array.isArray(values) ? values : [];
  const resolved = list.filter(isResolvedStory);
  const missing = list.filter(value => typeof value === 'string' && value);

  let fetched = [];
  if (missing.length) {
    try {
      const { data } = await api.get('cdn/stories', {
        version,
        by_uuids_ordered: missing.join(','),
        resolve_relations: 'planner.office',
        per_page: 100,
      });
      fetched = data.stories ?? [];
    }
    catch {
      fetched = [];
    }
  }

  const byUuid = new Map([...resolved, ...fetched].map(story => [story.uuid, story]));
  return list
    .map(value => byUuid.get(typeof value === 'string' ? value : value?.uuid))
    .filter(isActivePlanner);
}

/**
 * Content a planner is attached to: articles they wrote, events they host and
 * videos they feature. A reverse lookup, so nothing is stored on the planner.
 */
export async function fetchContentByPlanner(api, plannerUuid, { version } = {}) {
  if (!plannerUuid) {
    return [];
  }
  const queries = [
    { content_type: 'article-page', filter_query: { author: { in: plannerUuid } }, kind: 'Article' },
    { content_type: 'event', filter_query: { hosts: { any_in_array: plannerUuid } }, kind: 'Event' },
    { content_type: 'video_page', filter_query: { featured_planners: { any_in_array: plannerUuid } }, kind: 'Video' },
  ];

  const results = await Promise.all(
    queries.map(async ({ kind, ...params }) => {
      try {
        const { data } = await api.get('cdn/stories', { version, per_page: 12, ...params });
        return (data.stories ?? []).map(story => ({ kind, story }));
      }
      catch {
        return [];
      }
    }),
  );
  return results.flat();
}

/* ---------------------------------------------------- session + attribution */

const FINDER_KEY = 'sw_finder';
const ATTRIBUTION_KEY = 'sw_attribution';

function readSession(key) {
  if (!import.meta.client) {
    return null;
  }
  try {
    return JSON.parse(window.sessionStorage.getItem(key) || 'null');
  }
  catch {
    return null;
  }
}

function writeSession(key, value) {
  if (!import.meta.client) {
    return;
  }
  try {
    if (value === null) {
      window.sessionStorage.removeItem(key);
    }
    else {
      window.sessionStorage.setItem(key, JSON.stringify(value));
    }
  }
  catch {
    // Private mode or storage full: the finder still works, it just will not remember.
  }
}

/** `{ postcode, preference, topics }` the visitor gave the finder this session. */
export function readFinderAnswers() {
  const stored = readSession(FINDER_KEY);
  return {
    postcode: stored?.postcode ?? '',
    preference: stored?.preference ?? '',
    topics: Array.isArray(stored?.topics) ? stored.topics : [],
  };
}

export function saveFinderAnswers(answers) {
  writeSession(FINDER_KEY, {
    postcode: answers.postcode ?? '',
    preference: answers.preference ?? '',
    topics: answers.topics ?? [],
  });
}

export function clearFinderAnswers() {
  writeSession(FINDER_KEY, null);
}

/**
 * UTM parameters are only on the landing URL, so keep the first set we see for
 * the rest of the session. They travel with the lead form for attribution.
 */
export function captureAttribution() {
  if (!import.meta.client) {
    return {};
  }
  const stored = readSession(ATTRIBUTION_KEY) ?? {};
  const params = new URLSearchParams(window.location.search);
  let changed = false;
  for (const key of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']) {
    const value = params.get(key);
    if (value && !stored[key]) {
      stored[key] = value;
      changed = true;
    }
  }
  if (changed) {
    writeSession(ATTRIBUTION_KEY, stored);
  }
  return stored;
}

/* ------------------------------------------------------------ finder logic */

export const MEETING_LABELS = {
  home: 'Home visit',
  office: 'In the office',
  digital: 'Video or phone',
};

/** Normalises "ls14ap", "LS1  4AP" to "LS1 4AP" for display and API calls. */
export function normalisePostcode(value) {
  const compact = String(value ?? '').replace(/\s+/g, '').toUpperCase();
  if (compact.length < 5) {
    return compact;
  }
  return `${compact.slice(0, -3)} ${compact.slice(-3)}`;
}

/** https://postcodes.io, free and keyless. Returns `{ lat, lng }` or throws. */
export async function geocodePostcode(postcode) {
  const response = await fetch(`https://api.postcodes.io/postcodes/${encodeURIComponent(normalisePostcode(postcode))}`);
  if (response.status === 404) {
    const error = new Error('not-found');
    error.code = 'not-found';
    throw error;
  }
  if (!response.ok) {
    const error = new Error('unavailable');
    error.code = 'unavailable';
    throw error;
  }
  const { result } = await response.json();
  return { lat: result.latitude, lng: result.longitude };
}

/**
 * Scores planners for the finder.
 *
 *  - home:    only planners who visit homes and whose radius covers the
 *             postcode; nearest first.
 *  - office:  planners who meet in the office; nearest office first.
 *  - digital: planners who meet remotely; distance is ignored.
 *  - none:    everyone, nearest first when we know where the visitor is.
 *
 * Topic matches always rank first (more matching topics wins), then distance.
 * When topics are chosen but nothing matches, `fallback` is true and the list
 * is the same search without the topic filter so the visitor is never stranded.
 */
export function scorePlanners(planners, { origin, preference, topics }) {
  const rows = planners.map((planner) => {
    const content = planner.content ?? {};
    const office = officeFor(planner);
    const coordinates = officeCoordinates(office);
    const distance = origin && coordinates
      ? haversineMiles(origin.lat, origin.lng, coordinates.lat, coordinates.lng)
      : null;
    const offers = content.meeting_preferences ?? [];
    const matches = (content.specialisms ?? []).filter(topic => topics.includes(topic)).length;
    return { planner, distance, offers, matches, radius: toNumber(content.home_visit_radius_miles) };
  });

  const eligible = rows.filter((row) => {
    if (preference === 'home') {
      return row.offers.includes('home') && row.distance !== null && row.radius !== null && row.distance <= row.radius;
    }
    if (preference === 'office') {
      return row.offers.includes('office') && row.distance !== null;
    }
    if (preference === 'digital') {
      return row.offers.includes('digital');
    }
    return true;
  });

  const rank = (list) => {
    return [...list].sort((a, b) => {
      if (b.matches !== a.matches) {
        return b.matches - a.matches;
      }
      if (preference !== 'digital' && a.distance !== null && b.distance !== null && a.distance !== b.distance) {
        return a.distance - b.distance;
      }
      return compareByName(a.planner, b.planner);
    });
  };

  const matched = topics.length ? eligible.filter(row => row.matches > 0) : eligible;
  if (topics.length && !matched.length && eligible.length) {
    return { results: rank(eligible), fallback: true };
  }
  return { results: rank(matched), fallback: false };
}
