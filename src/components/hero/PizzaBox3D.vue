<template>
  <!--
    Pseudo-3D pizza box built entirely with CSS 3D transforms.
    Why not Three.js: for a single hero prop we gain nothing from WebGL and
    lose a lot of bytes + tooling. preserve-3d + real CSS geometry gives a
    convincing box and stays trivial to style/tune.

    Anatomy:
      - .pizza3d__box is the pivot carrying the camera-tilt.
      - .pizza3d__base = 5 faces (floor + 4 walls) of the lower half.
      - .pizza3d__lid  = 5 faces (top + 4 walls), hinged at the back edge
        of the base via transform-origin, pivots open with rotateX.
      - .pizza3d__pizza sits on the base floor and is revealed when the lid opens.

    Coord system used (CSS convention — Y points DOWN):
      origin = geometric centre of the closed box
      +X right, +Y down, +Z toward viewer
      base walls span y ∈ [0, +H]; lid walls span y ∈ [-H, 0]
  -->
  <div class="pizza3d" :class="[`pizza3d--${stage}`]" @click="onClick">
    <!-- Soft cast shadow on the "floor" so the box reads as floating, not pasted -->
    <div class="pizza3d__shadow" aria-hidden="true"></div>

    <!-- Warm light spilling out of the box when it opens -->
    <div class="pizza3d__inner-glow" aria-hidden="true"></div>

    <div class="pizza3d__box">
      <!-- BASE (lower half) -->
      <div class="pizza3d__base">
        <div class="face face--floor"></div>
        <div class="face face--base-front"></div>
        <div class="face face--base-back"></div>
        <div class="face face--base-left"></div>
        <div class="face face--base-right"></div>
      </div>

      <!-- LID (upper half, hinged at the back edge) -->
      <div class="pizza3d__lid">
        <div class="face face--top">
          <!-- Sticker — replace with the real SVG logo. It's applied on the
               exterior and will naturally hide as the lid rotates away. -->
          <div class="lid-sticker">
            <span class="lid-sticker__brand">DOPIS</span>
            <span class="lid-sticker__sub">Pizzeria · Napoli · 1987</span>
          </div>
        </div>
        <div class="face face--lid-front"></div>
        <div class="face face--lid-back"></div>
        <div class="face face--lid-left"></div>
        <div class="face face--lid-right"></div>

        <!-- Interior-of-lid face: plain cardboard visible once lid is open.
             Drawn slightly inside the exterior so we don't Z-fight. -->
        <div class="face face--lid-inside"></div>
      </div>

      <!-- Pizza inside the base -->
      <div class="pizza3d__pizza">
        <div class="pizza" :style="pizzaStyle" aria-hidden="true">
          <div class="pizza__crust"></div>
          <div class="pizza__sauce"></div>
          <span
            v-for="t in toppings"
            :key="t.id"
            class="pizza__topping"
            :style="t.style"
          ></span>
          <!-- subtle basil leaves -->
          <span class="pizza__leaf pizza__leaf--1"></span>
          <span class="pizza__leaf pizza__leaf--2"></span>
          <span class="pizza__leaf pizza__leaf--3"></span>
        </div>

        <!-- "Steam" rising off a hot pizza — three filtered wisps -->
        <div class="steam" aria-hidden="true">
          <span class="steam__wisp steam__wisp--1"></span>
          <span class="steam__wisp steam__wisp--2"></span>
          <span class="steam__wisp steam__wisp--3"></span>
        </div>
      </div>
    </div>

    <!-- Click hint only when box is closed and inviting interaction -->
    <transition name="hint">
      <span v-if="stage === 'closed'" class="pizza3d__hint">
        Toca la caja
      </span>
    </transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** 'closed' | 'opening' | 'open' — orchestrated by the parent hero. */
  stage: { type: String, default: 'closed' },
  /** Active pizza's accent colour — feeds both sauce and inner glow. */
  accent: { type: String, default: '#c94d3a' },
})

const emit = defineEmits(['box-click'])

function onClick() {
  emit('box-click')
}

