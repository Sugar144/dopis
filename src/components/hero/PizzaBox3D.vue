<template>
  <!--
    Pseudo-3D pizza box built entirely with CSS 3D transforms.
    Why not Three.js: the geometry is trivial, WebGL costs kBs for no gain.

    Cardboard realism comes from four stacked layers:
      1. Per-face lighting — each face gets a slightly different tint so
         the box reads as lit from above-right (key light), not painted.
      2. Fiber texture — SVG noise overlay (very low opacity) on every face.
      3. End-grain strips — a corrugated band on the inside-top edge of
         every base wall (visible when the lid is open). This is the
         signature "cardboard" tell.
      4. Edge shadows — inset box-shadows make corners read as folds.

    Coord system used (CSS convention — Y points DOWN):
      origin = geometric centre of the closed box
      +X right, +Y down, +Z toward viewer
      base walls span y ∈ [0, +H]; lid walls span y ∈ [-H, 0]
  -->
  <div class="pizza3d" :class="[`pizza3d--${stage}`]" @click="onClick">
    <!-- Soft cast shadow so the box reads as floating, not pasted -->
    <div class="pizza3d__shadow" aria-hidden="true"></div>

    <!-- Warm light "spilling out" as the lid opens -->
    <div class="pizza3d__inner-glow" aria-hidden="true"></div>

    <div class="pizza3d__box">
      <!-- BASE (lower half) -->
      <div class="pizza3d__base">
        <div class="face face--floor"></div>
        <div class="face face--base-front">
          <span class="rim" aria-hidden="true"></span>
        </div>
        <div class="face face--base-back">
          <span class="rim" aria-hidden="true"></span>
        </div>
        <div class="face face--base-left">
          <span class="rim" aria-hidden="true"></span>
        </div>
        <div class="face face--base-right">
          <span class="rim" aria-hidden="true"></span>
        </div>
      </div>

      <!-- LID (upper half, hinged at the back-top edge of the base) -->
      <div class="pizza3d__lid">
        <div class="face face--top">
          <!-- Printed paper label. Replace the <svg> by the real logo
               (black SVG). Keeps the red bar and wordmark structure. -->
          <div class="sticker">
            <svg class="sticker__mark" viewBox="0 0 40 40" aria-hidden="true">
              <!-- TODO: sustituir por logo real en negro -->
              <circle cx="20" cy="20" r="18" fill="none" stroke="currentColor" stroke-width="1.5" />
              <path d="M12 25 L20 9 L28 25 Z" fill="currentColor" />
              <circle cx="20" cy="22" r="2" fill="#fff" />
            </svg>
            <span class="sticker__brand">DOPIS</span>
            <span class="sticker__rule" aria-hidden="true"></span>
            <span class="sticker__sub">Pizzeria · Les Planes · 2025</span>
          </div>
        </div>
        <div class="face face--lid-front">
          <span class="rim rim--lid" aria-hidden="true"></span>
        </div>
        <div class="face face--lid-back">
          <span class="rim rim--lid" aria-hidden="true"></span>
        </div>
        <div class="face face--lid-left">
          <span class="rim rim--lid" aria-hidden="true"></span>
        </div>
        <div class="face face--lid-right">
          <span class="rim rim--lid" aria-hidden="true"></span>
        </div>

        <!-- Inside face of the lid — plain lighter kraft visible once open -->
        <div class="face face--lid-inside"></div>
      </div>

      <!-- Pizza sitting on the base floor. Hidden when parent's carousel
           has taken over, so we don't double up the same visual. -->
      <div class="pizza3d__pizza" :class="{ 'pizza3d__pizza--hidden': !showPizza }">
        <div class="pizza" :style="pizzaStyle" aria-hidden="true">
          <div class="pizza__crust"></div>
          <div class="pizza__sauce"></div>
          <span v-for="t in toppings" :key="t.id" class="pizza__topping" :style="t.style"></span>
          <span class="pizza__leaf pizza__leaf--1"></span>
          <span class="pizza__leaf pizza__leaf--2"></span>
          <span class="pizza__leaf pizza__leaf--3"></span>
        </div>

        <div class="steam" aria-hidden="true">
          <span class="steam__wisp steam__wisp--1"></span>
          <span class="steam__wisp steam__wisp--2"></span>
          <span class="steam__wisp steam__wisp--3"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** 'closed' | 'opening' | 'open' — orchestrated by the parent hero. */
  stage: { type: String, default: 'closed' },
  /** Active pizza's accent colour (sauce + inner glow). */
  accent: { type: String, default: '#d7172a' },
  /** Fade out the pizza inside when the external carousel takes over. */
  showPizza: { type: Boolean, default: true },
})

