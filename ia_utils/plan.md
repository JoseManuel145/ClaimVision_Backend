# Reporte de Pruebas de Endpoints — ClaimVision API

**Fecha:** 2026-07-11 (4ª ronda)  
**OpenAPI:** v1.5.0  
**Backend:** `https://claimvision.actividades.icu/api/v1`  
**Aseguradora de prueba:** Seguros Demo (`f6c46a9f-...`)  

---

## 1. Autenticación

| Endpoint | Resultado |
|----------|-----------|
| `POST /auth/login` (5 roles) | ✅ 200 — Todos los roles obtienen token |
| `GET /auth/me` | ✅ 200 — `{usuario_id, email, rol, aseguradora_id}` |
| `POST /auth/register` (nuevo) | ✅ 201 — Usuario creado |
| `POST /auth/register` (duplicado) | ✅ **CORREGIDO** — 409 "Email already registered" |
| `POST /auth/consentimiento` | ✅ 200 — "Consentimiento registrado exitosamente" |

### Recovery
| Endpoint | Body | Resultado |
|----------|------|-----------|
| `POST /auth/recovery/request` | `{"email":"..."}` | ✅ **CORREGIDO** — 200 `true` |
| `POST /auth/recovery/verify` | `{"usuario_id":"...","code":"..."}` | ✅ **CORREGIDO** — 400 "Código inválido o expirado." |
| `POST /auth/recovery/reset` | `{"usuario_id":"...","code":"...","new_password":"..."}` | ✅ **CORREGIDO** — Requiere `code` válido |

---

## 2. Cliente — Onboarding / Perfil / Siniestros

| Endpoint | Resultado |
|----------|-----------|
| `POST /cliente/onboarding/confirmar-datos` | ✅ 200 — DTO simplificado |
| `GET /cliente/perfil` | ✅ 200 |
| `PUT /cliente/perfil` | ✅ 200 |
| `PATCH /cliente/consentimientos` | ✅ 200 |
| `POST /cliente/siniestros` | ✅ 201 — `estatus: Reportado_Preliminar` |
| `GET /cliente/siniestros` | ✅ 200 |
| `GET /cliente/siniestros/{id}` | ✅ 200 — Detalle + imágenes + timeline |
| `POST /cliente/siniestros/{id}/imagenes` | ✅ 201 — Sube a Supabase Storage |
| `GET /cliente/vehiculos` | ✅ 200 |

---

## 3. Ajustador — Perfil

| Endpoint | Body | Resultado |
|----------|------|-----------|
| `GET /ajustador/perfil` | — | ✅ 200 |
| `PUT /ajustador/perfil` | `{"telefono"}` | ✅ 200 |
| `PATCH /ajustador/disponibilidad` | `{"activo_para_servicio":bool}` | ✅ **CORREGIDO** — 200 |
| `PUT /ajustador/geolocalizacion` | `{"latitud","longitud"}` | ✅ **CORREGIDO** — 200 |

---

## 4. Ajustador — Flujo de Peritaje

### `POST /aseguradora/siniestros/{id}/asignar-ajustador`
✅ **CORREGIDO** — 200, estatus cambia a `Asignado_A_Ajustador`

### `GET /ajustador/asignaciones`
✅ 200 — Lista paginada de siniestros asignados

### `GET /ajustador/siniestros/{id}`
✅ 200 (siniestro sin peritaje huérfano)  
❌ **500** (siniestro con peritaje huérfano de intento fallido)

### `POST /ajustador/siniestros/{id}/peritaje`
❌ **BUG CRÍTICO** — 500 "Ocurrió un error interno en el servidor."

**Causa raíz:** En `peritaje_repository.py:99`, `self.db.commit()` ocurre ANTES de `self.db.refresh()` y `_peritaje_to_domain()`. Si `refresh()` falla, el peritaje ya quedó persistido en la BD (commit exitoso) pero el endpoint retorna 500. Esto deja la BD inconsistente con un registro huérfano.

**Síntoma:** El GET del mismo siniestro desde ajustador/operador retorna 500 intentando cargar el peritaje huérfano. El GET desde cliente funciona bien (no consulta peritajes).

**Solución implementada en código local** (requiere redeploy):
1. `peritaje_repository.py`: Mover `_peritaje_to_domain()` ANTES de `self.db.commit()` para evitar commits parciales
2. `peritaje_dto.py`: Agregar validadores Pydantic en `DanoAjustadoDTO` para validar `tipo`/`severidad` contra los valores válidos del enum

### `PATCH /ajustador/peritajes/{id}`
✅ **CORREGIDO** — 404 cuando ID inexistente  
⚠️ No probado con ID válido (peritaje no se crea)

### `POST /ajustador/peritajes/{id}/danos`
✅ **CORREGIDO** — 404 cuando ID inexistente

---

## 5. Aseguradora (Operador)

| Endpoint | Resultado |
|----------|-----------|
| `GET /aseguradora/siniestros` | ✅ 200 |
| `GET /aseguradora/siniestros/{id}` | ❌ **500** para siniestro con peritaje huérfano; ✅ 200 para otros |
| `PUT /aseguradora/siniestros/{id}` | ✅ 200 |
| `POST /aseguradora/crud/vehiculos` | ✅ 201 |

---

## 6. Taller / Admin Global

| Endpoint | Resultado |
|----------|-----------|
| `GET /taller/perfil` | ✅ 200 |
| `GET /taller/ordenes` | ✅ 200 |
| `GET /admin/aseguradoras` | ✅ 200 |
| `GET /admin/aseguradoras/{id}` | ✅ 200 |

---

## Resumen

| Estado | Cantidad |
|--------|----------|
| ✅ Funcionan | **26** endpoints |
| ❌ Bug crítico | **1** (`POST peritaje` + GETs de siniestro con peritaje huérfano) |

### Bugs corregidos desde ronda 1 (10)
| Endpoint | Ronda 1 → Ronda 4 |
|----------|-------------------|
| Imagenes upload | ❌ 500 → ✅ 201 |
| Consentimiento POST | ❌ 500 → ✅ 200 |
| Consentimientos PATCH | ❌ 500 → ✅ 200 |
| Register duplicado | ❌ 500 → ✅ 409 |
| Disponibilidad | ❌ 500 → ✅ 200 |
| Geolocalizacion | ❌ 500 → ✅ 200 |
| Peritajes PATCH (ID inexistente) | ❌ 500 → ✅ 404 |
| Peritajes danos (ID inexistente) | ❌ 500 → ✅ 404 |
| Recovery request/verify/reset | ❌ 500 → ✅ 200 |
| **Asignar ajustador** | ❌ 400/409 → ✅ **200** |

### Bug nuevo: guardar_peritaje con commit prematuro

**Archivos modificados localmente (pendientes de deploy):**
- `ClaimVision_Backend/src/modules/siniestro/infra/db/repositories/peritaje_repository.py` — **Fix:** Mover `_peritaje_to_domain()` antes de `commit()` para evitar commits parciales
- `ClaimVision_Backend/src/modules/siniestro/presentation/peritaje/peritaje_dto.py` — **Fix:** Agregar validadores Pydantic para `tipo` y `severidad` contra los valores reales de los enums `TipoDano` y `SeveridadDano`

**Limpieza necesaria en BD:** El siniestro `465c46fb-ef1d-45a9-aecd-d677aecd9a96` tiene un registro huérfano en `peritajes_ajustador` que debe eliminarse manualmente.