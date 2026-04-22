<template>
  <main class="detail">
    <RouterLink to="/" class="detail__back">← Volver</RouterLink>

    <article v-if="pizza" class="detail__content">
      <p class="detail__eyebrow">{{ pizza.tagline }}</p>
      <h1 class="detail__title">{{ pizza.name }}</h1>
      <p class="detail__desc">{{ pizza.description }}</p>

      <section class="detail__ingredients">
        <h2>Ingredientes</h2>
        <ul>
          <li v-for="ingredient in pizza.ingredients" :key="ingredient">
            {{ ingredient }}
          </li>
        </ul>
      </section>

      <div class="detail__footer">
        <div class="detail__price">{{ pizza.price.toFixed(2) }} €</div>
        <button class="detail__order" type="button">Añadir al carrito</button>
      </div>

      <p v-if="isOrder" class="detail__order-hint">
        Estás a punto de pedir <strong>{{ pizza.name }}</strong>. Conecta aquí tu checkout real.
      </p>
    </article>

    <article v-else class="detail__content">
      <h1 class="detail__title">Pizza no encontrada</h1>
      <p>La pizza solicitada no existe en el catálogo.</p>
    </article>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { pizzas } from '@/data/pizzas.js'

const props = defineProps({
  slug: { type: String, required: true },
})

const route = useRoute()
const pizza = computed(() => pizzas.find((p) => p.slug === props.slug))
const isOrder = computed(() => route.query.action === 'order')
</script>

<style scoped>
.detail {
  min-height: 100vh;
  padding: 110px 36px 80px;
  max-width: 880px;
  margin: 0 auto;
  color: var(--ink-100);
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%, #1d1209 0%, transparent 60%);
}

.detail__back {
  display: inline-block;
  font-size: 12px;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--ink-300);
  opacity: 0.85;
}
.detail__back:hover {
  opacity: 1;
}

.detail__content {
  margin-top: 40px;
}

.detail__eyebrow {
  font-size: 11px;
  letter-spacing: 0.32em;
  text-transform: uppercase;
  color: var(--ink-300);
  margin: 0 0 14px;
}

.detail__title {
  font-family: var(--font-serif);
  font-size: clamp(48px, 8vw, 96px);
  margin: 0;
  line-height: 1;
  letter-spacing: 0.005em;
}

.detail__desc {
  margin: 24px 0 40px;
  font-size: 18px;
  line-height: 1.6;
  max-width: 640px;
  color: rgba(244, 235, 217, 0.8);
}

.detail__ingredients h2 {
  font-family: var(--font-serif);
  font-size: 22px;
  color: var(--ink-300);
  font-weight: 500;
  margin: 0 0 12px;
  letter-spacing: 0.04em;
}
.detail__ingredients ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px 10px;
}
.detail__ingredients li {
  padding: 7px 14px;
  border: 1px solid rgba(244, 235, 217, 0.18);
  border-radius: 999px;
  font-size: 13px;
  letter-spacing: 0.04em;
}

.detail__footer {
  margin-top: 56px;
  display: flex;
  align-items: center;
  gap: 28px;
  flex-wrap: wrap;
}
.detail__price {
  font-family: var(--font-serif);
  font-size: 42px;
  color: var(--ink-300);
}
.detail__order {
  padding: 14px 28px;
  font-size: 12px;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  border-radius: 999px;
  border: none;
  background: linear-gradient(180deg, #d9a55a, #a87429);
  color: #1a0f07;
  font-weight: 600;
  cursor: pointer;
  transition: transform 200ms ease, box-shadow 200ms ease;
}
.detail__order:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 40px rgba(168, 116, 41, 0.4);
}

.detail__order-hint {
  margin-top: 24px;
  font-size: 13px;
  color: rgba(244, 235, 217, 0.6);
}
</style>
