# Reporte de Pruebas de Endpoints — ClaimVision API

**Fecha:** 2026-07-11  
**Backend:** `https://claimvision.actividades.icu/api/v1`  
**Aseguradora de prueba:** Seguros Demo (`f6c46a9f-...`)  

---

## 1. Autenticación

### `POST /auth/login`
| Rol | Email | Resultado |
|-----|-------|-----------|
| Cliente | cliente@segurosdemo.com | ✅ 200 — Token obtenido |
| Ajustador | ajustador@segurosdemo.com | ✅ 200 — Token obtenido |
| Operador Aseguradora | operador@segurosdemo.com | ✅ 200 — Token obtenido |
| Operador Taller | taller@segurosdemo.com | ✅ 200 — Token obtenido |
| Admin Global | admin@claimvision.com | ✅ 200 — Token obtenido |

### `GET /auth/me`
| Token | Resultado |
|-------|-----------|
| Cliente | ✅ 200 — `{usuario_id, email, rol, aseguradora_id}` |

### `POST /auth/register`
| Escenario | Resultado |
|-----------|-----------|
| Registro exitoso | ✅ 201 — Usuario creado, token devuelto |
| Email duplicado | ❌ 500 — "Ocurrió un error interno" (debería ser 409) |
> Nota: Solo el SUPER_ADMINISTRADOR y ASEGURADORA pueden registrar usuarios
### `POST /auth/consentimiento`
| Body enviado | Resultado |
|-------------|-----------|
| `{"aviso_privacidad":true,"biometria":true,"transferencia_talleres":true}` | ❌ 500 — `"'str' object has no attribute 'value'"` (bug backend) |
| Campos incorrectos | ✅ 422 — Validación correcta (espera `aviso_privacidad`, `biometria`, `transferencia_talleres`) |

### `PATCH /cliente/consentimientos`
| Body enviado | Resultado |
|-------------|-----------|
| `{"consentimiento_aviso_privacidad":true,"consentimiento_biometria":true,"autoriza_transferencia_talleres":true}` | ❌ 500 — Error interno |

### `POST /auth/recovery/request`
| Parámetros | Resultado |
|------------|-----------|
| `?email=cliente@segurosdemo.com` (query) | ❌ 500 — Error interno (servicio de email no implementado?) |
| Body JSON | ❌ 422 — Espera `email` como query param, no en body |
> Nota: aun no implementado
### `POST /auth/recovery/verify`
| Parámetros | Resultado |
|------------|-----------|
| `?usuario_id=13f79148&code=123456` (query) | ❌ 500 — Error interno |
| Body JSON | ❌ 422 — Espera `usuario_id` y `code` como query params |
> Nota: aun no implementado

---

## 2. Cliente — Onboarding

### `POST /cliente/onboarding/ocr`
| Envío | Resultado |
|-------|-----------|
| Multipart `cedula` + `poliza` (imágenes) | ❌ 502 — "Error de comunicación con el servicio OCR: Temporary failure in name resolution" (servicio OCR externo no disponible) |
| JSON body | ❌ 422 — Espera multipart con campos `cedula` y `poliza` |

### `POST /cliente/onboarding/confirmar-datos`
| Precondición | Resultado |
|-------------|-----------|
| Sin consentimiento previo | ❌ 409 — "No se pueden guardar datos sensibles sin el consentimiento previo del aviso de privacidad." |
| Campos faltantes | ✅ 422 — Validación: requiere `vigencia_poliza`, `curp_rfc`, etc. |

Campos requeridos: `numero_poliza`, `vigencia_poliza`, `nombre_completo`, `fecha_nacimiento`, `curp_rfc`, `calle`, `numero_exterior`, `colonia`, `codigo_postal`, `ciudad`, `estado`

---

## 3. Cliente — Perfil

### `GET /cliente/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, numero_poliza, consentimientos, nombre, email, telefono}` |

---

## 4. Cliente — Siniestros

