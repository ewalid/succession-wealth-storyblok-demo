/**
 * Articles, videos and events as one feed: onward journeys, the topic hub,
 * the events hub and the content library all read from here.
 */
export const CONTENT_TYPES = ['article-page', 'video_page', 'event'];

const KIND = { 'article-page': 'Article', 'video_page': 'Video', 'event': 'Event' };

export function contentKind(story) {
  return KIND[story?.content?.component] || 'Page';
}

export function contentTitle(story) {
  const c = story?.content || {};
  return c.headline || c.title || story?.name || '';
}

export function contentImage(story) {
  const c = story?.content || {};
  return c.image || c.thumbnail || null;
}

export function eventStart(story) {
  const v = story?.content?.start;
  return v ? new Date(v.replace(' ', 'T')) : null;
}

/** An event is past once its end (or start) has gone by. */
export function isPastEvent(story) {
  const c = story?.content || {};
  const v = c.end || c.start;
  return v ? new Date(v.replace(' ', 'T')) < new Date() : false;
}

function newestFirst(a, b) {
  const da = new Date(a.first_published_at || a.published_at || a.created_at || 0);
  const db = new Date(b.first_published_at || b.published_at || b.created_at || 0);
  return db - da;
}

/**
 * Latest content filtered by topic and/or planner. Each type is queried on
 * its own because the planner lives in a different field per type.
 */
export async function fetchContentFeed(api, { version, topic, author, types, limit = 3, exclude = [] } = {}) {
  const wanted = types?.length ? types : CONTENT_TYPES;
  const plannerField = { 'article-page': 'author', 'video_page': 'featured_planners', 'event': 'hosts' };
  const results = await Promise.all(wanted.map(async (component) => {
    const filter = {};
    if (topic) {
      filter.specialisms = { any_in_array: topic };
    }
    if (author) {
      filter[plannerField[component]] = component === 'article-page' ? { in: author } : { any_in_array: author };
    }
    if (component === 'event') {
      filter.hide_from_hub = { not_in: 'true' };
    }
    try {
      const { data } = await api.get('cdn/stories', { version, content_type: component, per_page: 12, filter_query: filter });
      return data.stories ?? [];
    }
    catch {
      return [];
    }
  }));
  return results.flat()
    .filter(s => !exclude.includes(s.uuid))
    .filter(s => contentKind(s) !== 'Event' || !isPastEvent(s))
    .sort(newestFirst)
    .slice(0, Number(limit) || 3);
}

export async function fetchStoriesByUuids(api, uuids, { version } = {}) {
  const list = (uuids || []).filter(Boolean);
  if (!list.length) {
    return [];
  }
  try {
    const { data } = await api.get('cdn/stories', { version, by_uuids_ordered: list.join(','), per_page: 25 });
    return data.stories ?? [];
  }
  catch {
    return [];
  }
}
