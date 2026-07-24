<script setup>
defineProps({
  categories: { type: Array, required: true },
  active: { type: String, required: true },
})

defineEmits(['select'])
</script>

<template>
  <div class="flex gap-2 overflow-x-auto pb-1 -mx-4 px-4 sm:mx-0 sm:px-0">
    <button
      v-for="category in categories"
      :key="category.id"
      type="button"
      class="shrink-0 px-4 py-2 rounded-full font-medium text-sm border transition"
      :class="
        active === category.id
          ? 'bg-brand-red text-white border-brand-red'
          : 'bg-brand-card text-brand-text-soft border-brand-border hover:border-brand-red hover:text-brand-red'
      "
      @click="$emit('select', category.id)"
    >
      {{ category.label }}
    </button>
  </div>
</template>
