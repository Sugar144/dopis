<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary', // primary | secondary | ghost
  },
  type: {
    type: String,
    default: 'button',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['click'])

const base =
  'inline-flex items-center justify-center gap-2 rounded-full font-semibold px-6 py-3 text-base transition active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none'

const variants = {
  primary: 'bg-brand-red text-white shadow-sm hover:bg-brand-red-dark',
  secondary:
    'bg-brand-card text-brand-text border-2 border-brand-red hover:bg-brand-beige',
  ghost: 'bg-transparent text-brand-text-soft hover:bg-brand-beige',
}
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[base, variants[variant]]"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>
