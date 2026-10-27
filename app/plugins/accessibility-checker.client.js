import { createAccessibilityChecker } from '@storyblok/accessibility-checker';
import { defineNuxtPlugin } from '#app';

// Runs axe-core when the Visual Editor asks for a check and reports to its A11y tab.
// Outside the Visual Editor, enable() does nothing.
export default defineNuxtPlugin(() => {
  createAccessibilityChecker().enable();
});
