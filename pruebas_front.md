## Segunda ronda — 2026-07-18

Objetivo de esta ronda: re-verificar el hallazgo crítico de E.3 (500 al subir PDF de cotización) y validar contra el backend real 3 features nuevas del frontend (editar/eliminar vehículo, reactivar/listar aseguradoras desincorporadas, botones "Concluir trabajo"/"Listo para entrega" en Presupuestos Enviados).

**Primer intento bloqueado por caída del backend:** el backend respondió `502 Bad Gateway` (Cloudflare) en todos los endpoints probados, incluyendo rutas estáticas (`/`, `/openapi.json`, `/docs`) — instancia EC2 caída o inalcanzable, no un bug de la app. Se reintentó ~7 veces en ~2 minutos sin éxito. Tras avisar que el backend ya estaba levantado de nuevo, se confirmó `GET /openapi.json` → `200` y se corrió la ronda completa de punta a punta con éxito (ver abajo).

**Cómo se probó:** igual que la primera ronda — cadena de prueba armada desde cero con `curl` (sin browser automation disponible), usando el superadmin para crear un operador nuevo en el tenant vivo **"Aseguradora Testing GP"**, con prefijo de email `qa2.*.20260718@testinggp.com` para no chocar con los registros de la ronda anterior. Cada payload se armó leyendo el schema real en `openapi_backend.json` y los `*.routes.ts`/`*.schemas.ts` del frontend.

### 🔴 Hallazgo crítico — SIGUE ROTO

**`POST /taller/siniestros/{id}/cotizacion` (subir PDF) sigue devolviendo `500 Internal Server Error`.** Se armó una cadena 100% nueva (operador → cliente → vehículo → ajustador → taller → operador de taller → siniestro reportado → ajustador asignado → peritaje registrado → enviado a taller, confirmado en `Asignado_A_Taller`) y se subió un PDF válido con el mismo multipart exacto que arma `cotizaciones.routes.ts::create` (`monto_mano_obra`, `monto_refacciones`, `monto_total`, `observaciones_tecnicas`, `desglose_pdf`). Resultado: `500 {"error":"Ocurrió un error interno en el servidor."}`. Sin el archivo, el mismo endpoint sigue respondiendo `422` correctamente pidiendo `desglose_pdf` — confirma otra vez que el fallo está específicamente en el manejo del archivo. **No hay ningún cambio de comportamiento respecto a la primera ronda** — el bug documentado en el backend real sigue exactamente igual, no fue corregido.

Como consecuencia, `POST /taller/siniestros/{id}/concluir-trabajo` sin cotización aprobada también se retesteó y **sigue devolviendo `500`** en vez de un error de negocio controlado (mismo hallazgo secundario de E.5, sin cambios).

Esto **bloquea la validación end-to-end de la feature nueva "Concluir trabajo"/"Listo para entrega"** en `PresupuestosEnviadosPage.tsx`: como nunca se puede llegar a una cotización con estatus `Aprobada` por este bug, no se pudo ejercitar el happy path completo (aprobar cotización → concluir trabajo → listo para entrega) contra el backend real. Los endpoints (`concluir-trabajo`, `listo-entrega`) están correctamente conectados en el frontend y existen en el backend — pero quedan sin poder probarse de punta a punta hasta que se arregle la subida de PDF.

### ✅ Vehículos: editar y eliminar — validado end-to-end

| Prueba | Llamada | Resultado |
|---|---|---|
| Editar vehículo | `PUT /aseguradora/crud/vehiculos/{id}` (marca/modelo/placas/vin/color) | ✅ `200`, todos los campos se actualizaron correctamente (confirmado con `GET` posterior) |
| Eliminar vehículo | `DELETE /aseguradora/crud/vehiculos/{id}` | ✅ `204` |
| Confirmar baja | `GET /aseguradora/crud/vehiculos?cliente_id=...` tras eliminar | ✅ el vehículo eliminado ya no aparece en el listado, solo queda el otro vehículo del cliente |

Los botones nuevos de editar/eliminar en `VehiculoCard`/`GestionVehiculosPage.tsx` quedan validados contra el backend real.

### ✅ Aseguradoras: reactivar / desincorporadas — validado end-to-end

