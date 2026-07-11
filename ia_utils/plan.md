# Reporte de Pruebas de Endpoints — ClaimVision API

**Fecha:** 2026-07-11 (6ª ronda)  
**OpenAPI:** v1.5.0  
**Backend:** `https://claimvision.actividades.icu/api/v1`  
**Aseguradora:** Seguros Demo (`f6c46a9f-...`)

---

## 1. Autenticación

| Endpoint | Resultado |
|----------|-----------|
| `POST /auth/login` (5 roles) | ✅ 200 — Todos los roles obtienen token |
| `GET /auth/me` | ✅ 200 — `{usuario_id, email, rol, aseguradora_id}` |
| `POST /auth/register` (nuevo) | ✅ 201 — Usuario creado con token |
| `POST /auth/register` (duplicado) | ✅ 409 "Email already registered" |

### Consentimiento
| Endpoint | Campos | Resultado |
|----------|--------|-----------|
| `POST /auth/consentimiento` | `aviso_privacidad`, `biometria`, `transferencia_talleres` | ✅ **NUEVO SCHEMA** — 200 |
| `PATCH /cliente/consentimientos` | `consentimiento_aviso_privacidad`, `consentimiento_biometria`, `autoriza_transferencia_talleres` | ✅ 200 (schema anterior) |

### Recovery
| Endpoint | Body | Resultado |
|----------|------|-----------|
| `POST /auth/recovery/request` | `{"email":"..."}` | ✅ 200 `true` |
| `POST /auth/recovery/verify` | `{"usuario_id":"...","code":"..."}` | ✅ 400 "Código inválido o expirado." |
| `POST /auth/recovery/reset` | Requiere `code` válido | ✅ No vulnerable |

---

## 2. Cliente — Onboarding

| Endpoint | Body | Resultado |
|----------|------|-----------|
| `POST /cliente/onboarding/confirmar-datos` | `{"numero_poliza","vigencia_poliza","curp_rfc"}` | ⚠️ **Campo renombrado** de `curp_rpc` → `curp_rfc` |

---

## 3. Cliente — Perfil

| Endpoint | Body | Resultado |
|----------|------|-----------|
| `GET /cliente/perfil` | — | ✅ 200 |
| `PUT /cliente/perfil` | `{"nombre","telefono"}` | ✅ 200 |
| `PATCH /cliente/consentimientos` | `{"consentimiento_aviso_privacidad","consentimiento_biometria","autoriza_transferencia_talleres"}` | ✅ 200 |

---

## 4. Cliente — Siniestros

| Endpoint | Resultado |
|----------|-----------|
| `POST /cliente/siniestros` | ✅ 201 — Requiere `vehiculo_id` + `vehiculo_marca`, `vehiculo_modelo`, `vehiculo_anio`, `vehiculo_placas` |
| `GET /cliente/siniestros` | ✅ 200 — Paginación |
| `GET /cliente/siniestros/{id}` | ✅ 200 — Detalle + imágenes + timeline |
| `POST /cliente/siniestros/{id}/imagenes` | ✅ 201 — Sube a Supabase Storage |
| `GET /cliente/vehiculos` | ✅ 200 |

---

## 5. Ajustador — Perfil

| Endpoint | Body | Resultado |
|----------|------|-----------|
| `GET /ajustador/perfil` | — | ✅ 200 |
| `PUT /ajustador/perfil` | `{"telefono"}` | ✅ 200 |
| `PATCH /ajustador/disponibilidad` | `{"activo_para_servicio":bool}` | ✅ 200 |
| `PUT /ajustador/geolocalizacion` | `{"latitud","longitud"}` | ✅ 200 |

---

## 6. Ajustador — Flujo de Peritaje

### Asignación
| Endpoint | Resultado |
|----------|-----------|
| `POST /aseguradora/siniestros/{id}/asignar-ajustador` | ✅ 200 — estatus → `Asignado_A_Ajustador` |
| `GET /ajustador/asignaciones` | ✅ 200 — Lista paginada |
| `GET /ajustador/siniestros/{id}` | ✅ 200 — Detalle + imágenes + peritaje + peritaje_ia:null |

### Peritaje
| Endpoint | Envío | Resultado |
|----------|-------|-----------|
| `POST /ajustador/siniestros/{id}/peritaje` | `danos: [{tipo:"Abolladura", severidad:"Alto"}]` | ✅ **201** — Peritaje creado, estatus → `Peritaje_Validado` |
| `GET /ajustador/siniestros/{id}` | (post-peritaje) | ✅ **200** — Peritaje + danos visibles, siniestro en `Peritaje_Validado` |
| `PATCH /ajustador/peritajes/{id}` | `{"costo_definitivo_ajustador":26000}` | ✅ **409** "ya fue validado y no puede editarse" (correcto) |
| `POST /ajustador/peritajes/{id}/danos` | `{tipo,severidad,zona,costo}` | ✅ **409** "ya fue validado y no puede editarse" (correcto) |

