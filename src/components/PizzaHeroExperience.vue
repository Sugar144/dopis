<template>
  <section class="hero">
    <div class="scene">
      <div class="box-wrap">
        <div class="pizza-box" :class="stage" @click="openBox">
          <div class="lid"></div>

          <div class="base">
            <div class="inside" :class="{ visible: stage === 'open' }">
              <button class="nav nav-left" @click.stop="prev">‹</button>

              <div class="carousel">
                <div
                  v-for="(item, index) in items"
                  :key="item.id"
                  class="carousel-item"
                  :class="[item.type, { active: index === activeIndex }]"
                  :style="itemStyle(index)"
                >
                  <span class="item-label">{{ item.label }}</span>
                </div>
              </div>

              <button class="nav nav-right" @click.stop="next">›</button>
            </div>
          </div>
        </div>
      </div>

      <div class="controls">
        <button class="ghost-btn" @click="resetBox">Reset</button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'

const stage = ref('closed')
const activeIndex = ref(2) // pizza is the central initial option
let openTimer = null

const items = [
  { id: 1, type: 'side', label: '1' },
  { id: 2, type: 'drink', label: '2' },
  { id: 3, type: 'pizza', label: 'P' }, // central active item
  { id: 4, type: 'dessert', label: '4' },
  { id: 5, type: 'sauce', label: '5' },
]

function openBox() {
  if (stage.value !== 'closed') return

  // First the box grows, still closed
  stage.value = 'growing'

  // Only when the growing finishes, the box opens
  clearTimeout(openTimer)
  openTimer = setTimeout(() => {
    stage.value = 'open'
  }, 700)
}

function resetBox() {
  clearTimeout(openTimer)
  stage.value = 'closed'
  activeIndex.value = 2
}

function prev() {
  activeIndex.value = (activeIndex.value - 1 + items.length) % items.length
}

function next() {
  activeIndex.value = (activeIndex.value + 1) % items.length
}

function itemStyle(index) {
  const diff = index - activeIndex.value

  // position each item around the active center item
  const x = diff * 110

  let scale = 0.55
  let opacity = 0.25
  let zIndex = 1

  if (diff === 0) {
    scale = 1.45
    opacity = 1
    zIndex = 3
  } else if (Math.abs(diff) === 1) {
    scale = 0.82
    opacity = 0.7
    zIndex = 2
  } else if (Math.abs(diff) === 2) {
    scale = 0.58
    opacity = 0.35
    zIndex = 1
  }

  return {
    transform: `translate(calc(-50% + ${x}px), -50%) scale(${scale})`,
    opacity,
    zIndex,
  }
}

onBeforeUnmount(() => {
  clearTimeout(openTimer)
})
</script>

<style scoped>
.hero {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: #f8f5f1;
  overflow: hidden;
}

.scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.box-wrap {
  perspective: 1200px;
}

.pizza-box {
  --box-size: 220px;
  position: relative;
  width: var(--box-size);
  height: var(--box-size);
  transform: scale(0.72);
  transform-origin: center center;
  transition: transform 700ms ease;
  cursor: pointer;
}

.pizza-box.closed {
  transform: scale(0.72);
}

.pizza-box.growing {
  /* grows but still stays closed */
  transform: scale(1.35);
}

.pizza-box.open {
  /* same max size, but now opened */
  transform: scale(1.35);
}

.base,
.lid {
  position: absolute;
  left: 0;
  width: 100%;
  height: 100%;
  border: 3px solid #4f4035;
  border-radius: 10px;
  background: #e7d8c4;
  box-sizing: border-box;
}

.base {
  bottom: 0;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.lid {
  top: 0;
  z-index: 4;
  transform-origin: top center;
  transition:
    transform 600ms ease,
    box-shadow 600ms ease;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
}

/* While growing, still closed */
.pizza-box.growing .lid {
  transform: rotateX(0deg) translateY(0);
}

/* Only when fully grown, it opens */
.pizza-box.open .lid {
  transform: rotateX(-108deg) translateY(-8px);
  box-shadow: none;
}

.inside {
  position: absolute;
  inset: 0;
  opacity: 0;
  pointer-events: none;
  transition: opacity 260ms ease;
}

.inside.visible {
  opacity: 1;
  pointer-events: auto;
}

.carousel {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.carousel-item {
  position: absolute;
  top: 52%;
  left: 50%;
  width: 92px;
  height: 92px;
  border-radius: 999px;
  border: 3px solid #4f4035;
  background: #d9d2ca;
  display: grid;
  place-items: center;
  transition:
    transform 320ms ease,
    opacity 320ms ease;
  box-sizing: border-box;
}

.item-label {
  font-weight: 700;
  font-size: 20px;
  color: #4f4035;
  user-select: none;
}

/* Simple pizza look */
.carousel-item.pizza {
  background:
    radial-gradient(circle at 30% 30%, #c7362d 0 6px, transparent 7px),
    radial-gradient(circle at 68% 38%, #c7362d 0 6px, transparent 7px),
    radial-gradient(circle at 42% 68%, #c7362d 0 6px, transparent 7px),
    radial-gradient(circle at 65% 70%, #c7362d 0 6px, transparent 7px), #f0b55c;
  border-color: #8c5a2b;
  box-shadow: inset 0 0 0 8px #d58c3a;
}

.carousel-item.pizza .item-label {
  color: #5c2f12;
}

/* Other options are just circles */
.carousel-item.drink {
  background: #d7e9f5;
}

.carousel-item.side {
  background: #e5decf;
}

.carousel-item.dessert {
  background: #f2d9d9;
}

.carousel-item.sauce {
  background: #efe7c7;
}

.carousel-item.active {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.16);
}

.nav {
  position: absolute;
  top: 52%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  border-radius: 999px;
  border: 2px solid #4f4035;
  background: rgba(255, 255, 255, 0.85);
  color: #4f4035;
  font-size: 28px;
  line-height: 1;
  display: grid;
  place-items: center;
  cursor: pointer;
  z-index: 10;
}

.nav-left {
  left: 12px;
}

.nav-right {
  right: 12px;
}

.controls {
  display: flex;
  gap: 12px;
}

.ghost-btn {
  border: 1px solid #4f4035;
  background: transparent;
  color: #4f4035;
  padding: 10px 16px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
}
</style>
