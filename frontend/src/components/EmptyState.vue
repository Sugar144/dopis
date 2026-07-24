<script setup>
defineProps({
  title: { type: String, required: true },
  message: { type: String, default: '' },
  icon: { type: String, default: '🍕' },
})
</script>

<template>
  <div class="flex flex-col items-center justify-center text-center py-12 px-4">
    <span class="text-5xl mb-3">{{ icon }}</span>
    <p class="font-display font-semibold text-lg text-brand-text">{{ title }}</p>
    <p v-if="message" class="text-brand-text-soft mt-1 max-w-xs">{{ message }}</p>
    <div class="mt-4">
      <slot />
    </div>
  </div>
</template>
