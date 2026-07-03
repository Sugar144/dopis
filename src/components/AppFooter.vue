<script setup>
// Enlace a Instagram con placeholder. TODO: sustituir por la URL real de Dopis.
const instagramUrl = '#'
</script>

<template>
  <footer class="border-t border-brand-border bg-brand-card mt-16">
    <div class="max-w-5xl mx-auto px-4 py-8 grid gap-6 sm:grid-cols-3 text-sm">
      <div>
        <p class="font-display font-bold text-brand-text mb-1">Dopis</p>
        <p class="text-brand-text-soft">Les Planes, Sant Cugat</p>
        <p class="text-brand-text-soft">Abierto hoy · 19:00 - 23:00</p>
      </div>

      <div>
        <p class="font-semibold text-brand-text mb-1">Recogida en local</p>
        <p class="text-brand-text-soft">Solo recogida. No hacemos reparto a domicilio.</p>
      </div>

      <div class="sm:text-right">
        <a
          :href="instagramUrl"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 text-brand-red font-medium hover:text-brand-red-dark transition"
        >
          @dopis.pizzeria
        </a>
        <p class="text-brand-text-soft mt-1">Síguenos en Instagram</p>
      </div>
    </div>
    <p class="text-center text-xs text-brand-text-soft/70 pb-6">
      Demo funcional · Dopis © {{ new Date().getFullYear() }}
    </p>
  </footer>
</template>
