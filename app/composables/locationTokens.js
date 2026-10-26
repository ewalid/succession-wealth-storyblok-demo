/**
 * {city}, {phone} and {address} tokens for location landing pages. The page
 * provides the values from its Office; blocks call useLocationTokens() and pass
 * any text or rich-text doc through it. Outside a location page tokens are left as typed.
 */
const KEY = Symbol('location-tokens');

export function provideLocationTokens(values) {
  provide(KEY, values);
}

export function replaceLocationTokens(value, map) {
  return replaceIn(value, map || {});
}

function replaceIn(value, map) {
  if (typeof value === 'string') {
    return value.replace(/\{(city|phone|address)\}/g, (m, k) => map[k] || m);
  }
  if (Array.isArray(value)) {
    return value.map(v => replaceIn(v, map));
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, k === 'text' || typeof v === 'object' ? replaceIn(v, map) : v]));
  }
  return value;
}

/** The raw values the page provided (also carries officeUuid for maps), or null. */
export function useLocationContext() {
  return inject(KEY, null);
}

export function useLocationTokens() {
  const values = inject(KEY, null);
  return value => (values ? replaceIn(value, values.value || {}) : value);
}
