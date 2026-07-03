<script setup>
import { RouterLink } from 'vue-router'
import { useCart } from '../composables/useCart'
import BaseButton from '../components/BaseButton.vue'
import EmptyState from '../components/EmptyState.vue'

const { lastOrder } = useCart()
</script>

<template>
  <div class="max-w-lg mx-auto px-4 py-10">
    <template v-if="lastOrder">
      <div class="text-center mb-6">
        <span class="text-5xl">🎉</span>
        <h1 class="font-display font-extrabold text-2xl sm:text-3xl text-brand-text mt-2">Pedido recibido</h1>
        <p class="text-brand-text-soft mt-1">Número de pedido <span class="font-semibold text-brand-text">{{ lastOrder.id }}</span></p>
      </div>

      <div class="bg-brand-card border border-brand-border rounded-2xl p-5 flex flex-col gap-4">
        <div class="flex flex-col gap-1 text-sm">
          <p v-for="(item, index) in lastOrder.items" :key="index" class="text-brand-text">
            {{ item.qty }}× {{ item.name }}
          </p>
        </div>

        <div class="border-t border-brand-border pt-3 flex items-center justify-between font-bold text-brand-text text-lg">
          <span>Total</span>
          <span>{{ lastOrder.total.toFixed(2) }} €</span>
        </div>

        <div class="grid grid-cols-2 gap-3 text-sm pt-2">
          <div>
            <p class="text-brand-text-soft">Hora estimada</p>
            <p class="font-semibold text-brand-text">{{ lastOrder.time }}</p>
          </div>
          <div>
            <p class="text-brand-text-soft">Pago</p>
            <p class="font-semibold text-brand-text">{{ lastOrder.paymentMethod }}</p>
          </div>
        </div>
      </div>

      <p class="text-center font-display font-semibold text-lg text-brand-red mt-6">
        Te esperamos en Dopis
      </p>

      <RouterLink to="/carta" class="block mt-6">
        <BaseButton class="w-full">Volver a la carta</BaseButton>
      </RouterLink>
    </template>

    <EmptyState
      v-else
      icon="🍕"
      title="Todavía no hay ningún pedido"
      message="Haz un pedido desde la carta para ver aquí la confirmación."
    >
      <RouterLink to="/carta">
        <BaseButton>Ver carta</BaseButton>
      </RouterLink>
    </EmptyState>
  </div>
</template>
