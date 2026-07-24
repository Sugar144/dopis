// Pedidos ficticios para el panel de demostración del dueño.
// TODO: cuando exista backend, sustituir por pedidos reales guardados en base de datos
// y por notificaciones al dueño (push, sonido, etc.) cuando entre un pedido nuevo.
import { reactive } from 'vue'

export const orderStatuses = ['Nuevo', 'En preparación', 'Listo para recoger']

export const mockOrders = reactive([
  {
    id: 'DOP-1038',
    time: '20:12',
    customerName: 'Marta Roig',
    items: [
      { name: 'Margarita', qty: 1 },
      { name: 'Coca-Cola', qty: 2 },
    ],
    total: 12.9,
    paymentMethod: 'Pagar en local',
    status: 'Listo para recoger',
  },
  {
    id: 'DOP-1039',
    time: '20:20',
    customerName: 'Toni Ferrer',
    items: [
      { name: 'Diavola', qty: 2 },
      { name: 'Tiramisú', qty: 1 },
    ],
    total: 25.5,
    paymentMethod: 'Pagar en local',
    status: 'En preparación',
  },
  {
    id: 'DOP-1040',
    time: '20:31',
    customerName: 'Núria Camps',
    items: [
      { name: 'Vegetal', qty: 1 },
      { name: 'Agua', qty: 1 },
      { name: 'Cheesecake', qty: 1 },
    ],
    total: 16.0,
    paymentMethod: 'Pagar online (demo)',
    status: 'Nuevo',
  },
  {
    id: 'DOP-1041',
    time: '20:38',
    customerName: 'Jordi Puig',
    items: [
      { name: 'Quattro Formaggi', qty: 1 },
      { name: 'Prosciutto', qty: 1 },
      { name: 'Fanta', qty: 2 },
    ],
    total: 25.4,
    paymentMethod: 'Pagar en local',
    status: 'Nuevo',
  },
])

let orderCounter = 1042

export function createMockOrder({ customerName, items, total, paymentMethod, pickupTime }) {
  const id = `DOP-${orderCounter}`
  orderCounter += 1
  const order = {
    id,
    time: pickupTime,
    customerName,
    items: items.map((item) => ({ name: item.name, qty: item.qty })),
    total,
    paymentMethod,
    status: 'Nuevo',
  }
  mockOrders.unshift(order)
  return order
}