### `POST /cliente/siniestros` (Crear reporte preliminar)
| Body | Resultado |
|------|-----------|
| Con `vehiculo_id` válido + todos los campos | ✅ 201 — Siniestro creado con `estatus: Reportado_Preliminar` |
| Sin `vehiculo_id` | ❌ 422 — Campo requerido |

**Campos requeridos:** `vehiculo_id`, `vehiculo_marca`, `vehiculo_modelo`, `vehiculo_anio`, `vehiculo_placas`, `latitud_siniestro`, `longitud_siniestro`  
**Campos opcionales:** `narracion_texto`, `indicaciones_dano_interno`  
**Nota:** El móvil debe crear el vehículo vía `POST /aseguradora/crud/vehiculos` (rol Operador) antes de crear el siniestro, o bien el backend debe aceptar `vehiculo_id` nullable.

### `GET /cliente/siniestros`
| Parámetros | Resultado |
|------------|-----------|
| Sin filtros | ✅ 200 — `{data: [...], total, page, page_size}` con paginación correcta |

### `GET /cliente/siniestros/{id}`
| Resultado |
|-----------|
| ✅ 200 — Detalle completo con `imagenes: []` y `timeline` de estatus |

### `POST /cliente/siniestros/{id}/imagenes`
| Envío | Resultado |
|-------|-----------|
| Multipart con `imagenes`, `files`, `file` | ❌ 500 — "Ocurrió un error interno en el servidor." (bug backend) |

---

## 5. Ajustador — Perfil

### `GET /ajustador/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, cedula_profesional, activo_para_servicio, nombre, email, telefono}` |

---

## 6. Ajustador — Asignaciones

### `GET /ajustador/asignaciones`
| Escenario | Resultado |
|-----------|-----------|
| Sin siniestros asignados | ✅ 200 — `{data: [], total: 0, page: 1, page_size: 20}` (paginación correcta) |

---

## 7. Ajustador — Siniestros

### `GET /ajustador/siniestros/{id}`
| Escenario | Resultado |
|-----------|-----------|
| Siniestro no asignado a este ajustador | ❌ 403 — "Este siniestro no está asignado al ajustador autenticado." |

---

## 8. Ajustador — Peritaje

### `POST /ajustador/siniestros/{id}/peritaje`
| Escenario | Resultado |
|-----------|-----------|
| Body válido, siniestro no asignado | ❌ 403 — "Este siniestro no está asignado al ajustador autenticado." (validación de body ✅ pasó) |
| Body inválido | ✅ 422 — Validación correcta |

**Campos requeridos:** `costo_definitivo_ajustador` (number), `firma_digital_ajustador` (string/base64), `danos` (array de `DanoAjustadoDTO`)  
**DanoAjustadoDTO:** `zona_vehiculo`, `tipo`, `severidad`, `costo_real_reparacion` (todos requeridos), `origen_cambio` (default: "AJUSTADOR")  
**Opicional:** `observaciones_campo`

### `PATCH /ajustador/peritajes/{id}`
| Escenario | Resultado |
|-----------|-----------|
| ID inexistente | ❌ 500 — Error interno |
| Body inválido | ✅ 422 — Validación (`EditarPeritajeRequest` con campos opcionales) |

### `POST /ajustador/peritajes/{id}/danos`
| Escenario | Resultado |
|-----------|-----------|
| ID inexistente | ❌ 500 — Error interno |
| Sin archivo | ❌ 422 — Validación (espera archivo `imagenes`) |

---

## 9. Aseguradora (Operador)

### `GET /aseguradora/siniestros`
| Parámetros | Resultado |
|------------|-----------|
| `?estatus=Reportado_Preliminar` | ✅ 200 — Lista filtrada con paginación |
| Sin filtro | ✅ 200 — Lista completa |

### `GET /aseguradora/siniestros/{id}`
| Resultado |
|-----------|
| ✅ 200 — Detalle con `peritaje`, `cotizacion`, `peritaje_ia`, `cliente_nombre`, `ajustador_nombre` extras |

### `PUT /aseguradora/siniestros/{id}`
| Body | Resultado |
|------|-----------|
| `{}` (sin cambios) | ✅ 200 — Siniestro devuelto sin modificar |

