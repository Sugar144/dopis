# Dopis — Demo de pedidos online

Demo funcional (frontend-only) de una web de pedidos online con recogida en local para
Dopis, pizzería de barrio en Les Planes, Sant Cugat. Pensada para validar estética,
flujo de pedido y facilidad de uso antes de construir un backend real.

## Stack

- Vue 3 + Vite
- Vue Router 4
- Tailwind CSS 4
- JavaScript (sin TypeScript)
- Datos mock en frontend, sin backend ni base de datos

## Cómo ejecutar

```bash
npm install
npm run dev
```

## Qué incluye

- **Home** (`/`) — presentación, beneficios, dirección y horario.
- **Carta** (`/carta`) — pizzas, bebidas, postres y café, con carrito sticky y upsell.
- **Checkout** (`/checkout`) — datos de contacto, hora de recogida, método de pago.
- **Confirmación** (`/confirmacion`) — resumen del pedido mock.
- **Panel del dueño** (`/panel`) — vista simple de pedidos entrantes con cambio de estado.

## Qué es mock / demo

- Productos y pedidos: datos estáticos en `src/data/`.
- Carrito: estado en memoria (`src/composables/useCart.js`), se pierde al recargar.
- Pagos: no hay pasarela real; "Pagar online" está marcado como demo.
- Panel del dueño: pedidos ficticios, sin conexión a backend.
- Idioma: selector ES/CA/EN solo visual, sin traducción funcional.

Los puntos de conexión futura (backend, persistencia, pagos reales, notificaciones,
gestión de carta, RGPD, i18n real) están marcados con `TODO` en el código.

## Marca

Los assets de marca originales (PDF del logo/cartel) están en `brand/`. El logo usado
en la app se extrajo de ahí y vive en `src/assets/brand/`.
