/**
 * Intro/body fields moved from plain textarea to rich text. These helpers accept
 * both shapes, so content saved before the migration still renders.
 */
export function hasRichText(value) {
  if (!value) {
    return false;
  }
  if (typeof value === 'string') {
    return value.trim().length > 0;
  }
  const walk = node => (node?.text?.trim() ? true : (node?.content || []).some(walk));
  return walk(value);
}
