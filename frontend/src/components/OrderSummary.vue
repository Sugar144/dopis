<script setup>
defineProps({
  items: { type: Array, required: true }, // { name, price?, qty }
  total: { type: Number, required: true },
  editable: { type: Boolean, default: false },
})

defineEmits(['increment', 'decrement', 'remove'])
</script>

<template>
  <div class="flex flex-col gap-3">
    <div
      v-for="item in items"
      :key="item.id ?? item.name"
      class="flex items-center justify-between gap-3"
    >
      <div class="min-w-0">
        <p class="font-medium text-brand-text truncate">{{ item.name }}</p>
        <p v-if="item.price != null" class="text-brand-text-soft text-sm">
          {{ item.price.toFixed(2) }} € × {{ item.qty }}
        </p>
      </div>

      <div v-if="editable" class="flex items-center gap-2 shrink-0">
        <button
          type="button"
          aria-label="Quitar una unidad"
          class="w-7 h-7 rounded-full bg-brand-beige text-brand-red font-bold flex items-center justify-center"
          @click="$emit('decrement', item.id)"
        >
          −
        </button>
        <span class="w-4 text-center font-semibold text-sm">{{ item.qty }}</span>
        <button
          type="button"
          aria-label="Añadir una unidad"
          class="w-7 h-7 rounded-full bg-brand-beige text-brand-red font-bold flex items-center justify-center"
          @click="$emit('increment', item.id)"
        >
          +
        </button>
        <button
          type="button"
          class="text-xs text-brand-text-soft underline ml-1 hover:text-brand-red"
          @click="$emit('remove', item.id)"
        >
          Quitar
        </button>
      </div>
      <div v-else class="shrink-0 font-semibold text-brand-text">
        {{ (item.price * item.qty).toFixed(2) }} €
      </div>
    </div>

    <div class="border-t border-brand-border pt-3 flex items-center justify-between font-bold text-brand-text text-lg">
      <span>Total</span>
      <span>{{ total.toFixed(2) }} €</span>
    </div>
  </div>
</template>
