/**
 * Turns a Storyblok multilink value into a href.
 *
 * Handles story, url, email and asset links, plus an optional anchor. Returns an
 * empty string for an empty link so callers can hide the button/link entirely
 * (an unset "Booking link" must never render as a dead button).
 */
export default function (link) {
  if (!link || typeof link !== 'object') {
    return '';
  }

  const anchor = link.anchor ? `#${link.anchor}` : '';

  switch (link.linktype) {
    case 'story': {
      const slug = link.story?.full_slug ?? link.cached_url ?? '';
      if (!slug) {
        return '';
      }
      const path = slug === 'home' ? '/' : `/${slug.replace(/^\/+/, '')}`;
      return `${path}${anchor}`;
    }
    case 'email':
      return link.email ? `mailto:${link.email}` : '';
    case 'asset':
      return link.url || link.cached_url || '';
    case 'url':
    default: {
      const url = link.url || link.cached_url || '';
      return url ? `${url}${anchor}` : '';
    }
  }
}
