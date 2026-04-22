<template>
  <main class="home">
    <!-- Brand bar stays pinned over the hero — it's not part of the cinematic
         stage, but anchors the page in the product/brand world. -->
    <header class="home__header">
      <RouterLink to="/" class="brand" aria-label="Dopis Pizzeria">
        <!-- TODO: sustituir por logo real (SVG preferible, conserva currentColor) -->
        <svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">
          <circle cx="20" cy="20" r="18" fill="none" stroke="currentColor" stroke-width="1.4" />
          <path d="M12 25 L20 10 L28 25 Z" fill="currentColor" />
          <circle cx="20" cy="22" r="1.8" fill="var(--bg-900)" />
        </svg>
        <span class="brand__name">Dopis<em>·</em>Pizzeria</span>
      </RouterLink>

      <nav class="home__nav">
        <a href="#menu">Carta</a>
        <a href="#about">Historia</a>
        <a href="#contact">Reservar</a>
      </nav>
    </header>

    <PizzaHeroExperience />

    <!-- Continuation placeholder so the hero reads as the opening act
         rather than the whole page. -->
    <section class="home__continuation">
      <p class="home__continuation-eyebrow">Sigue descubriendo</p>
      <p class="home__continuation-text">
        Aquí conectaríamos el resto de la home (carta completa, historia, ubicación…).
      </p>
    </section>
  </main>
</template>

<script setup>
import PizzaHeroExperience from '@/components/hero/PizzaHeroExperience.vue'
</script>

<style scoped>
.home {
  min-height: 100vh;
  background:
    radial-gradient(ellipse 90% 70% at 50% 0%, #1d1209 0%, #0a0705 55%, #050302 100%);
  position: relative;
  overflow-x: hidden;
}

.home__header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 22px 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 50;
  pointer-events: none;
}
.home__header > * {
  pointer-events: auto;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: var(--ink-300);
  font-family: var(--font-serif);
  font-size: 22px;
  letter-spacing: 0.06em;
}
.brand__mark {
  width: 32px;
  height: 32px;
}
.brand__name em {
  font-style: normal;
  opacity: 0.55;
  margin: 0 4px;
}

.home__nav {
  display: flex;
  gap: 28px;
  font-size: 11px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: rgba(244, 235, 217, 0.72);
}
.home__nav a {
  transition: color 220ms ease;
}
.home__nav a:hover {
  color: var(--ink-300);
}

.home__continuation {
  padding: 96px 36px 120px;
  text-align: center;
  color: rgba(244, 235, 217, 0.45);
}
.home__continuation-eyebrow {
  font-size: 10px;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  color: var(--ink-400);
  margin: 0 0 12px;
}
.home__continuation-text {
  font-size: 14px;
  margin: 0;
}

@media (max-width: 640px) {
  .home__header {
    padding: 16px 20px;
  }
  .home__nav {
    display: none;
  }
}
</style>
