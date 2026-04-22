/*
  Mock catalogue. Keep the shape stable — the detail view, carousel and
  box-accent glow all read from here. Replace `image` with real product
  photos (1:1, transparent PNG ideally, min ~1000px).
*/
export const pizzas = [
  {
    id: 1,
    slug: 'margherita-dop',
    name: 'Margherita DOP',
    tagline: 'La esencia napolitana',
    description:
      'Tomate San Marzano DOP, mozzarella di bufala campana, albahaca fresca y un hilo de aceite de oliva virgen extra.',
    price: 12.5,
    accent: '#c94d3a',
    ingredients: [
      'Tomate San Marzano DOP',
      'Mozzarella di bufala campana',
      'Albahaca fresca',
      'Aceite de oliva virgen extra',
      'Sal marina',
    ],
    image: null, // TODO: sustituir por foto del producto (1:1)
  },
  {
    id: 2,
    slug: 'diavola',
    name: 'Diavola',
    tagline: 'Picante con carácter',
    description:
      'Salami picante italiano, mozzarella fior di latte, tomate San Marzano y un toque de chile fresco.',
    price: 13.9,
    accent: '#d94b2b',
    ingredients: [
      'Salami picante',
      'Mozzarella fior di latte',
      'Tomate San Marzano',
      'Chile fresco',
      'Orégano',
    ],
    image: null,
  },
  {
    id: 3,
    slug: 'tartufo-nero',
    name: 'Tartufo Nero',
    tagline: 'Gourmet en cada bocado',
    description:
      'Crema de trufa negra, mozzarella, champiñones portobello salteados, parmigiano reggiano 24 meses y rúcula fresca.',
    price: 16.9,
    accent: '#a07c4a',
    ingredients: [
      'Crema de trufa negra',
      'Mozzarella',
      'Portobello salteado',
      'Parmigiano Reggiano 24 meses',
      'Rúcula',
    ],
    image: null,
  },
  {
    id: 4,
    slug: 'quattro-formaggi',
    name: 'Quattro Formaggi',
    tagline: 'Cremosa y reconfortante',
    description:
      'Mozzarella fior di latte, gorgonzola DOP, parmigiano reggiano y scamorza ahumada, terminada con miel de flores.',
    price: 14.5,
    accent: '#e0a653',
    ingredients: [
      'Mozzarella fior di latte',
      'Gorgonzola DOP',
      'Parmigiano Reggiano',
      'Scamorza ahumada',
      'Miel de flores',
    ],
    image: null,
  },
  {
    id: 5,
    slug: 'prosciutto-funghi',
    name: 'Prosciutto e Funghi',
    tagline: 'Clásica reinventada',
    description:
      'Prosciutto cotto de alta calidad, mezcla de setas de temporada, mozzarella, tomate y tomillo fresco.',
    price: 13.5,
    accent: '#b85450',
    ingredients: [
      'Prosciutto cotto',
      'Setas de temporada',
      'Mozzarella',
      'Tomate',
      'Tomillo',
    ],
    image: null,
  },
  {
    id: 6,
    slug: 'vegetale-orto',
    name: "Vegetale dell'Orto",
    tagline: 'El huerto en tu mesa',
    description:
      'Calabacín, berenjena asada, pimiento rojo, cebolla roja caramelizada, mozzarella y albahaca fresca.',
    price: 13.2,
    accent: '#7a9a58',
    ingredients: [
      'Calabacín',
      'Berenjena asada',
      'Pimiento rojo',
      'Cebolla caramelizada',
      'Mozzarella',
      'Albahaca',
    ],
    image: null,
  },
]
