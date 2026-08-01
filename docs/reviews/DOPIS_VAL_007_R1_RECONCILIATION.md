# DOPIS-VAL-007-R1 — Veredicto de reconciliación (compacto)

## 1. Verificación

`Sugar144/dopis@6fef9a8002a45114c8c7f266b3d76a3d7ee5e626` (`main`) y `Sugar144/stakeholder-validation-portal@a1919e1f81fc3b7b98af0fafb8dce712df81f9bf` (ancestro de HEAD) verificados.

La identidad de la respuesta (`response.id`, `cycleId`, `cycleVersion`, `cycleSha256`, `stakeholderRef`, `status`) coincide exactamente con lo declarado.

* 89/89 items con respuesta 1:1.
* `needsDiscussionItems: 0`.
* Ambos JSON localizados en `~/Downloads`, fuera del repositorio y no modificados.

## 2. Veredicto ejecutivo

* `BUSINESS_DISCOVERY`: sustancialmente cerrado. Existe una petición clasificada `SCOPE_CHANGE` que requiere decisión del Owner.
* Jaime ratifica sustancialmente el modelo de negocio esencial: **63/89 `RATIFIED`**, incluida la ratificación final del conjunto.
* No se necesita otra ronda amplia de stakeholder validation.
* Sí se necesitan follow-ups focalizados y mínimos.
* Se requiere reconciliación canónica por el Owner antes de tratar los nuevos resultados como verdad del repositorio.
* `USE_CASE_AND_ARCHITECTURE_PLANNING`: puede avanzar de forma condicionada en los dominios ya estables, sin asumir como resueltos los asuntos abiertos.
* `IMPLEMENTATION_AUTHORITY`: no autorizada; sin cambios respecto al estado previo.
* `PILOT_READINESS`: no listo.
* `WITHOUT_JAIME_READINESS`: no listo.
* `PUBLIC_LAUNCH_READINESS`: no listo.

## 3. Recuento de disposiciones

| Disposition           |  Count |
| --------------------- | -----: |
| `RATIFIED`            |     63 |
| `EVIDENCE_PENDING`    |     15 |
| `RESOLVED_DELTA`      |      5 |
| `FOLLOW_UP_REQUIRED`  |      3 |
| `CALIBRATION_PENDING` |      2 |
| `SCOPE_CHANGE`        |      1 |
| **Total**             | **89** |

## 4. Registro de deltas materiales

### SCOPE_CHANGE

* `DVAL2-S01-C02` — Jaime pide **pedidos para otros días con recordatorios**. Entra en conflicto con `EXC-ADVANCE-ORDERS` y con la regla vigente de pedidos del primer MVP. No puede promocionarse a alcance aceptado sin decisión del Owner.

### FOLLOW_UP_REQUIRED

* `DVAL2-S02-C03` — Jaime responde **"No entiendo"** respecto al respaldo móvil. Afecta `FR-KITCHEN-004`, `SEC-KITCHEN-001` y `JV-ACCESS`. Requiere reformulación simple y nueva respuesta.

* `DVAL2-S07-C08` — Jaime pide poder **"invitar"** pedidos, es decir, entregarlos sin cobrar. La cuestión ya pertenece a `JV-PAYMENT-PROCEDURE`, pero falta definir quién puede autorizarlo y bajo qué límites.

* `DVAL2-S08-C05` — Jaime esboza una regla según la cual, tras determinados problemas de pago o no recogida, el cliente tendría que pagar antes de recoger en pedidos posteriores. La respuesta no cierra suficientemente la regla. Afecta `BR-INCIDENT-002` y `JV-INCIDENT-FAIRNESS` y requiere además revisión de fairness/compliance.

### RESOLVED_DELTA

* `DVAL2-S01-C07` — Añade la obligación de poder avisar al cliente cuando existe un problema con un pedido ya aceptado / que requiere atención.

* `DVAL2-S01-C10` — Pide conservar de alguna manera la asociación del contacto con un **pedido anterior no recogido**. Afecta las reglas de incidencias y debe reconciliarse con privacidad/retención.

