<template>
  <div class="carousel">
    <!--
      Each slide carries ONLY the pizza disc now. All copy lives in the
      single text block below the Swiper, synced to activeIndex.
      That removes the "letter soup" you saw between neighbour slides
      while keeping the coverflow depth on the discs themselves.
    -->
    <Swiper
      :modules="modules"
      effect="coverflow"
      :grab-cursor="true"
      :centered-slides="true"
      slides-per-view="auto"
      :loop="pizzas.length > 3"
      :speed="650"
      :initial-slide="initialIndex"
      :coverflow-effect="{
        rotate: 22,
        stretch: 0,
        depth: 260,
        modifier: 1,
        slideShadows: false,
      }"
      :navigation="{
        prevEl: '.carousel__nav--prev',
        nextEl: '.carousel__nav--next',
      }"
      :pagination="{
        clickable: true,
        el: '.carousel__pager',
        bulletClass: 'carousel__dot',
        bulletActiveClass: 'carousel__dot--active',
      }"
      :keyboard="{ enabled: true }"
      @slide-change="onSlideChange"
      class="carousel__swiper"
    >
      <SwiperSlide
        v-for="(pizza, index) in pizzas"
        :key="pizza.id"
        class="carousel__slide"
      >
        <button
          type="button"
          class="disc"
          :class="{ 'disc--active': index === activeIndex }"
          :style="{ '--accent': pizza.accent }"
          :aria-label="`Ver ${pizza.name}`"
          @click="$emit('details', pizza)"
        >
          <img
            v-if="pizza.image"
            :src="pizza.image"
            :alt="`Pizza ${pizza.name}`"
            class="disc__img"
          />
          <span v-else class="fake-pizza" aria-hidden="true">
            <span class="fake-pizza__sauce"></span>
            <span
              v-for="t in toppingPositions(pizza.id)"
              :key="t.k"
              class="fake-pizza__topping"
              :style="t.style"
            ></span>
          </span>
        </button>
      </SwiperSlide>
    </Swiper>

    <button class="carousel__nav carousel__nav--prev" aria-label="Anterior pizza">‹</button>
    <button class="carousel__nav carousel__nav--next" aria-label="Siguiente pizza">›</button>

    <!--
      Single, authoritative text block. Swapping the :key on transition
      gives a quick cross-fade whenever the active pizza changes —
      prevents any visual stutter of stale text under new text.
    -->
    <transition name="copy" mode="out-in">
      <div :key="active.id" class="copy">
        <p class="copy__tagline">{{ active.tagline }}</p>
        <h2 class="copy__name">{{ active.name }}</h2>
        <p class="copy__desc">{{ active.description }}</p>
        <p class="copy__price">{{ active.price.toFixed(2) }} €</p>
      </div>
    </transition>

    <div class="carousel__actions">
      <button class="btn btn--primary" type="button" @click="$emit('order', active)">
        <span>Pídela ahora</span>
        <span class="btn__arrow" aria-hidden="true">→</span>
      </button>
      <button class="btn btn--ghost" type="button" @click="$emit('details', active)">
        Ver ingredientes
      </button>
    </div>

    <div class="carousel__pager"></div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectCoverflow, Navigation, Pagination, Keyboard } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/effect-coverflow'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const props = defineProps({
  pizzas: { type: Array, required: true },
  initialIndex: { type: Number, default: 0 },
})

const emit = defineEmits(['active-change', 'order', 'details'])

const modules = [EffectCoverflow, Navigation, Pagination, Keyboard]

const activeIndex = ref(props.initialIndex)
const active = computed(() => props.pizzas[activeIndex.value] ?? props.pizzas[0])

function onSlideChange(swiper) {
  activeIndex.value = swiper.realIndex
  emit('active-change', swiper.realIndex)
}

function toppingPositions(seed) {
  const count = 7
  return Array.from({ length: count }, (_, k) => {
    const angle = ((seed * 31 + k * 47) % 360) * (Math.PI / 180)
    const radius = 0.22 + ((seed + k * 11) % 14) / 100
    const x = 50 + Math.cos(angle) * radius * 100
    const y = 50 + Math.sin(angle) * radius * 100
    const size = 10 + ((seed + k) % 4) * 3
    return {
      k,
      style: {
        left: `${x}%`,
        top: `${y}%`,
        width: `${size}px`,
        height: `${size}px`,
      },
    }
  })
}
</script>

<style scoped>
.carousel {
  position: relative;
  max-width: 1100px;
  margin: 0 auto;
  padding-bottom: 40px;
}

.carousel__swiper {
  overflow: visible !important;
  padding: 18px 0 24px;
}

.carousel__slide {
  width: 260px;
  display: flex;
  justify-content: center;
}