/*
  Deterministic topping placement using the golden angle — gives an even,
  non-grid scatter across the pizza. Stable by index so we can animate
  without topping "jitter".
*/
const TOPPING_COUNT = 10
const toppings = Array.from({ length: TOPPING_COUNT }, (_, i) => {
  const angle = (i * 137.5 * Math.PI) / 180
  const radius = 0.22 + ((i * 37) % 17) / 100 // 22%–39% of pizza radius
  const x = 50 + Math.cos(angle) * radius * 100
  const y = 50 + Math.sin(angle) * radius * 100
  const size = 12 + ((i * 7) % 7) // 12–18px
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
  Whole box is driven by two CSS variables — resize/re-proportion by
  overriding --A (footprint) and --H (wall height of each half).
*/
.pizza3d {
  --A: 340px;
  --H: 44px;

  --cardboard: #2a1d14;
  --cardboard-mid: #3d2918;
  --cardboard-light: #5a3d26;
  --interior: #e8d1a8;
  --interior-deep: #b89668;

  position: relative;
  width: var(--A);
  height: var(--A);
  transform-style: preserve-3d;
  cursor: pointer;
  user-select: none;

  /* Gentle idle float while the box is still closed. Killed as soon as
     the user interacts so the GSAP timeline has full control. */
  animation: pizza3d-float 5.5s ease-in-out infinite;
}

.pizza3d--opening,
.pizza3d--open {
  animation: none;
}

/* Cast shadow on the ground. Rotated to lie flat so it moves with
   perspective — more convincing than a plain box-shadow. */
.pizza3d__shadow {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 86%;
  height: 64%;
  transform: translate(-50%, -50%) translateY(calc(var(--H) * 1.8)) rotateX(90deg);
  background: radial-gradient(
    ellipse at center,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.32) 38%,
    transparent 72%
  );
  filter: blur(18px);
  pointer-events: none;
  transition: opacity 700ms ease, transform 700ms ease;
}
.pizza3d--opening .pizza3d__shadow,
.pizza3d--open .pizza3d__shadow {
  width: 96%;
  opacity: 0.9;
}

/* Inner glow that "spills out" when the box opens — a warm, slightly
   tinted radial that sits behind/under the box scene. */
.pizza3d__inner-glow {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 120%;
  height: 120%;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle at center,
    color-mix(in oklab, var(--accent, #c94d3a) 40%, #f4d07a) 0%,
    transparent 60%
  );
  filter: blur(48px);
  opacity: 0;
  transition: opacity 900ms ease 100ms;
  pointer-events: none;
  mix-blend-mode: screen;
}
.pizza3d--opening .pizza3d__inner-glow,
.pizza3d--open .pizza3d__inner-glow {
  opacity: 0.65;
}

/*
  .pizza3d__box is a 0×0 pivot anchored at the centre of the wrapper.
  All faces live in this pivot's local frame (via explicit translateX/Y/Z
  from the origin). The overall camera-tilt lives here too.
*/
.pizza3d__box {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  transform-style: preserve-3d;
  transform: translate(-50%, -50%) rotateX(-55deg) rotateZ(-18deg);
  transition: transform 900ms cubic-bezier(0.2, 0.85, 0.2, 1);
}

/* When opening we straighten up a touch so the camera peeks a bit more
   head-on into the interior. */
.pizza3d--opening .pizza3d__box,
.pizza3d--open .pizza3d__box {
  transform: translate(-50%, -50%) rotateX(-50deg) rotateZ(-10deg);
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

/*
  ---- Face primitives ----
  All faces are absolutely positioned at the pivot origin. Widths are
  set per-face; margins recentre the element so rotations pivot around
  the face's centre.
*/
.face {
  position: absolute;
  left: 0;
  top: 0;
  background: var(--cardboard);
  box-sizing: border-box;
  backface-visibility: visible;
}

/* Shared cardboard micro-texture */
.face::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(
      90deg,
      transparent 0 14px,
      rgba(255, 255, 255, 0.025) 14px 15px
    ),
    linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(0, 0, 0, 0.2));
  pointer-events: none;
}

/* ---- BASE FACES ---- */
/* Floor: A × A rectangle lying flat at y = +H, normal up (into box) */
.face--floor {
  width: var(--A);
  height: var(--A);
  margin-left: calc(var(--A) / -2);
  margin-top: calc(var(--A) / -2);
  background:
    radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.18) 0%, transparent 65%),
    linear-gradient(180deg, var(--interior) 0%, var(--interior-deep) 100%);
  transform: translateY(var(--H)) rotateX(90deg);
}
.face--floor::before {
  background:
    repeating-linear-gradient(
      45deg,
      transparent 0 20px,
      rgba(120, 80, 38, 0.06) 20px 21px
    );
}

