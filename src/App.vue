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

  /* Brand — corporate red / white / black */
  --brand-red: #d7172a;
  --brand-red-deep: #9c0d1c;
  --brand-red-ink: #6a0813;
  --brand-white: #f5f3ee;
  --brand-black: #0d0b0a;

  /* UI ink tokens — 100 is off-white, 300 is the brand red used as accent */
  --ink-100: #f5f3ee;
  --ink-200: #d9d4c8;
  --ink-300: var(--brand-red);
  --ink-400: #a0a0a0;

  /* Dark room palette (the hero stage is lit from above, very dim edges) */
  --bg-900: #0a0707;
  --bg-800: #120d0d;
  --bg-700: #1b1212;
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
