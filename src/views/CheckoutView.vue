<script setup>
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'
import { createMockOrder } from '../data/mockOrders'
import CheckoutForm from '../components/CheckoutForm.vue'
import OrderSummary from '../components/OrderSummary.vue'

const router = useRouter()
const { items, totalPrice, isEmpty, clearCart, setLastOrder } = useCart()

function handleConfirm(formData) {
  // TODO: cuando exista backend, enviar el pedido al servidor en lugar de
  // guardarlo solo en memoria del navegador.
  const order = createMockOrder({
    customerName: formData.name,
    items: items.value,
    total: totalPrice.value,
    paymentMethod: formData.paymentMethod,
    pickupTime: formData.pickupTime,
  })

  setLastOrder({
    ...order,
    phone: formData.phone,
    note: formData.note,
  })

  clearCart()
  router.push('/confirmacion')
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="font-display font-extrabold text-2xl sm:text-3xl text-brand-text mb-6">Finalizar pedido</h1>

    <div class="grid gap-8 sm:grid-cols-2">
      <CheckoutForm :cart-is-empty="isEmpty" @confirm="handleConfirm" />

      <div class="bg-brand-card border border-brand-border rounded-2xl p-5 h-fit order-first sm:order-last">
        <p class="font-display font-semibold text-brand-text mb-3">Resumen del pedido</p>
        <OrderSummary v-if="!isEmpty" :items="items" :total="totalPrice" />
        <p v-else class="text-brand-text-soft text-sm">Tu pedido está vacío.</p>
      </div>
    </div>
  </div>
</template>
