import { reactive, computed } from 'vue'

// Estado del carrito compartido en toda la app mientras dura la sesión del navegador.
// TODO: cuando haya backend, sustituir este estado en memoria por persistencia real
// (localStorage como mínimo, o pedido en servidor) para que sobreviva a recargas.
const state = reactive({
  items: [], // { id, name, price, qty, category }
  lastOrder: null, // pedido mock creado en checkout, usado en la confirmación
})

function addItem(product) {
  const existing = state.items.find((item) => item.id === product.id)
  if (existing) {
    existing.qty += 1
  } else {
    state.items.push({
      id: product.id,
      name: product.name,
      price: product.price,
      category: product.category,
      qty: 1,
    })
  }
}

function removeItem(id) {
  state.items = state.items.filter((item) => item.id !== id)
}

function increment(id) {
  const item = state.items.find((i) => i.id === id)
  if (item) item.qty += 1
}

function decrement(id) {
  const item = state.items.find((i) => i.id === id)
  if (!item) return
  if (item.qty <= 1) {
    removeItem(id)
  } else {
    item.qty -= 1
  }
}

function clearCart() {
  state.items = []
}

function setLastOrder(order) {
  state.lastOrder = order
}

const totalUnits = computed(() =>
  state.items.reduce((sum, item) => sum + item.qty, 0),
)

const totalPrice = computed(() =>
  state.items.reduce((sum, item) => sum + item.qty * item.price, 0),
)

const isEmpty = computed(() => state.items.length === 0)

const hasPizza = computed(() =>
  state.items.some((item) => item.category === 'pizzas'),
)

export function useCart() {
  return {
    items: computed(() => state.items),
    lastOrder: computed(() => state.lastOrder),
    totalUnits,
    totalPrice,
    isEmpty,
    hasPizza,
    addItem,
    removeItem,
    increment,
    decrement,
    clearCart,
    setLastOrder,
  }
}