/* Front wall of base: A × H at z = +A/2, normal +Z */
.face--base-front {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2)) translateZ(calc(var(--A) / 2));
  background: linear-gradient(180deg, var(--cardboard-mid) 0%, var(--cardboard) 100%);
}
/* Back wall: z = -A/2, rotated so its outer face points -Z */
.face--base-back {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2))
             translateZ(calc(var(--A) / -2))
             rotateY(180deg);
  background: linear-gradient(180deg, var(--cardboard) 0%, #1d1209 100%);
}
/* Left wall: A wide × H tall rectangle whose X axis maps to world Z */
.face--base-left {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2))
             translateX(calc(var(--A) / -2))
             rotateY(-90deg);
  background: linear-gradient(90deg, #241810 0%, var(--cardboard-light) 100%);
}
/* Right wall */
.face--base-right {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / 2))
             translateX(calc(var(--A) / 2))
             rotateY(90deg);
  background: linear-gradient(270deg, #241810 0%, var(--cardboard-light) 100%);
}

/* ---- LID ----
   Hinge line = back-top edge of the base → (y=0, z=-A/2), parallel to X.
   Placing transform-origin at that line means a single rotateX on
   .pizza3d__lid opens it like a real hinge. */
.pizza3d__lid {
  transform-origin: 0 0 calc(var(--A) / -2);
  transform: rotateX(0deg);
  transition: transform 1000ms cubic-bezier(0.6, 0, 0.15, 1.04);
}
.pizza3d--opening .pizza3d__lid,
.pizza3d--open .pizza3d__lid {
  /* Slight overshoot past 90° gives the natural "flopped back" feel. */
  transform: rotateX(118deg);
}

/* Exterior top of lid. rotateX(90) keeps the normal pointing up in CSS
   (i.e. visually up) — same as the base floor. */
.face--top {
  width: var(--A);
  height: var(--A);
  margin-left: calc(var(--A) / -2);
  margin-top: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) * -1)) rotateX(90deg);
  background:
    radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.08) 0%, transparent 55%),
    linear-gradient(135deg, #241810 0%, var(--cardboard-mid) 55%, var(--cardboard) 100%);
  display: grid;
  place-items: center;
  border: 1px solid rgba(0, 0, 0, 0.5);
}

.lid-sticker {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  color: #e9c97a;
  text-align: center;
  padding: 16px 26px;
  border: 1px solid rgba(233, 201, 122, 0.55);
  background: rgba(15, 10, 8, 0.65);
  box-shadow: inset 0 0 28px rgba(233, 201, 122, 0.12);
}
.lid-sticker__brand {
  font-family: var(--font-serif);
  font-size: 28px;
  letter-spacing: 0.26em;
  line-height: 1;
}
.lid-sticker__sub {
  font-size: 9px;
  letter-spacing: 0.38em;
  text-transform: uppercase;
  opacity: 0.8;
}

/* Inside face of lid — sits just below the exterior top, visible once
   the lid is rotated open. Normal points the opposite way. */
.face--lid-inside {
  width: var(--A);
  height: var(--A);
  margin-left: calc(var(--A) / -2);
  margin-top: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) * -1 + 1px)) rotateX(-90deg);
  background:
    radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.22) 0%, transparent 60%),
    linear-gradient(180deg, #3a2818 0%, #1c120b 100%);
}