const emit = defineEmits(['box-click'])

function onClick() {
  emit('box-click')
}

/* Golden-angle scatter — deterministic, stable across re-renders. */
const TOPPING_COUNT = 10
const toppings = Array.from({ length: TOPPING_COUNT }, (_, i) => {
  const angle = (i * 137.5 * Math.PI) / 180
  const radius = 0.22 + ((i * 37) % 17) / 100
  const x = 50 + Math.cos(angle) * radius * 100
  const y = 50 + Math.sin(angle) * radius * 100
  const size = 12 + ((i * 7) % 7)
  return {
    id: i,
    style: {
      left: `${x}%`,
      top: `${y}%`,
      width: `${size}px`,
      height: `${size}px`,
    },
  }
})

const pizzaStyle = computed(() => ({ '--accent': props.accent }))
</script>

<style scoped>
/*
  Resize / re-proportion by overriding --A (footprint) and --H
  (wall height of each half).  Real pizza box ratio ≈ 10:1.
*/
.pizza3d {
  --A: 340px;
  --H: 36px;

  /* Kraft-paper palette. Each wall picks a specific tint to simulate
     a top-right key light: top brightest → front bright → left mid →
     right slightly dark → back darkest. */
  --kraft-top: #cfa779;
  --kraft-front: #c09863;
  --kraft-left: #b38a56;
  --kraft-right: #a07949;
  --kraft-back: #8d6837;
  --kraft-inner: #e4ccaa;
  --kraft-shadow: #6e5225;
  --kraft-crease: #4a3816;

  /* Tiny fiber noise — SVG encoded as data URI so no extra request. */
  --fiber: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='1.4' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.4  0 0 0 0 0.28  0 0 0 0 0.14  0 0 0 0.6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");

  position: relative;
  width: var(--A);
  height: var(--A);
  transform-style: preserve-3d;
  cursor: pointer;
  user-select: none;

  /* Idle float — killed as soon as the GSAP timeline kicks in. */
  animation: pizza3d-float 5.5s ease-in-out infinite;
}

.pizza3d--opening,
.pizza3d--open {
  animation: none;
}

/* Floor cast shadow */
.pizza3d__shadow {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 86%;
  height: 64%;
  transform: translate(-50%, -50%) translateY(calc(var(--H) * 2)) rotateX(90deg);
  background: radial-gradient(
    ellipse at center,
    rgba(0, 0, 0, 0.78) 0%,
    rgba(0, 0, 0, 0.32) 38%,
    transparent 72%
  );
  filter: blur(22px);
  pointer-events: none;
  transition: opacity 700ms ease;
}

