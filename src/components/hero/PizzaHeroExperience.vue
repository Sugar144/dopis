<template>
  <section class="hero">
    <!-- Atmospheric backdrop: vignette + accent glow + film grain.
         All purely decorative, pointer-events-none. -->
    <div class="hero__backdrop" aria-hidden="true">
      <div class="backdrop__vignette"></div>
      <div class="backdrop__glow" :style="glowStyle"></div>
      <div class="backdrop__grain"></div>
    </div>

    <!-- Intro copy. Present only until the box starts opening. -->
    <transition name="intro">
      <div
        v-if="stage === 'closed' || stage === 'growing'"
        class="hero__intro"
      >
        <p class="eyebrow">Edición limitada · Napoli 1987</p>
        <h1 class="headline">
          La pizza que
          <br />
          <em>merece ser abierta.</em>
        </h1>
        <p class="subhead">
          Cada caja que abres es una receta que nuestros maestros pizzeros
          han cuidado durante cuatro generaciones.
        </p>
      </div>
    </transition>

    <!-- Stage: the 3D box lives inside the scene-frame. GSAP tweens the
         frame's scale/yOffset for a cinematic push-in / pull-back move. -->
    <div class="hero__scene" :class="[`hero__scene--${stage}`]">
      <div class="scene-frame" :style="sceneFrameStyle">
        <PizzaBox3D
          :stage="boxStage"
          :accent="activePizza.accent"
          @box-click="openBox"
        />
      </div>
    </div>

    <!-- Carousel reveals after the box has finished opening. -->
    <transition name="carousel">
      <div v-if="stage === 'open'" class="hero__carousel">
        <PizzaCarousel
          :pizzas="pizzas"
          :initial-index="0"
          @active-change="onActiveChange"
          @order="onOrder"
          @details="onDetails"
        />
      </div>
    </transition>

    <!-- Reset lets users re-experience the reveal. Visible once opened. -->
    <transition name="fade">
      <button
        v-if="stage === 'open'"
        class="hero__reset"
        type="button"
        @click="resetBox"
      >
        ← cerrar la caja
      </button>
    </transition>
  </section>
</template>

<script setup>
import { computed, reactive, ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import PizzaBox3D from './PizzaBox3D.vue'
import PizzaCarousel from './PizzaCarousel.vue'
import { pizzas } from '@/data/pizzas.js'

const router = useRouter()

/*
  State machine — a single `stage` ref drives every template branch,
  every CSS selector on the 3D box, and every phase of the GSAP timeline.

     closed → growing → opening → open
                                  ↑
                                  └── reset → closed

  The CSS transitions on the 3D box happen automatically via
  `.pizza3d--opening` / `.pizza3d--open`; GSAP only animates the
  scene-frame (scale + yOffset), so CSS and JS never fight each other.
*/
const stage = ref('closed')
const activeIndex = ref(0)

const sceneAnim = reactive({
  scale: 1,
  yOffset: 0,
})

const boxStage = computed(() => {
  if (stage.value === 'closed' || stage.value === 'growing') return 'closed'
  if (stage.value === 'opening') return 'opening'
  return 'open'
})

const activePizza = computed(() => pizzas[activeIndex.value] ?? pizzas[0])

const sceneFrameStyle = computed(() => ({
  transform: `translate3d(0, ${sceneAnim.yOffset}px, 0) scale(${sceneAnim.scale})`,
}))

const glowStyle = computed(() => ({
  '--glow-accent': activePizza.value.accent,
  '--glow-intensity': stage.value === 'closed' ? '0.35' : '0.65',
}))

let timeline = null

function openBox() {
  if (stage.value !== 'closed') return

  stage.value = 'growing'

  // Kill any previous tween to avoid overlap when spam-clicking.
  if (timeline) timeline.kill()

  timeline = gsap.timeline()

  // Phase 1 — grow: the box scales up and lifts, intro fades out.
  timeline.to(sceneAnim, {
    scale: 1.2,
    yOffset: -30,
    duration: 0.85,
    ease: 'power3.out',
  })

  // Phase 2 — open: hand over to CSS for the lid rotation (smooth,
  // compositor-friendly) by flipping the stage.
  timeline.call(() => {
    stage.value = 'opening'
  })

  // Phase 3 — settle: slight pull-back so the carousel has room below.
  timeline.to(
    sceneAnim,
    {
      scale: 0.88,
      yOffset: -140,
      duration: 0.95,
      ease: 'power2.inOut',
    },
    '+=0.05',
  )

  // Phase 4 — open is fully committed: reveal carousel + CTAs.
  timeline.call(() => {
    stage.value = 'open'
  })
}

function resetBox() {
  if (timeline) timeline.kill()
  stage.value = 'closed'
  activeIndex.value = 0
  gsap.to(sceneAnim, {
    scale: 1,
    yOffset: 0,
    duration: 0.7,
    ease: 'power2.out',
  })
}

function onActiveChange(index) {
  activeIndex.value = index
}

function onOrder(pizza) {
  // Placeholder — swap for your real checkout/route once it exists.
  router.push({
    name: 'pizza-detail',
    params: { slug: pizza.slug },
    query: { action: 'order' },
  })
}

function onDetails(pizza) {
  router.push({ name: 'pizza-detail', params: { slug: pizza.slug } })
}

onBeforeUnmount(() => {
  if (timeline) timeline.kill()
})
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 120px 24px 60px;
  overflow: hidden;
  isolation: isolate;
}

