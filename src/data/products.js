// Datos mock de la carta. TODO: cuando exista backend, sustituir por una
// gestión real de carta (panel de administración conectado a base de datos).
export const categories = [
  { id: 'pizzas', label: 'Pizzas' },
  { id: 'bebidas', label: 'Bebidas' },
  { id: 'postres', label: 'Postres' },
  { id: 'cafe', label: 'Café' },
]

export const products = [
  {
    id: 'pizza-margarita',
    category: 'pizzas',
    name: 'Margarita',
    description: 'Tomate, mozzarella y albahaca',
    price: 8.5,
  },
  {
    id: 'pizza-prosciutto',
    category: 'pizzas',
    name: 'Prosciutto',
    description: 'Tomate, mozzarella y jamón cocido',
    price: 9.5,
  },
  {
    id: 'pizza-diavola',
    category: 'pizzas',
    name: 'Diavola',
    description: 'Tomate, mozzarella y salami picante',
    price: 10.5,
  },
  {
    id: 'pizza-quattro-formaggi',
    category: 'pizzas',
    name: 'Quattro Formaggi',
    description: 'Mezcla de cuatro quesos',
    price: 11.0,
  },
  {
    id: 'pizza-vegetal',
    category: 'pizzas',
    name: 'Vegetal',
    description: 'Verduras de temporada y mozzarella',
    price: 10.0,
  },
  {
    id: 'bebida-agua',
    category: 'bebidas',
    name: 'Agua',
    description: 'Botella de agua mineral',
    price: 1.5,
  },
  {
    id: 'bebida-cocacola',
    category: 'bebidas',
    name: 'Coca-Cola',
    description: 'Lata 33 cl',
    price: 2.2,
  },
  {
    id: 'bebida-fanta',
    category: 'bebidas',
    name: 'Fanta',
    description: 'Lata 33 cl',
    price: 2.2,
  },
  {
    id: 'bebida-cerveza-sa',
    category: 'bebidas',
    name: 'Cerveza sin alcohol',
    description: 'Botella 33 cl',
    price: 2.5,
  },
  {
    id: 'postre-tiramisu',
    category: 'postres',
    name: 'Tiramisú',
    description: 'Receta casera de la casa',
    price: 4.5,
  },
  {
    id: 'postre-cheesecake',
    category: 'postres',
    name: 'Cheesecake',
    description: 'Tarta de queso con coulis de frutos rojos',
    price: 4.5,
  },
  {
    id: 'cafe-solo',
    category: 'cafe',
    name: 'Café solo',
    description: 'Espresso',
    price: 1.4,
  },
  {
    id: 'cafe-cortado',
    category: 'cafe',
    name: 'Cortado',
    description: 'Espresso con un toque de leche',
    price: 1.6,
  },
  {
    id: 'cafe-con-leche',
    category: 'cafe',
    name: 'Café con leche',
    description: 'Espresso con leche',
    price: 1.9,
  },
]

export const upsellDrinkIds = ['bebida-cocacola', 'bebida-agua', 'bebida-fanta']
export const upsellDessertIds = ['postre-tiramisu', 'postre-cheesecake']
