/**
 * Fetch published Redirect stories from Storyblok and apply 301/302 navigations.
 * Marketing users manage entries under redirects/ in the CMS — no deploy needed.
 */
export default defineNuxtRouteMiddleware(async (to) => {
  // Skip Visual Editor / API paths
  if (to.path.startsWith('/api') || to.query._storyblok !== undefined) {
    return;
  }

  const config = useRuntimeConfig();
  const token = config.public.templateToken;
  if (!token) {
    return;
  }

  try {
    const version = getVersion();
    const result = await $fetch('https://api.storyblok.com/v2/cdn/stories', {
      query: {
        token,
        version,
        starts_with: 'redirects/',
        per_page: 100,
      },
    });

    const stories = result?.stories || result?.data?.stories || [];
    const path = to.path.replace(/\/$/, '') || '/';

    for (const story of stories) {
      const c = story.content || {};
      if (c.component !== 'Redirect') {
        continue;
      }

      const fromUrl = normalizePath(
        c.oldURL?.cached_url || c.oldURL?.url || '',
      );

      if (!fromUrl) {
        continue;
      }

      const matchesFrom = path === fromUrl || path === `/${fromUrl}` || to.path === fromUrl;
      if (!matchesFrom) {
        continue;
      }

      const status = Number(c.Type) === 302 ? 302 : 301;
      let target
        = c.newURL?.cached_url
          || c.newURL?.url
          || '';

      // Prefer internal story target when set (UUID)
      if (c.ToInternalStory) {
        try {
          const { data: targetData } = await $fetch(
            `https://api.storyblok.com/v2/cdn/stories/${c.ToInternalStory}`,
            { query: { token, version, find_by: 'uuid' } },
          );
          if (targetData?.story?.full_slug) {
            target = `/${targetData.story.full_slug}`.replace(/\/$/, '');
          }
        }
        catch {
          /* keep URL target */
        }
      }

      if (!target) {
        continue;
      }

      // Absolute external URL
      if (/^https?:\/\//i.test(target)) {
        if (import.meta.server) {
          return navigateTo(target, { external: true, redirectCode: status });
        }
        window.location.href = target;
        return;
      }

      const dest = target.startsWith('/') ? target : `/${target}`;
      return navigateTo(dest, { redirectCode: status });
    }
  }
  catch (e) {
    console.warn('[redirects] skipped', e);
  }
});

function normalizePath(raw) {
  if (!raw) {
    return '';
  }
  try {
    if (/^https?:\/\//i.test(raw)) {
      return new URL(raw).pathname.replace(/\/$/, '') || '/';
    }
  }
  catch {
    /* ignore */
  }
  return raw.replace(/\/$/, '') || '/';
}
