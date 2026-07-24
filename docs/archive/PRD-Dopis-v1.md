> **Status:** SUPERSEDED — retained for historical reference
>
> This document describes the initial product scope. Current MVP technical
> decisions are governed by `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`.

---

# PRD — Web Dopis

> Web de pedidos online con recogida en local para una pizzería de barrio en Les Planes de Sant Cugat, optimizada para móvil.

**Fecha:** 2026-06-04
**Versión:** 1.0 (MVP)
**Tipo:** Producto nuevo
**Perfil del interlocutor:** No técnico
**Estado:** Borrador para validación técnica

---

## 1. Visión y objetivos

### 1.1 Problema

El dueño gestiona todos los pedidos por teléfono o en persona. En momentos punta (viernes y sábado por la noche, o cuando está solo en cocina) no puede atender el teléfono y cocinar a la vez. Hay clientes potenciales que no llaman porque prefieren pedir online.

### 1.2 Propuesta de valor

Una web sencilla desde el móvil donde el cliente elige su pedido, paga si quiere, y solo tiene que aparecer a recogerlo. Para el dueño: menos teléfono, más pedidos, y datos de clientes para fidelizarlos.

### 1.3 Objetivos del MVP

- Permitir pedidos online con recogida en local
- Mostrar la carta completa con pizzas, extras, postres, café y bebidas
- Ofrecer pago online (tarjeta, Apple Pay) y opción de pagar en local
- Registrar clientes para futuras campañas u ofertas
- Ser operable por el dueño sin conocimientos técnicos

### 1.4 Fuera de alcance (YAGNI)

- Reparto a domicilio
- Reserva de mesas
- Blog o contenido editorial
- App nativa
- Cualquier canal que no sea recogida en local

---

## 2. Usuarios y casos de uso

### 2.1 Perfiles

| Perfil | Descripción |
|---|---|
| Cliente habitual | Vecino del barrio o alrededores, conoce Dopis, pide desde el móvil |
| Cliente nuevo | Descubre Dopis, quiere explorar la carta y pedir sin llamar |
| Jaime (dueño) | Gestiona la web, consulta pedidos entrantes, accede a datos de clientes |

### 2.2 Casos de uso

| ID | Caso de uso |
|---|---|
| CU-01 | Cliente consulta la carta desde el móvil |
| CU-02 | Cliente selecciona pizzas, cantidades y extras |
| CU-03 | Cliente elige método de pago (online o en local) |
| CU-04 | Cliente recibe confirmación del pedido |
| CU-05 | Cliente se registra o identifica para acumular historial |
| CU-06 | Jaime recibe notificación de pedido nuevo |
| CU-07 | Jaime consulta pedidos del día |
| CU-08 | Jaime consulta datos y frecuencia de clientes registrados |
| CU-09 | Jaime envía oferta o comunicación a clientes registrados |

---

## 3. Funcionalidades del MVP

- **F1** — Carta digital con categorías: pizzas, postres, café (solo mañanas), bebidas
- **F2** — Selector de cantidad por producto
- **F3** — Flujo de upsell: al acabar de elegir pizzas, ofrecer extras (postres, bebidas, café)
- **F4** — Pasarela de pago online: tarjeta y Apple Pay (Google Pay pendiente confirmar)
- **F5** — Opción de pagar en local al recoger
- **F6** — Confirmación de pedido al cliente (pantalla + notificación, canal a definir)
- **F7** — Panel para el dueño: pedidos entrantes en tiempo real
- **F8** — Registro de clientes (nombre, contacto, historial de pedidos)
- **F9** — Herramienta básica para enviar ofertas a clientes registrados
- **F10** — Enlace a Instagram visible en la web
- **F11** — Web en tres idiomas: castellano, catalán, inglés

---

## 4. Restricciones de negocio

- **Plazo:** cuanto antes, sin fecha dura
- **Presupuesto:** no confirmado (pendiente)
- **Idiomas:** castellano, catalán, inglés
- **Marca:** logo y paleta de colores ya existentes, el dueño los facilita
- **Legal/privacidad:** recogida de datos de clientes → cumplimiento RGPD necesario (parking lot técnico)
- **Decisor:** Jaime (único)
- **Volumen esperado:** negocio de barrio; picos claros viernes y sábado noche
- **Dispositivo principal:** móvil

---

## 5. Sistema existente

*No aplica — producto nuevo.*

---

## 6. Métricas de éxito

- Reducción de llamadas recibidas los viernes y sábados por la noche
- Incremento de pedidos totales respecto a la media actual
- Número de clientes nuevos registrados
- Frecuencia de repetición de clientes registrados
- Cero incidencias de pago no recibido por el dueño

---

## 7. Riesgos

| Riesgo | Impacto | Mitigación propuesta |
|---|---|---|
| El dueño no sabe manejar el panel de gestión | Pedidos perdidos o no vistos a tiempo | Panel muy simple; formación breve al entregar; soporte accesible |
| La web falla en hora punta (viernes/sábado noche) | Pedidos perdidos, mala imagen | Fiabilidad como requisito no funcional crítico; alertas ante caída |
| Desincronización entre pago online y pedido recibido | Cliente pagó pero el dueño no lo ve; reclamaciones | Integración de pago con confirmación en tiempo real; log de transacciones |

---

## 8. Supuestos y preguntas abiertas

### Supuestos

- Los clientes recogen siempre en local; no hay reparto ahora ni en el futuro próximo
- El dueño gestiona la web solo, sin equipo técnico propio
- El café solo se ofrece en horario de mañana (lógica de horario a implementar)
- Google Pay incluido junto a Apple Pay (pendiente confirmar con Jaime)

### Preguntas abiertas

- ¿Cuál es el horario de apertura y los días que abre Dopis?
- ¿Hay un horario diferente para el café de mañana?
- ¿Jaime quiere gestionar la carta (añadir/quitar productos, cambiar precios) él mismo, o lo hace el programador cuando haga falta?
- ¿Cómo quiere Jaime recibir el aviso de pedido nuevo? (sonido en el local, móvil, tablet…)
- ¿Presupuesto disponible?
- ¿Dominio propio ya comprado o hay que gestionarlo?