| Prueba | Llamada | Resultado |
|---|---|---|
| Crear aseguradora descartable | `POST /admin/aseguradoras` | ✅ `201`, nace `Suspendido` |
| Verificar | `POST .../verificar` | ✅ `200`, pasa a `Activo` |
| Dar de baja | `DELETE /admin/aseguradoras/{id}` | ✅ `200`, `estatus_comercial: Cancelado`, `deleted_at` con timestamp |
| Confirmar excluida del listado normal | `GET /admin/aseguradoras?include_deleted=false` | ✅ no aparece |
| Confirmar aparece en desincorporadas | `GET /admin/aseguradoras/desincorporadas` | ✅ aparece |
| Reactivar | `PATCH /admin/aseguradoras/{id}/reactivar` | ✅ `200` |
| Confirmar reaparece en listado normal | `GET /admin/aseguradoras?include_deleted=false` | ✅ reaparece |

**Nota de comportamiento del backend (no es un bug, pero afecta la UX):** al reactivar, `estatus_comercial` vuelve a `Suspendido`, **no** al `Activo` que tenía antes de la baja — el backend no recuerda el estado previo, exige re-verificar. En el frontend esto ya se maneja bien solo: como la pestaña "Activas" mapea cualquier estatus distinto de `Activo` a `'Inactiva'`, una aseguradora recién reactivada aparece ahí con el botón "Verificar" visible, que es exactamente lo que hace falta hacer. No se requiere ningún cambio de código por este hallazgo.

### ✅ Spot-check del resto del flujo

| Prueba | Llamada | Resultado |
|---|---|---|
| 403 en Aseguradoras (quefalta #12) | `GET /admin/aseguradoras?page=1&page_size=20` | ✅ `200`, sigue sin reproducirse |
| Auditoría — listar eventos | `GET /admin/auditoria/logs?page=1&page_size=10` | ✅ `200`, 102 eventos totales (subieron desde los 67 de la primera ronda, quedaron auditadas todas las acciones de esta corrida) |
| Cambio de contraseña propia | `PATCH /auth/password` | ✅ `200` |
| Login con contraseña nueva | `POST /auth/login` | ✅ `200`, confirma que aplicó |

### Hallazgos menores de esta ronda (no bloquean nada)

- El regex de RFC (`^[A-ZÑ&]{3,4}\d{6}[A-Za-z\d]{3}$`) no acepta dígitos en el prefijo de 3-4 letras — un error de datos de prueba propio (`QA2260718AB1`), no un bug; el backend respondió `422` correctamente con el detalle del patrón esperado.
- `POST /aseguradora/siniestros/{id}/enviar-taller` con un `taller_id` no existente/malformado (probado sin querer por un error de encadenado de variables en el script de prueba) devolvió `500` en vez de `404`/`422` — el schema no valida formato UUID en `EnviarTallerDTO.taller_id`, así que un id inválido llega hasta una consulta a base de datos que revienta sin control. Hallazgo menor, mismo patrón de manejo de errores poco robusto que ya se documentó en E.3/E.5, pero de bajo impacto porque el frontend siempre manda IDs reales tomados de un `<select>`.
- `POST /auth/login` respondió `429 Too Many Requests` una vez, en una ráfaga de logins consecutivos sin pausa — hay rate limiting activo en login; no afecta el uso normal de la web (un usuario no hace logins consecutivos en segundos).

### Datos de prueba que quedaron en el backend (ronda 2)

Todo bajo el tenant **"Aseguradora Testing GP"**, prefijo `qa2.*.20260718@testinggp.com`:

- Operador de aseguradora, operador de taller, cliente, ajustador (todos activos)
- 1 taller ("QA2 Taller Prueba")
- 1 vehículo (el que quedó tras probar editar/eliminar sobre el otro)
- 1 siniestro en `Asignado_A_Taller` sin cotización (bloqueado por el bug crítico, igual que el de la ronda 1)
- La aseguradora "QA2 Aseguradora Reactivacion" quedó activa de nuevo (`Suspendido`, pendiente de re-verificar) tras el ciclo completo de baja/reactivación

No se purgó nada — mismo criterio que la ronda anterior.