/* ---- Backdrop ---- */
.hero__backdrop {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.backdrop__vignette {
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 80% 62% at 50% 42%,
    rgba(70, 40, 22, 0.55) 0%,
    rgba(15, 10, 8, 0.12) 50%,
    rgba(0, 0, 0, 0.85) 100%
  );
}
.backdrop__glow {
  position: absolute;
  left: 50%;
  top: 55%;
  width: 82vmin;
  height: 82vmin;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle at center,
    color-mix(in oklab, var(--glow-accent, #c94d3a) 55%, transparent) 0%,
    transparent 62%
  );
  filter: blur(70px);
  opacity: var(--glow-intensity, 0.45);
  transition: opacity 900ms ease, background 900ms ease;
  mix-blend-mode: screen;
}
/* Film grain — tiny inline SVG noise, stays crisp at any zoom */
.backdrop__grain {
  position: absolute;
  inset: -50%;
  opacity: 0.07;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  mix-blend-mode: overlay;
  animation: grain-drift 8s steps(6) infinite;
}
@keyframes grain-drift {
  0%   { transform: translate(0, 0); }
  20%  { transform: translate(-2%, 3%); }
  40%  { transform: translate(3%, -1%); }
  60%  { transform: translate(-1%, -3%); }
  80%  { transform: translate(2%, 2%); }
  100% { transform: translate(0, 0); }
}

/* ---- Intro copy ---- */
.hero__intro {
  position: absolute;
  top: 110px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  max-width: 640px;
  color: var(--ink-100);
  z-index: 5;
  padding: 0 20px;
}
.eyebrow {
  font-size: 10px;
  letter-spacing: 0.42em;
  text-transform: uppercase;
  color: var(--ink-300);
  margin: 0 0 18px;
  font-weight: 500;
}
.headline {
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: clamp(42px, 6vw, 72px);
  line-height: 1.02;
  margin: 0;
  letter-spacing: 0.005em;
}
.headline em {
  font-style: italic;
  color: var(--ink-300);
}
.subhead {
  margin: 24px auto 0;
  max-width: 420px;
  font-size: 14px;
  line-height: 1.65;
  color: rgba(244, 235, 217, 0.65);
}

.intro-enter-active,
.intro-leave-active {
  transition: opacity 500ms ease, transform 500ms ease;
}
.intro-enter-from { opacity: 0; transform: translate(-50%, 16px); }
.intro-leave-to   { opacity: 0; transform: translate(-50%, -16px); }

/* ---- Scene ---- */
.hero__scene {
  position: relative;
  z-index: 2;
  perspective: 1800px;
  perspective-origin: 50% 45%;
}
.scene-frame {
  transform-origin: center center;
  will-change: transform;
}

/* ---- Carousel ---- */
.hero__carousel {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 12px;
  z-index: 3;
  padding: 0 24px;
}
.carousel-enter-active,
.carousel-leave-active {
  transition: opacity 500ms ease, transform 500ms ease;
}
.carousel-enter-from { opacity: 0; transform: translateY(30px); }
.carousel-leave-to   { opacity: 0; transform: translateY(30px); }

.fade-enter-active,
.fade-leave-active { transition: opacity 400ms ease; }
.fade-enter-from,
.fade-leave-to     { opacity: 0; }

/* ---- Reset button ---- */
.hero__reset {
  position: absolute;
  top: 90px;
  right: 28px;
  background: transparent;
  border: 1px solid rgba(244, 235, 217, 0.25);
  color: rgba(244, 235, 217, 0.75);
  font-size: 11px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  padding: 10px 18px;
  border-radius: 999px;
  cursor: pointer;
  z-index: 20;
  transition: all 220ms ease;
}
.hero__reset:hover {
  border-color: var(--ink-300);
  color: var(--ink-300);
}

@media (max-width: 768px) {
  .hero__intro { top: 84px; }
  .hero__reset { top: 72px; right: 16px; padding: 8px 14px; font-size: 10px; }
  .hero { padding: 96px 16px 40px; }
}
</style>
