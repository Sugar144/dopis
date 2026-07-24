<script setup>
import { useCart } from '../composables/useCart'

defineEmits(['open'])

const { totalUnits, totalPrice, isEmpty } = useCart()
</script>

<template>
  <Transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="!isEmpty"
      class="fixed bottom-0 left-0 right-0 z-40 p-3 sm:p-4"
    >
      <button
        type="button"
        class="max-w-5xl mx-auto w-full flex items-center justify-between gap-3 bg-brand-red text-white rounded-2xl px-5 py-4 shadow-lg active:scale-[0.99] transition"
        @click="$emit('open')"
      >
        <span class="flex items-center gap-2 font-semibold">
          <span class="bg-white/20 rounded-full w-7 h-7 flex items-center justify-center text-sm">
            {{ totalUnits }}
          </span>
          Ver pedido
        </span>
        <span class="font-bold">{{ totalPrice.toFixed(2) }} €</span>
      </button>
    </div>
  </Transition>
</template>
