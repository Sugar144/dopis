<script setup>
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'
import OrderSummary from './OrderSummary.vue'
import BaseButton from './BaseButton.vue'
import EmptyState from './EmptyState.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const router = useRouter()
const { items, totalPrice, increment, decrement, removeItem, isEmpty } = useCart()

function goToCheckout() {
  emit('close')
  router.push('/checkout')
}
</script>

<template>
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="open" class="fixed inset-0 z-50 flex justify-end">
      <div class="absolute inset-0 bg-black/40" @click="$emit('close')" />

      <Transition
        appear
        enter-active-class="transition duration-250 ease-out"
        enter-from-class="translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="translate-x-full"
      >
        <div
          v-if="open"
          class="relative bg-brand-background w-full sm:max-w-md h-full flex flex-col shadow-xl"
        >
          <div class="flex items-center justify-between px-5 py-4 border-b border-brand-border">
            <h2 class="font-display font-bold text-lg text-brand-text">Tu pedido</h2>
            <button
              type="button"
              aria-label="Cerrar"
              class="w-9 h-9 rounded-full hover:bg-brand-beige flex items-center justify-center text-xl"
              @click="$emit('close')"
            >
              ✕
            </button>
          </div>

          <div class="flex-1 overflow-y-auto px-5 py-4">
            <EmptyState
              v-if="isEmpty"
              icon="🛒"
              title="Tu pedido está vacío"
              message="Añade alguna pizza, bebida o postre desde la carta."
            />
            <OrderSummary
              v-else
              :items="items"
              :total="totalPrice"
              editable
              @increment="increment"
              @decrement="decrement"
              @remove="removeItem"
            />
          </div>

          <div class="px-5 py-4 border-t border-brand-border bg-brand-card">
            <p class="text-sm text-brand-text-soft text-center mb-3">
              Solo recogida en local. No hacemos reparto a domicilio.
            </p>
            <BaseButton
              class="w-full"
              :disabled="isEmpty"
              @click="goToCheckout"
            >
              Continuar pedido
            </BaseButton>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
