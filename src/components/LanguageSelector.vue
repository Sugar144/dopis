<script setup>
import { ref } from 'vue'

// Selector visual ES / CA / EN. No hace traducción real todavía.
// TODO: conectar a un sistema de i18n real (vue-i18n) cuando haya contenido multidioma.
const languages = ['ES', 'CA', 'EN']
const active = ref('ES')

function select(lang) {
  active.value = lang
}
</script>

<template>
  <div class="inline-flex items-center gap-1 rounded-full bg-brand-card border border-brand-border p-1 text-sm">
    <button
      v-for="lang in languages"
      :key="lang"
      type="button"
      class="px-2.5 py-1 rounded-full font-medium transition"
      :class="active === lang ? 'bg-brand-red text-white' : 'text-brand-text-soft hover:bg-brand-beige'"
      @click="select(lang)"
    >
      {{ lang }}
    </button>
  </div>
</template>
