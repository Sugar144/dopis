<template>
  <RouterView v-slot="{ Component }">
    <transition name="route" mode="out-in">
      <component :is="Component" />
    </transition>
  </RouterView>
</template>

<style>
/*
  Global design tokens. Kept in App.vue so they're loaded once and
  available to every view without a separate global stylesheet file.
*/
:root {
  --font-serif: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;

  /* Warm dark palette — trattoria-at-night */
  --ink-100: #f4ebd9;
  --ink-200: #e2d2ae;
  --ink-300: #c9a25a;
  --ink-400: #a57c37;
  --ink-500: #6b4818;

  --bg-900: #0a0705;
  --bg-800: #130d09;
  --bg-700: #1c140f;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  padding: 0;
  background: var(--bg-900);
  color: var(--ink-100);
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100vh;
  overflow-x: hidden;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
}

.route-enter-active,
.route-leave-active {
  transition: opacity 380ms ease;
}
.route-enter-from,
.route-leave-to {
  opacity: 0;
}

/* Respect users who prefer reduced motion — we still allow the reveal,
   but strip any lingering idle animations. */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 200ms !important;
  }
}
</style>