* `DVAL2-S07-C02` — Resuelve la cuestión de si todos los pedidos presenciales necesitan teléfono: **no siempre**. Si el cliente espera allí puede no ser necesario; si se marcha y vuelve después, sí se necesita una vía de contacto.

* `DVAL2-S07-C03` — Aunque seleccionó "Pendiente de aportar", el comentario resuelve sustantivamente la responsabilidad de los pedidos telefónicos: **no hay responsable fijo; los atiende quien pueda según la carga de trabajo**.

* `DVAL2-S09-C02` — Refuerza el modelo de sesión operativa compartida en la tablet: Jaime y el delegado la utilizarán ambos y no es viable exigir reautenticación en cada interacción.

### CALIBRATION_PENDING

* `DVAL2-S01-C06` — El mecanismo de revisión manual por consumo elevado de capacidad queda aceptado inicialmente para el piloto; el porcentaje exacto queda para calibración.

* `DVAL2-S08-C03` — El comentario establece que las sustituciones son raras, normalmente sin modificar el precio, y que cuando falta algo pueden aplicar algún descuento si el cliente acepta. Queda pendiente calibrar/definir el límite económico correspondiente.

### EVIDENCE_PENDING

Las siguientes 15 cards no quedan resueltas simplemente por haberse seleccionado una opción; falta la información o evidencia concreta:

* `DVAL2-S01-C13`
* `DVAL2-S02-C07`
* `DVAL2-S03-C05`
* `DVAL2-S03-C09`
* `DVAL2-S04-C05`
* `DVAL2-S04-C06`
* `DVAL2-S05-C05`
* `DVAL2-S06-C03`
* `DVAL2-S07-C07`
* `DVAL2-S08-C09`
* `DVAL2-S09-C08`
* `DVAL2-S09-C05`
* `DVAL2-S10-C05`
* `DVAL2-S11-C02`
* `DVAL2-S11-C06`

En `DVAL2-S04-C06`, el comentario de Jaime sí aporta una frontera de negocio importante: solo pueden garantizar de forma específica la opción sin gluten; las alergias como frutos secos son muy difíciles de garantizar en esa cocina. Debe conservarse como evidencia, pero todavía falta el procedimiento y documentación necesarios para cerrar el gate correspondiente.

## 5. Gates no cerrados

Los 20 gates fueron evaluados. Los gates previamente cerrados `JV-DISCOVERY-CLOSE` y `JV-COHERENCE` permanecen resueltos.

Persisten asuntos abiertos en:

### PILOT

* `JV-CAPACITY` — valores operativos de capacidad y lead time.
* `JV-DELAYS` — umbrales exactos de retraso y respuesta.
* `JV-MODIFIERS` — matriz completa de modificadores, precios y límites.
* `JV-GLUTEN` — documentación del proveedor, procedimiento de cocina y límites ante alergias severas.
* `JV-ALLERGENS` — matriz de ingredientes/alérgenos/trazas y procedimiento de revisión.
* `JV-CATALOG-APPROVAL` — orden/categorías, destacados, temporales y datos definitivos del catálogo.
* `JV-STOCK` — plan de recuentos, responsables, límites y umbrales.
* `JV-PILOT` — participantes, fecha, ensayo, responsables de medición/revisión y evidencia de readiness.
* `JV-THRESHOLDS` — porcentajes y otros umbrales operativos.
* `JV-SHIFT-AUTHORITY` — límites de sustituciones/descuentos y autoridad del delegado.
* `JV-MANUAL-CHANNELS` — formalizar las reglas operativas derivadas de las respuestas sobre teléfono/mostrador.
* `JV-PAYMENT-PROCEDURE` — práctica de tickets/caja y decisión pendiente sobre pedidos "invitados".
* `JV-INCIDENT-FAIRNESS` — regla final para incidencias repetidas y revisión de fairness/compliance.

### WITHOUT_JAIME

* `JV-DELEGATION` — falta identidad y condiciones concretas del delegado; sigue siendo bloqueante.
* `JV-ACCESS` — falta procedimiento de onboarding/revocación/sesión y la aclaración de `DVAL2-S02-C03`.