/* Warm glow that brightens as the box opens */
.pizza3d__inner-glow {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 130%;
  height: 130%;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle at center,
    color-mix(in oklab, var(--accent, #d7172a) 55%, #ffb46b) 0%,
    transparent 62%
  );
  filter: blur(56px);
  opacity: 0;
  transition: opacity 900ms ease 100ms;
  pointer-events: none;
  mix-blend-mode: screen;
}
.pizza3d--opening .pizza3d__inner-glow,
.pizza3d--open .pizza3d__inner-glow {
  opacity: 0.75;
}

/*
  The pivot carrying the overall camera-tilt. 0×0 so transform-origin
  stays at the geometric centre of the closed box.
*/
.pizza3d__box {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
  transform: translate(-50%, -50%) rotateX(-54deg) rotateZ(-20deg);
  transition: transform 900ms cubic-bezier(0.2, 0.85, 0.2, 1);
}
.pizza3d--opening .pizza3d__box,
.pizza3d--open .pizza3d__box {
  transform: translate(-50%, -50%) rotateX(-48deg) rotateZ(-10deg);
}

.pizza3d__base,
.pizza3d__lid {
  position: absolute;
  left: 0;
  top: 0;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
}

/* ---- Face primitives ---- */
.face {
  position: absolute;
  left: 0;
  top: 0;
  box-sizing: border-box;
  backface-visibility: visible;
  /* Every face picks up the kraft fiber overlay via ::before */
}

/* Cardboard fibers + directional sheen applied on every face */
.face::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: var(--fiber);
  background-size: 180px 180px;
  mix-blend-mode: multiply;
  opacity: 0.55;
  pointer-events: none;
}

/* Shadow band on the top-inner edge: reads as corrugated "end grain".
   Only applied to base/lid walls — it's the pizza-box tell. */
.rim {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 5px;
  background:
    linear-gradient(180deg, rgba(0, 0, 0, 0.38) 0%, transparent 100%),
    repeating-linear-gradient(
      90deg,
      var(--kraft-crease) 0 2px,
      var(--kraft-inner) 2px 5px,
      var(--kraft-shadow) 5px 7px
    );
  border-bottom: 1px solid rgba(0, 0, 0, 0.25);
}
.rim--lid {
  top: auto;
  bottom: 0;
  border-top: 1px solid rgba(0, 0, 0, 0.25);
  border-bottom: none;
  background:
    linear-gradient(0deg, rgba(0, 0, 0, 0.38) 0%, transparent 100%),
    repeating-linear-gradient(
      90deg,
      var(--kraft-crease) 0 2px,
      var(--kraft-inner) 2px 5px,
      var(--kraft-shadow) 5px 7px
    );
}

/* ---- BASE FACES ---- */
/* Floor — A × A at y = +H, normal up (into the box interior) */
.face--floor {
  width: var(--A);
  height: var(--A);
  margin-left: calc(var(--A) / -2);
  margin-top: calc(var(--A) / -2);
  background:
    radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.25) 0%, transparent 65%),
    linear-gradient(180deg, var(--kraft-inner) 0%, #c9b08a 100%);
  transform: translateY(var(--H)) rotateX(90deg);
  /* Slight inset border reads as the floor "sitting" between walls */
  box-shadow:
    inset 0 0 0 1px rgba(0, 0, 0, 0.15),
    inset 0 0 60px rgba(110, 82, 37, 0.35);
}

/* Front wall — A × H at z = +A/2, normal +Z.
   This one catches the most light (camera-facing + top-lit). */
.face--base-front {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2)) translateZ(calc(var(--A) / 2));
  background: linear-gradient(180deg, var(--kraft-front) 0%, #a07a48 100%);
  box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.35);
}
/* Back wall */
.face--base-back {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2)) translateZ(calc(var(--A) / -2)) rotateY(180deg);
  background: linear-gradient(180deg, var(--kraft-back) 0%, #6d4f27 100%);
}
/* Left wall */
.face--base-left {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2)) translateX(calc(var(--A) / -2)) rotateY(-90deg);
  background: linear-gradient(90deg, #8a6535 0%, var(--kraft-left) 100%);
}
/* Right wall (slightly in shadow because of the Z-rotate on .box) */
.face--base-right {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2)) translateX(calc(var(--A) / 2)) rotateY(90deg);
  background: linear-gradient(270deg, #795a2f 0%, var(--kraft-right) 100%);
}

