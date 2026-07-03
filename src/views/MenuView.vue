<script setup>
import { ref, computed } from 'vue'
import { categories, products, upsellDrinkIds, upsellDessertIds } from '../data/products'
import { useCart } from '../composables/useCart'
import CategoryTabs from '../components/CategoryTabs.vue'
import ProductCard from '../components/ProductCard.vue'
import CartBar from '../components/CartBar.vue'
import CartDrawer from '../components/CartDrawer.vue'

const activeCategory = ref('pizzas')
const drawerOpen = ref(false)

const { hasPizza, items } = useCart()

const visibleProducts = computed(() =>
  products.filter((product) => product.category === activeCategory.value),
)

const upsellProducts = computed(() => {
  const suggestedIds = [...upsellDrinkIds, ...upsellDessertIds]
  const cartIds = new Set(items.value.map((item) => item.id))
  return products
    .filter((product) => suggestedIds.includes(product.id) && !cartIds.has(product.id))
    .slice(0, 3)
})

const showUpsell = computed(
  () => activeCategory.value === 'pizzas' && hasPizza.value && upsellProducts.value.length > 0,
)
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-6 pb-32">
    <h1 class="font-display font-extrabold text-2xl sm:text-3xl text-brand-text mb-4">Nuestra carta</h1>

    <CategoryTabs :categories="categories" :active="activeCategory" @select="activeCategory = $event" />

    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 mt-6">
      <ProductCard v-for="product in visibleProducts" :key="product.id" :product="product" />
    </div>

    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
    >
      <div v-if="showUpsell" class="mt-8 bg-brand-beige/60 border border-brand-border rounded-2xl p-5">
        <p class="font-display font-semibold text-brand-text">¿Quieres añadir bebida o postre? 😊</p>
        <p class="text-brand-text-soft text-sm mt-1 mb-4">Un buen acompañamiento para tu pizza.</p>
        <div class="grid gap-3 sm:grid-cols-3">
          <ProductCard v-for="product in upsellProducts" :key="product.id" :product="product" />
        </div>
      </div>
    </Transition>

    <CartBar @open="drawerOpen = true" />
    <CartDrawer :open="drawerOpen" @close="drawerOpen = false" />
  </div>
</template>