### PUBLIC_LAUNCH

* `JV-COMPLIANCE` — entre otros puntos, faltan reglas/plazos de retención.
* `JV-CONTENT` — faltan copy final ES/CA y fotografía/contenido definitivo.
* `JV-PRIVACY` — falta concretar procedimientos de acceso, rectificación, borrado y demás obligaciones pendientes.

## 6. Reparto del trabajo restante

### STAKEHOLDER_DECISION_REQUIRED — Jaime

1. `DVAL2-S02-C03` — reformular y volver a preguntar los límites del respaldo móvil.
2. `DVAL2-S07-C08` — definir quién puede autorizar un pedido sin cobrar y bajo qué límites.
3. `DVAL2-S08-C05` — confirmar la regla final ante incidencias previas de pago/no recogida, incluyendo si realmente debe existir prepago posterior y en qué condiciones.

### OWNER_SCOPE_DECISION_REQUIRED

* `DVAL2-S01-C02` — decidir si los pedidos para días posteriores con recordatorios entran en el primer MVP o permanecen diferidos, dado su conflicto con `EXC-ADVANCE-ORDERS`.
* Autorizar o rechazar la incorporación canónica de los cinco `RESOLVED_DELTA`.

### DATA_OR_EVIDENCE_COLLECTION

No requieren una nueva card conceptual.

Incluyen los 15 `EVIDENCE_PENDING`: fechas especiales, datos reales de tablet/avisos, matriz de modificadores, contenido definitivo, documentación de alérgenos/gluten, plan de recuentos, mapa de sugerencias, práctica de tickets/caja, umbrales operativos, procedimiento de accesos, identidad del delegado, información de retención/privacidad, plan de medición del piloto, clientes participantes y fecha candidata.

### PILOT_CALIBRATION

* porcentaje/umbral asociado a la revisión manual por capacidad;
* límite económico aplicable a la excepción de sustitución/descuento.

## 7. Follow-up mínimo

No se necesita un nuevo ciclo amplio de stakeholder validation.

Es suficiente un **addendum de 3 preguntas semánticas** dirigido a Jaime:

1. respaldo móvil;
2. autoridad/límites para pedidos invitados;
3. regla final de incidencias repetidas/prepago.

Debe mantenerse separado de:

* la recogida de datos/evidencia pendiente;
* la calibración del piloto;
* la decisión de scope reservada al Owner.

## 8. Siguiente governed packet

### Owner Canonical Reconciliation & Follow-up Authorization

**Objetivo**

El Owner revisa este veredicto y:

1. decide el `SCOPE_CHANGE` de `DVAL2-S01-C02` / `EXC-ADVANCE-ORDERS`;
2. decide la incorporación canónica de los cinco `RESOLVED_DELTA`;
3. autoriza el addendum mínimo de tres preguntas a Jaime;
4. separa formalmente las vías de `DATA_OR_EVIDENCE_COLLECTION` y `PILOT_CALIBRATION`.

**Dependencia**

Este informe de reconciliación y la evidencia primaria `DOPIS-VAL-007`.

**Resultado esperado**

Un estado canónico reconciliado o unas decisiones explícitas del Owner que permitan continuar por vías separadas:

* follow-up focalizado de Jaime;
* recogida de evidencia;
* calibración posterior;
* planificación de use cases/arquitectura en los dominios ya estables.

**Decisión previa del Owner**

La cuestión de pedidos multi-día / `EXC-ADVANCE-ORDERS` requiere decisión de scope del Owner y no debe resolverse implícitamente.

Use-case/architecture planning puede avanzar únicamente sobre dominios ya `RATIFIED`, `RESOLVED_DELTA` una vez aceptados y mecanismos cuya calibración posterior no altere el modelo.

No debe asumir como cerrados los dominios pendientes de catálogo/alérgenos/stock, delegación/acceso, incidentes/pagos o cualquier otro gate cuyo diseño dependa de la decisión aún abierta.
