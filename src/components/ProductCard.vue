<script setup>
import { computed } from 'vue'
import BaseButton from './BaseButton.vue'
import { useCart } from '../composables/useCart'

const props = defineProps({
  product: { type: Object, required: true },
})

const { items, addItem, increment, decrement } = useCart()

const cartItem = computed(() =>
  items.value.find((item) => item.id === props.product.id),
)

const qty = computed(() => cartItem.value?.qty ?? 0)

function handleAdd() {
  addItem(props.product)
}
</script>

<template>
  <div
    class="bg-brand-card rounded-2xl border border-brand-border p-4 flex flex-col gap-3 shadow-sm"
  >
    <div>
      <p class="font-display font-semibold text-brand-text text-lg leading-tight">
        {{ product.name }}
      </p>
      <p class="text-brand-text-soft text-sm mt-1">{{ product.description }}</p>
    </div>

    <div class="mt-auto flex items-center justify-between pt-2">
      <span class="font-semibold text-brand-text">{{ product.price.toFixed(2) }} €</span>

      <BaseButton v-if="qty === 0" variant="secondary" class="!px-4 !py-2 text-sm" @click="handleAdd">
        Añadir
      </BaseButton>

      <div v-else class="flex items-center gap-3 bg-brand-beige rounded-full px-1 py-1">
        <button
          type="button"
          aria-label="Quitar una unidad"
          class="w-8 h-8 rounded-full bg-white text-brand-red font-bold text-lg leading-none flex items-center justify-center active:scale-95 transition"
          @click="decrement(product.id)"
        >
          −
        </button>
        <span class="w-4 text-center font-semibold">{{ qty }}</span>
        <button
          type="button"
          aria-label="Añadir una unidad"
          class="w-8 h-8 rounded-full bg-brand-red text-white font-bold text-lg leading-none flex items-center justify-center active:scale-95 transition"
          @click="increment(product.id)"
        >
          +
        </button>
      </div>
    </div>
  </div>
</template>