/* ---- LID ---- */
.pizza3d__lid {
  transform-origin: 0 0 calc(var(--A) / -2);
  transform: rotateX(0deg);
  transition: transform 1000ms cubic-bezier(0.6, 0, 0.15, 1.04);
}
.pizza3d--opening .pizza3d__lid,
.pizza3d--open .pizza3d__lid {
  transform: rotateX(118deg);
}

/* Top of lid — where the label lives */
.face--top {
  width: var(--A);
  height: var(--A);
  margin-left: calc(var(--A) / -2);
  margin-top: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) * -1)) rotateX(90deg);
  background:
    radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.14) 0%, transparent 55%),
    linear-gradient(135deg, #b8874b 0%, var(--kraft-top) 50%, #a77a44 100%);
  display: grid;
  place-items: center;
  box-shadow:
    inset 0 0 0 1px rgba(0, 0, 0, 0.25),
    inset 0 0 80px rgba(74, 56, 22, 0.45);
}

/* Inside of lid — lighter kraft, visible once lid is open */
.face--lid-inside {
  width: var(--A);
  height: var(--A);
  margin-left: calc(var(--A) / -2);
  margin-top: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) * -1 + 1px)) rotateX(-90deg);
  background:
    radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.18) 0%, transparent 60%),
    linear-gradient(180deg, var(--kraft-inner) 0%, #c9b08a 100%);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.2);
}

/* Lid walls mirror the base walls */
.face--lid-front {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2)) translateZ(calc(var(--A) / 2));
  background: linear-gradient(0deg, var(--kraft-front) 0%, #a07a48 100%);
  box-shadow: inset 0 1px 0 rgba(0, 0, 0, 0.35);
}
.face--lid-back {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2)) translateZ(calc(var(--A) / -2)) rotateY(180deg);
  background: linear-gradient(0deg, var(--kraft-back) 0%, #6d4f27 100%);
}
.face--lid-left {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2)) translateX(calc(var(--A) / -2)) rotateY(-90deg);
  background: linear-gradient(90deg, #8a6535 0%, var(--kraft-left) 100%);
}
.face--lid-right {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2)) translateX(calc(var(--A) / 2)) rotateY(90deg);
  background: linear-gradient(270deg, #795a2f 0%, var(--kraft-right) 100%);
}

/* ---- Sticker (printed paper label) ---- */
.sticker {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px 28px;
  background: var(--brand-white);
  color: var(--brand-black);
  box-shadow:
    0 2px 0 rgba(0, 0, 0, 0.12),
    0 1px 2px rgba(0, 0, 0, 0.18);
  /* Slight crooked paste — just enough to feel hand-applied */
  transform: rotate(-1.5deg);
  border: 1px solid rgba(0, 0, 0, 0.12);
}
.sticker__mark {
  width: 34px;
  height: 34px;
  color: var(--brand-black);
}
.sticker__brand {
  font-family: var(--font-serif);
  font-size: 24px;
  letter-spacing: 0.3em;
  line-height: 1;
  color: var(--brand-black);
  font-weight: 500;
}
.sticker__rule {
  display: block;
  width: 30px;
  height: 2px;
  background: var(--brand-red);
}
.sticker__sub {
  font-size: 8px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--brand-black);
  opacity: 0.7;
}

/* ---- Pizza inside the base ---- */
.pizza3d__pizza {
  position: absolute;
  left: 0;
  top: 0;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
  opacity: 0;
  transition: opacity 500ms ease 350ms;
}
.pizza3d--opening .pizza3d__pizza,
.pizza3d--open .pizza3d__pizza {
  opacity: 1;
}
.pizza3d--open .pizza3d__pizza--hidden {
  opacity: 0;
  transition: opacity 400ms ease;
}

