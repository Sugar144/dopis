import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
  },
  {
    path: '/carta',
    name: 'carta',
    component: () => import('../views/MenuView.vue'),
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: () => import('../views/CheckoutView.vue'),
  },
  {
    path: '/confirmacion',
    name: 'confirmacion',
    component: () => import('../views/ConfirmationView.vue'),
  },
  {
    path: '/panel',
    name: 'panel',
    component: () => import('../views/OwnerPanelView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
