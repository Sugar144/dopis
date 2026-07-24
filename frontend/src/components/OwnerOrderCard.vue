<script setup>
import { orderStatuses } from '../data/mockOrders'

const props = defineProps({
  order: { type: Object, required: true },
})

const emit = defineEmits(['update-status'])

const statusStyles = {
  Nuevo: 'bg-brand-red text-white',
  'En preparación': 'bg-amber-500 text-white',
  'Listo para recoger': 'bg-emerald-600 text-white',
}

function nextStatus() {
  const currentIndex = orderStatuses.indexOf(props.order.status)
  const next = orderStatuses[currentIndex + 1]
  if (next) emit('update-status', { id: props.order.id, status: next })
}
</script>

<template>
  <div class="bg-brand-card border border-brand-border rounded-2xl p-5 flex flex-col gap-4 shadow-sm">
    <div class="flex items-start justify-between gap-3">
      <div>
        <p class="font-display font-bold text-lg text-brand-text">{{ order.id }}</p>
        <p class="text-brand-text-soft text-sm">{{ order.time }} · {{ order.customerName }}</p>
      </div>
      <span
        class="text-xs font-semibold px-3 py-1.5 rounded-full whitespace-nowrap"
        :class="statusStyles[order.status]"
      >
        {{ order.status }}
      </span>
    </div>

    <ul class="text-sm text-brand-text flex flex-col gap-1">
      <li v-for="(item, index) in order.items" :key="index">
        {{ item.qty }}× {{ item.name }}
      </li>
    </ul>

    <div class="flex items-center justify-between text-sm">
      <span class="text-brand-text-soft">{{ order.paymentMethod }}</span>
      <span class="font-bold text-brand-text text-base">{{ order.total.toFixed(2) }} €</span>
    </div>

    <div class="grid gap-2" :class="orderStatuses.indexOf(order.status) < orderStatuses.length - 1 ? 'grid-cols-1' : ''">
      <button
        v-if="orderStatuses.indexOf(order.status) < orderStatuses.length - 1"
        type="button"
        class="w-full rounded-xl bg-brand-red text-white font-semibold py-3.5 text-base active:scale-[0.98] transition"
        @click="nextStatus"
      >
        Marcar como "{{ orderStatuses[orderStatuses.indexOf(order.status) + 1] }}"
      </button>
      <p v-else class="text-center text-emerald-700 font-semibold py-2">
        Pedido listo ✓
      </p>
    </div>
  </div>
</template>