/* Lid walls: mirror of base walls shifted to y ∈ [-H, 0] */
.face--lid-front {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2)) translateZ(calc(var(--A) / 2));
  background: linear-gradient(0deg, var(--cardboard-mid) 0%, var(--cardboard) 100%);
}
.face--lid-back {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2))
             translateZ(calc(var(--A) / -2))
             rotateY(180deg);
  background: linear-gradient(0deg, var(--cardboard) 0%, #1d1209 100%);
}
.face--lid-left {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2))
             translateX(calc(var(--A) / -2))
             rotateY(-90deg);
  background: linear-gradient(90deg, #241810 0%, var(--cardboard-light) 100%);
}
.face--lid-right {
  width: var(--A);
  height: var(--H);
  margin-left: calc(var(--A) / -2);
  transform: translateY(calc(var(--H) / -2))
             translateX(calc(var(--A) / 2))
             rotateY(90deg);
  background: linear-gradient(270deg, #241810 0%, var(--cardboard-light) 100%);
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

.pizza {
  --size: calc(var(--A) * 0.78);
  position: absolute;
  left: 0;
  top: 0;
  width: var(--size);
  height: var(--size);
  margin-left: calc(var(--size) / -2);
  margin-top: calc(var(--size) / -2);
  /* Rests flat on the floor at y = +H (2px lift to avoid Z-fight). */
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
    radial-gradient(circle at 50% 50%, var(--accent, #c94d3a) 0%, #8a2920 85%);
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

/* Basil leaves for a pop of green — purely decorative */
.pizza__leaf {
  position: absolute;
  width: 18px;
  height: 10px;
  border-radius: 60% 40% 60% 40% / 80% 20% 80% 20%;
  background: radial-gradient(ellipse at 30% 40%, #6ea03d 0%, #2f5e1f 100%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.35);
  transform: translate(-50%, -50%);
}
.pizza__leaf--1 { left: 32%; top: 38%; transform: translate(-50%, -50%) rotate(24deg); }
.pizza__leaf--2 { left: 62%; top: 56%; transform: translate(-50%, -50%) rotate(-32deg); }
.pizza__leaf--3 { left: 48%; top: 68%; transform: translate(-50%, -50%) rotate(72deg); }

/* Steam — three wisps rising off the pizza */
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
.steam__wisp--1 { left: -70px; animation-delay: 0s; }
.steam__wisp--2 { left: 0; animation-delay: 1.2s; }
.steam__wisp--3 { left: 70px; animation-delay: 2.4s; }

/* Click hint */
.pizza3d__hint {
  position: absolute;
  bottom: -46px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  color: rgba(244, 235, 217, 0.58);
  white-space: nowrap;
}
.pizza3d__hint::after {
  content: '';
  display: block;
  width: 1px;
  height: 22px;
  margin: 10px auto 0;
  background: linear-gradient(to bottom, rgba(244, 235, 217, 0.55), transparent);
  animation: hint-pulse 1.8s ease-in-out infinite;
}

.hint-enter-active,
.hint-leave-active {
  transition: opacity 400ms ease;
}
.hint-enter-from,
.hint-leave-to {
  opacity: 0;
}

@keyframes pizza3d-float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-10px); }
}
@keyframes hint-pulse {
  0%, 100% { opacity: 0.3; transform: scaleY(0.6); transform-origin: top; }
  50%      { opacity: 1;   transform: scaleY(1); }
}
@keyframes steam-rise {
  0%   { transform: translateY(0) scale(0.6); opacity: 0; }
  25%  { opacity: 0.9; }
  100% { transform: translateY(-180px) scale(1.6); opacity: 0; }
}

/* Scale-down on smaller screens so the box still feels like a hero
   centrepiece without overflowing. */
@media (max-width: 768px) {
  .pizza3d {
    --A: 260px;
    --H: 36px;
  }
}
@media (max-width: 420px) {
  .pizza3d {
    --A: 220px;
    --H: 32px;
  }
}
</style>