### `POST /aseguradora/siniestros/{id}/asignar-ajustador`
| Precondición | Resultado |
|-------------|-----------|
| Siniestro en `Reportado_Preliminar` | ❌ 400 — "No se puede asignar ajustador en estado EstatusSiniestro.REPORTADO_PRELIMINAR" |
| `ajustador_id` inválido | ❌ 400 — "Ajustador no encontrado o inactivo" |

**Nota:** No se encontró endpoint para cambiar el estatus del siniestro de `Reportado_Preliminar` a otro estado. El flujo completo requiere que el backend exponga un endpoint de revisión/aprobación del reporte preliminar, o bien que la asignación del ajustador sea el propio mecanismo de transición (lo cual contradice el error actual).

---

## 10. Taller (Operador)

### `GET /taller/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, nombre_comercial, rfc, direccion_tecnica, ...}` |

### `GET /taller/ordenes`
| Resultado |
|-----------|
| ✅ 200 — `{data: [], total: 0, page: 1, page_size: 20}` (sin órdenes asignadas) |

---

## 11. Admin Global

### `GET /admin/aseguradoras`
| Resultado |
|-----------|
| ✅ 200 — Lista de aseguradoras con `estatus_comercial` |

### `GET /admin/aseguradoras/{id}`
| Resultado |
|-----------|
| ✅ 200 — Detalle de aseguradora |

**Nota:** La aseguradora "Seguros Demo" tiene `estatus_comercial: "Suspendido"`. No se pudo reactivar vía PATCH (405 Method Not Allowed).

---

## 12. CRUD Aseguradora

### `POST /aseguradora/crud/vehiculos`
| Body | Resultado |
|------|-----------|
| Con todos los campos | ✅ 201 — Vehículo creado con ID |

---

## Resumen de Hallazgos

| Estado | Cantidad |
|--------|----------|
| ✅ Funcionan correctamente | **14** endpoints |
| ❌ Error interno del servidor (500) | **7** endpoints |
| ❌ Requieren precondiciones (403/409) | **4** endpoints |
| ❌ Servicio externo no disponible (502) | **1** endpoint |

### Bugs detectados en el backend

1. **`POST /auth/consentimiento`** — Error `"'str' object has no attribute 'value'"` con el body correcto `{"aviso_privacidad":true,"biometria":true,"transferencia_talleres":true}`. El endpoint pasa validación Pydantic pero falla en lógica interna.

2. **`PATCH /cliente/consentimientos`** — Error 500 con los campos correctos del esquema `ConsentimientosRequest`.

3. **`POST /cliente/siniestros/{id}/imagenes`** — Error 500 sin importar el nombre del campo multipart (`imagenes`, `files`, `file`).

4. **`POST /auth/register` con email duplicado** — Retorna 500 en lugar de 409 Conflict.

5. **`PATCH /ajustador/peritajes/{id}` y `POST .../danos`** — Retornan 500 con ID inexistente, deberían retornar 404.

6. **Endpoints de recovery** — Retornan 500 (probablemente falta implementación del servicio de email).

### Observaciones sobre el flujo mobile

- **Creación de siniestro:** El móvil envía datos de vehículo sin un `vehiculo_id` precargado. El backend requiere `vehiculo_id` como campo obligatorio. Soluciones posibles: (a) que el backend acepte `vehiculo_id` como nullable, auto-creando el vehículo; (b) que el móvil tenga un paso previo de registro de vehículo.

- **Asignación de ajustador:** El estatus `Reportado_Preliminar` bloquea la asignación. No existe un endpoint público para cambiar este estatus desde el frontend web del operador. Se necesita o bien: (a) un endpoint `POST .../revisar` o similar; (b) que el `asignar-ajustador` permita la transición desde `Reportado_Preliminar`.

- **Consentimiento del cliente:** Es requisito previo para `confirmar-datos`, pero el endpoint de consentimiento tiene un bug que impiste otorgarlo. Sin consentimiento no se puede completar el onboarding.