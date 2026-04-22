<template>
  <div class="carousel">
    <!--
      Swiper w/ EffectCoverflow gives the premium "record-sleeve" depth we
      want without hand-rolling it. slidesPerView='auto' lets cards keep
      their own width so the carousel adapts to viewport.
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
        rotate: 18,
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
        <article
          class="card"
          :class="{ 'card--active': index === activeIndex }"
          @click="$emit('details', pizza)"
        >
          <!-- Pizza artwork. Swap the <FakePizza /> block for an <img>
               (or optimized <picture>) once real product photos arrive. -->
          <div class="card__plate" :style="{ '--accent': pizza.accent }">
            <img
              v-if="pizza.image"
              :src="pizza.image"
              :alt="`Pizza ${pizza.name}`"
              class="card__img"
            />
            <div v-else class="fake-pizza" aria-hidden="true">
              <span class="fake-pizza__sauce"></span>
              <span
                v-for="t in toppingPositions(pizza.id)"
                :key="t.k"
                class="fake-pizza__topping"
                :style="t.style"
              ></span>
            </div>
          </div>

          <h2 class="card__name">{{ pizza.name }}</h2>
          <p class="card__tagline">{{ pizza.tagline }}</p>
          <p class="card__desc">{{ pizza.description }}</p>
          <div class="card__price">{{ pizza.price.toFixed(2) }} €</div>
        </article>
      </SwiperSlide>
    </Swiper>

    <button class="carousel__nav carousel__nav--prev" aria-label="Anterior pizza">‹</button>
    <button class="carousel__nav carousel__nav--next" aria-label="Siguiente pizza">›</button>

    <div class="carousel__actions">
      <button class="btn btn--primary" type="button" @click="$emit('order', current)">
        <span>Pídela ahora</span>
        <span class="btn__arrow">→</span>
      </button>
      <button class="btn btn--ghost" type="button" @click="$emit('details', current)">
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
const current = computed(() => props.pizzas[activeIndex.value] ?? props.pizzas[0])

function onSlideChange(swiper) {
  // Use realIndex so loop-mode duplicate slides resolve to the source pizza.
  activeIndex.value = swiper.realIndex
  emit('active-change', swiper.realIndex)
}

/*
  Deterministic fake-topping layout per pizza. Stable across renders
  so there's no topping jitter while Swiper transitions.
*/
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
  padding-bottom: 90px;
}

.carousel__swiper {
  overflow: visible !important;
  padding: 30px 0 48px;
}

.carousel__slide {
  width: 320px;
  display: flex;
  justify-content: center;
}

.card {
  width: 100%;
  text-align: center;
  color: var(--ink-100);
  transition: opacity 500ms ease, transform 500ms ease;
  opacity: 0.4;
  cursor: pointer;
}
.card--active {
  opacity: 1;
}

.card__plate {
  width: 230px;
  height: 230px;
  margin: 0 auto 24px;
  position: relative;
  filter: drop-shadow(0 30px 50px rgba(0, 0, 0, 0.55))
          drop-shadow(0 0 42px color-mix(in oklab, var(--accent, #c94d3a) 40%, transparent));
  transition: filter 500ms ease;
}

.card__img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Fallback painted pizza while real photos aren't ready */
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
    radial-gradient(circle at 50% 50%, var(--accent, #c94d3a) 0%, #872820 90%);
}
.fake-pizza__topping {
  position: absolute;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle at 32% 30%, #f0c77b, #7c3313);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.45), inset -2px -2px 4px rgba(0, 0, 0, 0.25);
}

.card__name {
  font-family: var(--font-serif);
  font-size: 38px;
  margin: 0 0 6px;
  letter-spacing: 0.008em;
  line-height: 1;
}
.card__tagline {
  color: var(--ink-300);
  font-size: 11px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  margin: 0 0 14px;
}
.card__desc {
  font-size: 14px;
  line-height: 1.55;
  color: rgba(244, 235, 217, 0.72);
  max-width: 280px;
  margin: 0 auto;
}
.card__price {
  margin-top: 16px;
  font-family: var(--font-serif);
  font-size: 24px;
  color: var(--ink-300);
}

/* Nav arrows — discreet glass buttons on either side */
.carousel__nav {
  position: absolute;
  top: 38%;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 1px solid rgba(244, 235, 217, 0.2);
  background: rgba(15, 10, 8, 0.5);
  color: var(--ink-100);
  font-size: 26px;
  cursor: pointer;
  display: grid;
  place-items: center;
  transform: translateY(-50%);
  z-index: 20;
  transition: all 220ms ease;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  padding: 0;
  line-height: 1;
}
.carousel__nav:hover {
  border-color: var(--ink-300);
  color: var(--ink-300);
  transform: translateY(-50%) scale(1.05);
}
.carousel__nav--prev { left: -8px; }
.carousel__nav--next { right: -8px; }

/* CTAs */
.carousel__actions {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 10px;
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
  border-radius: 999px;
  cursor: pointer;
  transition: all 240ms ease;
  border: 1px solid transparent;
  font-weight: 600;
}
.btn--primary {
  background: linear-gradient(180deg, #d9a55a 0%, #a87429 100%);
  color: #1a0f07;
  box-shadow: 0 12px 30px rgba(168, 116, 41, 0.35);
}
.btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(168, 116, 41, 0.55);
}
.btn__arrow {
  transition: transform 240ms ease;
}
.btn--primary:hover .btn__arrow {
  transform: translateX(5px);
}
.btn--ghost {
  background: transparent;
  color: var(--ink-100);
  border-color: rgba(244, 235, 217, 0.28);
}
.btn--ghost:hover {
  border-color: var(--ink-300);
  color: var(--ink-300);
}

/* Pagination dots styled as minimalist bars */
.carousel__pager {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 24px;
}
:deep(.carousel__dot) {
  width: 22px;
  height: 2px;
  background: rgba(244, 235, 217, 0.25);
  border: none;
  border-radius: 0;
  opacity: 1;
  transition: all 260ms ease;
  cursor: pointer;
  padding: 0;
}
:deep(.carousel__dot--active) {
  width: 40px;
  background: var(--ink-300);
}

@media (max-width: 640px) {
  .carousel__slide { width: 260px; }
  .card__plate { width: 180px; height: 180px; margin-bottom: 18px; }
  .card__name { font-size: 30px; }
  .carousel__nav { display: none; }
  .carousel { padding-bottom: 70px; }
}
</style>