/* A slide is just a clickable pizza disc */
.disc {
  position: relative;
  width: 220px;
  height: 220px;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  opacity: 0.45;
  transition: opacity 500ms ease, filter 500ms ease, transform 500ms ease;
  filter: drop-shadow(0 26px 42px rgba(0, 0, 0, 0.55));
}
.disc--active {
  opacity: 1;
  filter:
    drop-shadow(0 30px 48px rgba(0, 0, 0, 0.6))
    drop-shadow(0 0 36px color-mix(in oklab, var(--accent, #d7172a) 50%, transparent));
}
.disc__img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 50%;
}

/* Fallback painted pizza until real photos are plugged in */
.fake-pizza {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 50%, #e7b05a 0%, #c17324 70%, #7a4516 100%);
  box-shadow:
    inset 0 0 0 12px rgba(212, 148, 70, 0.5),
    inset 0 -10px 30px rgba(0, 0, 0, 0.35);
}
.fake-pizza__sauce {
  position: absolute;
  inset: 9%;
  border-radius: 50%;
  background:
    radial-gradient(circle at 46% 44%, #f3d988 0%, #e4b355 38%, transparent 65%),
    radial-gradient(circle at 50% 50%, var(--accent, #d7172a) 0%, #7a0916 90%);
}
.fake-pizza__topping {
  position: absolute;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle at 32% 30%, #f0c77b, #7c3313);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.45), inset -2px -2px 4px rgba(0, 0, 0, 0.25);
}

/* Single text block — synced to active slide */
.copy {
  text-align: center;
  max-width: 520px;
  margin: 10px auto 24px;
  padding: 0 20px;
  color: var(--ink-100);
}
.copy__tagline {
  font-size: 11px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--brand-red);
  margin: 0 0 10px;
  font-weight: 500;
}
.copy__name {
  font-family: var(--font-serif);
  font-size: clamp(36px, 5vw, 56px);
  margin: 0 0 12px;
  line-height: 1;
  color: var(--brand-white);
  letter-spacing: 0.005em;
}
.copy__desc {
  font-size: 14px;
  line-height: 1.6;
  color: rgba(245, 243, 238, 0.72);
  margin: 0 0 12px;
}
.copy__price {
  font-family: var(--font-serif);
  font-size: 22px;
  color: var(--brand-red);
  margin: 0;
}

.copy-enter-active,
.copy-leave-active {
  transition: opacity 260ms ease, transform 260ms ease;
}
.copy-enter-from { opacity: 0; transform: translateY(8px); }
.copy-leave-to   { opacity: 0; transform: translateY(-8px); }

/* Nav arrows */
.carousel__nav {
  position: absolute;
  top: 110px; /* aligned with centre of disc row */
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 1px solid rgba(245, 243, 238, 0.22);
  background: rgba(10, 7, 7, 0.55);
  color: var(--brand-white);
  font-size: 26px;
  cursor: pointer;
  display: grid;
  place-items: center;
  z-index: 20;
  transition: all 220ms ease;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  padding: 0;
  line-height: 1;
}
.carousel__nav:hover {
  border-color: var(--brand-red);
  color: var(--brand-red);
  transform: scale(1.05);
}
.carousel__nav--prev { left: -8px; }
.carousel__nav--next { right: -8px; }

/* CTAs */
.carousel__actions {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 6px;
  flex-wrap: wrap;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  border-radius: 2px;
  cursor: pointer;
  transition: all 240ms ease;
  border: 1px solid transparent;
  font-weight: 600;
}
.btn--primary {
  background: var(--brand-red);
  color: var(--brand-white);
  box-shadow: 0 10px 24px rgba(215, 23, 42, 0.35);
}
.btn--primary:hover {
  background: var(--brand-red-deep);
  transform: translateY(-2px);
  box-shadow: 0 16px 32px rgba(215, 23, 42, 0.5);
}
.btn__arrow {
  transition: transform 240ms ease;
}
.btn--primary:hover .btn__arrow {
  transform: translateX(5px);
}
.btn--ghost {
  background: transparent;
  color: var(--brand-white);
  border-color: rgba(245, 243, 238, 0.35);
}
.btn--ghost:hover {
  border-color: var(--brand-white);
  color: var(--brand-white);
  background: rgba(245, 243, 238, 0.05);
}

.carousel__pager {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 22px;
}
:deep(.carousel__dot) {
  width: 22px;
  height: 2px;
  background: rgba(245, 243, 238, 0.22);
  border: none;
  border-radius: 0;
  opacity: 1;
  transition: all 260ms ease;
  cursor: pointer;
  padding: 0;
}
:deep(.carousel__dot--active) {
  width: 40px;
  background: var(--brand-red);
}

@media (max-width: 640px) {
  .carousel__slide { width: 210px; }
  .disc { width: 170px; height: 170px; }
  .carousel__nav { top: 85px; display: none; }
  .copy__name { font-size: 32px; }
}
</style>
