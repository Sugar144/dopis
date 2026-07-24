<script setup>
import { mockOrders } from '../data/mockOrders'
import OwnerOrderCard from '../components/OwnerOrderCard.vue'
import EmptyState from '../components/EmptyState.vue'

function handleUpdateStatus({ id, status }) {
  const order = mockOrders.find((o) => o.id === id)
  if (order) order.status = status
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="font-display font-extrabold text-2xl sm:text-3xl text-brand-text mb-2">Pedidos de hoy</h1>
    <p class="inline-block bg-amber-100 text-amber-800 text-sm font-medium rounded-full px-3 py-1.5 mb-6">
      ⚠️ Panel de demostración — datos ficticios
    </p>

    <!-- TODO: cuando exista backend, sustituir mockOrders por pedidos reales en
    tiempo real y avisar a Jaime con notificación/sonido al entrar un pedido nuevo. -->

    <div v-if="mockOrders.length" class="grid gap-4 sm:grid-cols-2">
      <OwnerOrderCard
        v-for="order in mockOrders"
        :key="order.id"
        :order="order"
        @update-status="handleUpdateStatus"
      />
    </div>

    <EmptyState v-else icon="📋" title="No hay pedidos por ahora" />
  </div>
</template>
