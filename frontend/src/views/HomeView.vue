<script setup>
import { RouterLink } from 'vue-router'
import BaseButton from '../components/BaseButton.vue'
import mascot from '../assets/brand/logo-mascot.png'

const benefits = [
  { icon: '🏠', title: 'Recogida en local', text: 'Pasa por Dopis y recoge tu pedido ya listo.' },
  { icon: '⚡', title: 'Pedido rápido sin llamar', text: 'Pide desde el móvil en menos de un minuto.' },
  { icon: '💳', title: 'Pago online o en local', text: 'Elige la opción que te resulte más cómoda.' },
]

// TODO: sustituir por la URL real de Instagram de Dopis.
const instagramUrl = '#'
</script>

<template>
  <div>
    <section class="max-w-5xl mx-auto px-4 pt-8 pb-12 sm:pt-14 grid gap-8 sm:grid-cols-2 sm:items-center">
      <div class="order-2 sm:order-1 text-center sm:text-left">
        <h1 class="font-display font-extrabold text-3xl sm:text-4xl leading-tight text-brand-text">
          Pide tu pizza online y recógela en el local
        </h1>
        <p class="text-brand-text-soft mt-4 text-lg">
          Haz tu pedido desde el móvil y ven a recogerlo cuando esté listo.
        </p>

        <div class="mt-6 flex flex-col sm:flex-row gap-3 justify-center sm:justify-start">
          <RouterLink to="/carta">
            <BaseButton class="w-full sm:w-auto">Ver carta</BaseButton>
          </RouterLink>
          <RouterLink to="/panel">
            <BaseButton variant="secondary" class="w-full sm:w-auto">Ver panel demo</BaseButton>
          </RouterLink>
        </div>

        <div class="mt-8 flex flex-col items-center sm:items-start gap-1 text-sm text-brand-text-soft">
          <p>📍 Les Planes, Sant Cugat</p>
          <p>🕗 Abierto hoy · 19:00 - 23:00</p>
          <a :href="instagramUrl" target="_blank" rel="noopener" class="text-brand-red font-medium hover:text-brand-red-dark">
            📷 Síguenos en Instagram
          </a>
        </div>
      </div>

      <div class="order-1 sm:order-2 flex justify-center">
        <img :src="mascot" alt="Dopis" class="w-48 sm:w-72 h-auto drop-shadow-sm" />
      </div>
    </section>

    <section class="bg-brand-card border-y border-brand-border">
      <div class="max-w-5xl mx-auto px-4 py-10 grid gap-6 sm:grid-cols-3">
        <div v-for="benefit in benefits" :key="benefit.title" class="text-center sm:text-left">
          <span class="text-3xl">{{ benefit.icon }}</span>
          <p class="font-display font-bold text-brand-text mt-2">{{ benefit.title }}</p>
          <p class="text-brand-text-soft text-sm mt-1">{{ benefit.text }}</p>
        </div>
      </div>
    </section>

    <section class="max-w-5xl mx-auto px-4 py-12 text-center">
      <p class="font-display font-bold text-2xl text-brand-text">¿Ya sabes lo que quieres?</p>
      <p class="text-brand-text-soft mt-2">Echa un vistazo a la carta y pide en un momento.</p>
      <RouterLink to="/carta">
        <BaseButton class="mt-5">Ver carta</BaseButton>
      </RouterLink>
    </section>
  </div>
</template>
