<script setup>
import { RouterLink } from 'vue-router'
import LanguageSelector from './LanguageSelector.vue'
import wordmark from '../assets/brand/logo-wordmark.png'
</script>

<template>
  <header class="sticky top-0 z-30 bg-brand-background/95 backdrop-blur border-b border-brand-border">
    <div class="max-w-5xl mx-auto flex items-center justify-between gap-3 px-4 py-3">
      <RouterLink to="/" class="flex items-center gap-2 shrink-0">
        <img :src="wordmark" alt="Dopis" class="h-8 w-auto" />
      </RouterLink>

      <nav class="hidden sm:flex items-center gap-6 text-sm font-medium text-brand-text-soft">
        <RouterLink to="/" class="hover:text-brand-red transition">Inicio</RouterLink>
        <RouterLink to="/carta" class="hover:text-brand-red transition">Carta</RouterLink>
        <RouterLink to="/panel" class="hover:text-brand-red transition">Panel del dueño</RouterLink>
      </nav>

      <LanguageSelector class="shrink-0" />
    </div>
  </header>
</template>
