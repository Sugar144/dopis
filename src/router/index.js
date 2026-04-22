import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      // Lazy-loaded so the hero bundle stays lean on first paint.
      path: '/pizza/:slug',
      name: 'pizza-detail',
      component: () => import('@/views/PizzaDetailView.vue'),
      props: true,
    },
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  },
})

export default router