.pizza {
  --size: calc(var(--A) * 0.78);
  position: absolute;
  left: 0;
  top: 0;
  width: var(--size);
  height: var(--size);
  margin-left: calc(var(--size) / -2);
  margin-top: calc(var(--size) / -2);
  transform: translateY(calc(var(--H) - 2px)) rotateX(90deg) scale(0.8);
  transition: transform 600ms cubic-bezier(0.2, 0.9, 0.3, 1.1) 400ms;
  border-radius: 50%;
}
.pizza3d--open .pizza {
  transform: translateY(calc(var(--H) - 2px)) rotateX(90deg) scale(1);
}

.pizza__crust {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 50%, #e7b05a 0%, #c17324 68%, #7a4516 100%);
  box-shadow:
    inset 0 -8px 22px rgba(0, 0, 0, 0.35),
    inset 0 0 0 10px rgba(212, 148, 70, 0.45),
    0 12px 28px rgba(0, 0, 0, 0.45);
}
.pizza__sauce {
  position: absolute;
  inset: 8%;
  border-radius: 50%;
  background:
    radial-gradient(circle at 46% 44%, #f3d988 0%, #e4b355 40%, transparent 70%),
    radial-gradient(circle at 50% 50%, var(--accent, #d7172a) 0%, #7a0916 85%);
  box-shadow: inset 0 0 24px rgba(0, 0, 0, 0.25);
}
.pizza__topping {
  position: absolute;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle at 32% 30%, #f0c77b, #7c3313);
  box-shadow:
    0 2px 4px rgba(0, 0, 0, 0.4),
    inset -2px -2px 4px rgba(0, 0, 0, 0.25);
}
.pizza__leaf {
  position: absolute;
  width: 18px;
  height: 10px;
  border-radius: 60% 40% 60% 40% / 80% 20% 80% 20%;
  background: radial-gradient(ellipse at 30% 40%, #6ea03d 0%, #2f5e1f 100%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.35);
  transform: translate(-50%, -50%);
}
.pizza__leaf--1 {
  left: 32%;
  top: 38%;
  transform: translate(-50%, -50%) rotate(24deg);
}
.pizza__leaf--2 {
  left: 62%;
  top: 56%;
  transform: translate(-50%, -50%) rotate(-32deg);
}
.pizza__leaf--3 {
  left: 48%;
  top: 68%;
  transform: translate(-50%, -50%) rotate(72deg);
}

/* Steam */
.steam {
  position: absolute;
  left: 0;
  top: 0;
  width: 0;
  height: 0;
  opacity: 0;
  transition: opacity 500ms ease 700ms;
  transform: translateY(calc(var(--H) * -0.5));
}
/* Steam rides on .pizza3d__pizza's opacity, so it auto-fades with
   the pizza when --hidden is applied — no extra rule needed. */
.pizza3d--opening .steam,
.pizza3d--open .steam {
  opacity: 0.55;
}
.steam__wisp {
  position: absolute;
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.85) 0%, transparent 70%);
  filter: blur(12px);
  animation: steam-rise 3.8s ease-in infinite;
}
.steam__wisp--1 {
  left: -70px;
  animation-delay: 0s;
}
.steam__wisp--2 {
  left: 0;
  animation-delay: 1.2s;
}
.steam__wisp--3 {
  left: 70px;
  animation-delay: 2.4s;
}

@keyframes pizza3d-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
@keyframes steam-rise {
  0% {
    transform: translateY(0) scale(0.6);
    opacity: 0;
  }
  25% {
    opacity: 0.9;
  }
  100% {
    transform: translateY(-180px) scale(1.6);
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .pizza3d {
    --A: 260px;
    --H: 28px;
  }
  .sticker {
    padding: 12px 20px;
  }
  .sticker__brand {
    font-size: 20px;
  }
}
@media (max-width: 420px) {
  .pizza3d {
    --A: 220px;
    --H: 24px;
  }
}
</style>