### Notas
- Los enums de `tipo` y `severidad` usan **PascalCase** (`Abolladura`, `Alto`, etc.) tanto en el DTO como en la BD.
- UPPERCASE (`ABOLLADURA`, `ALTO`) es rechazado por el DTO con 422.
- El peritaje transiciona automáticamente a `Peritaje_Validado`, lo que bloquea edits/danos posteriores (comportamiento esperado).

---

## 7. Aseguradora (Operador)

| Endpoint | Resultado |
|----------|-----------|
| `GET /aseguradora/siniestros` | ✅ 200 |
| `GET /aseguradora/siniestros/{id}` | ✅ 200 — Detalle con peritaje, cotización, peritaje_ia |
| `POST /aseguradora/siniestros/{id}/asignar-ajustador` | ✅ 200 |
| `POST /aseguradora/siniestros/{id}/asignar-taller` | ✅ 200 (si taller existe) |
| `GET /aseguradora/crud/vehiculos` | ✅ 200 — **NUEVA RUTA** (`/aseguradora/vehiculos` ya no existe) |
| `GET /aseguradora/crud/talleres` | ✅ 200 — **NUEVA RUTA** |
| `GET /aseguradora/crud/ajustadores` | ✅ 200 — **NUEVA RUTA** (antes `/aseguradora/perfil-ajustadores`) |

---

## 8. Taller

| Endpoint | Resultado |
|----------|-----------|
| `GET /taller/perfil` | ✅ 200 |
| `GET /taller/ordenes` | ✅ 200 |

---

## 9. Admin Global

| Endpoint | Resultado |
|----------|-----------|
| `GET /admin/aseguradoras` | ✅ 200 |
| `GET /admin/aseguradoras/{id}` | ✅ 200 — Retorna `nombre` (campo actualizado) |
| `PATCH /admin/aseguradoras/{id}/reactivar` | ✅ 409 si estatus no es "Cancelado" |

---

## Resumen

| Estado | Cantidad |
|--------|----------|
| ✅ Funcionan | **32** endpoints |
| ❌ Bugs | **0** — todos los bugs resueltos |
| ⚠️ Observaciones | **2** (ver abajo) |

### Observaciones
1. **Onboarding** — El campo `curp_rpc` cambió a `curp_rfc`. No es un bug, solo un rename de schema.
2. **Rutas de operador movidas** — `GET /aseguradora/{vehiculos,talleres,perfil-ajustadores}` ahora son `GET /aseguradora/crud/{vehiculos,talleres,ajustadores}`. El endpoint `ajustadores-disponibles` fue eliminado.

### Cambios detectados en el schema (vs ronda 4)
| Endpoint | Cambio |
|----------|--------|
| `POST /cliente/siniestros` | **Ahora requiere** `vehiculo_id` además de los campos de vehículo |
| `POST /auth/consentimiento` | **Campos cambiados** a `aviso_privacidad`, `biometria`, `transferencia_talleres` |
| `GET /admin/aseguradoras/{id}` | **Campo cambiado** de `nombre_comercial` a `nombre` |
| `POST /cliente/onboarding/confirmar-datos` | **Campo renombrado** de `curp_rpc` → `curp_rfc` |
| Rutas de operador | Movidas a `/aseguradora/crud/*` |

### Historial de bugs resueltos

| Bug | Estado | Fix |
|-----|--------|-----|
| `POST peritaje` con commit prematuro (500 + peritaje huérfano) | ✅ **RESUELTO** | `peritaje_repository.py`: `flush()` → `refresh()` → `_peritaje_to_domain()` → `commit()` |
| Enum mismatch `tipo_dano`/`severidad_dano` | ✅ **NO APLICABA** — el análisis inicial fue incorrecto. El PG enum usa PascalCase, igual que el código Python. El error original era solo el commit prematuro. |

### Siniestros con peritajes huérfanos (requieren limpieza en BD)
```sql
DELETE FROM danos_ajustados_manual WHERE peritaje_ajustador_id IN 
  (SELECT id FROM peritajes_ajustador WHERE siniestro_id = '465c46fb-ef1d-45a9-aecd-d677aecd9a96');
DELETE FROM peritajes_ajustador WHERE siniestro_id = '465c46fb-ef1d-45a9-aecd-d677aecd9a96';
-- Repetir para '6070bbc6-91cc-42f3-8096-ae6fd49e7734' y '2eadddb3-7b24-43c4-bab9-a047ed2a010e'
```