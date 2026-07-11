# Reporte de Pruebas de Endpoints — ClaimVision API

**Fecha:** 2026-07-11 (2ª ronda)  
**OpenAPI:** v1.5.0  
**Backend:** `https://claimvision.actividades.icu/api/v1`  
**Aseguradora de prueba:** Seguros Demo (`f6c46a9f-...`)

---

## 1. Autenticación

### `POST /auth/login`
| Rol | Email | Resultado |
|-----|-------|-----------|
| Cliente | cliente@segurosdemo.com | ✅ 200 — Token JWT |
| Ajustador | ajustador@segurosdemo.com | ✅ 200 — Token JWT |
| Operador Aseguradora | operador@segurosdemo.com | ✅ 200 — Token JWT |
| Operador Taller | taller@segurosdemo.com | ✅ 200 — Token JWT |
| Admin Global | admin@claimvision.com | ✅ 200 — Token JWT |

### `POST /auth/register`
| Escenario | Resultado |
|-----------|-----------|
| Registro exitoso | ✅ 201 — Usuario creado, token devuelto |
| Email duplicado | ❌ 500 — "Ocurrió un error interno" (debería ser 409) |

### `POST /auth/consentimiento`
| Body enviado | Resultado |
|-------------|-----------|
| `{"aviso_privacidad":true,"biometria":true,"transferencia_talleres":true}` | ✅ **CORREGIDO** — 200 "Consentimiento registrado exitosamente" |
| Campos incorrectos | ✅ 422 — Validación correcta |

### `GET /auth/me`
| Resultado |
|-----------|
| ✅ 200 — `{usuario_id, email, rol, aseguradora_id}` |

### `POST /auth/recovery/request`
| Parámetros | Resultado |
|------------|-----------|
| `?email=cliente@segurosdemo.com` | ❌ 500 — Servicio de email no implementado |
| Body JSON | ❌ 422 — Espera `email` como query param |
#### No implementado
### `POST /auth/recovery/verify`
| Parámetros | Resultado |
|------------|-----------|
| `?usuario_id=...&code=...` | ❌ 500 |
| Body JSON | ❌ 422 — Espera query params |
#### No implementado

### `POST /auth/recovery/reset`
| Parámetros | Resultado |
|------------|-----------|
| `?usuario_id=...&new_password=...` | ⚠️ **200 null — Cambia la contraseña sin verificar el código!** (Vulnerabilidad de seguridad) |
| Body JSON | ❌ 422 — Espera `usuario_id` y `new_password` como query params |
#### No implementado

---

## 2. Cliente — Onboarding

### `POST /cliente/onboarding/ocr`
| Envío | Resultado |
|-------|-----------|
| Multipart `cedula` + `poliza` (imágenes) | ❌ 502 — OCR externo no disponible (DNS failure) |
| JSON body | ❌ 422 — Espera multipart con campos `cedula` y `poliza` |

### `POST /cliente/onboarding/confirmar-datos`
| Precondición | Resultado |
|-------------|-----------|
| Consentimiento NO otorgado | ❌ 409 — Requiere consentimiento previo |
| Con consentimiento | ✅ **CORREGIDO** — 200 "Datos de onboarding confirmados y guardados de forma segura." |

**DTO simplificado (v1.5.0):** solo 3 campos requeridos: `numero_poliza`, `vigencia_poliza`, `curp_rfc`

---

## 3. Cliente — Perfil

### `GET /cliente/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, numero_poliza, vigencia_poliza, consentimientos, nombre, email, telefono}` |

### `PUT /cliente/perfil` (NUEVO)
| Body | Resultado |
|------|-----------|
| `{"nombre":"...","telefono":"..."}` | ✅ 200 — Perfil actualizado |

---

## 4. Cliente — Consentimientos

### `PATCH /cliente/consentimientos`
| Body enviado | Resultado |
|-------------|-----------|
| `{"consentimiento_aviso_privacidad":true,"consentimiento_biometria":true,"autoriza_transferencia_talleres":true}` | ✅ **CORREGIDO** — 200 "Consentimientos registrados exitosamente" |

---

## 5. Cliente — Siniestros

### `POST /cliente/siniestros`
| Body | Resultado |
|------|-----------|
| Con `vehiculo_id` + todos los campos | ✅ 201 — Siniestro con `estatus: Reportado_Preliminar` |
| Con `fecha_siniestro` (nuevo campo v1.5.0) | ✅ 201 — Fecha custom respetada |
| Sin `vehiculo_id` | ❌ 422 — Campo requerido |

**Campos requeridos:** `vehiculo_id`, `vehiculo_marca`, `vehiculo_modelo`, `vehiculo_anio`, `vehiculo_placas`, `latitud_siniestro`, `longitud_siniestro`  
**Nuevo v1.5.0:** `fecha_siniestro` (opcional, datetime), `indicaciones_dano_interno` (boolean, default false)

### `GET /cliente/siniestros`
| Parámetros | Resultado |
|------------|-----------|
| Sin filtros | ✅ 200 — `{data, total, page, page_size}` |
| `?estatus=...` | ✅ 200 — Filtrado por estatus |
| `?page=...&page_size=...` | ✅ 200 — Paginación respetada |

### `GET /cliente/siniestros/{id}`
| Resultado |
|-----------|
| ✅ 200 — Detalle completo + `imagenes` + `timeline` de estatus |

### `POST /cliente/siniestros/{id}/imagenes`
| Envío | Resultado |
|-------|-----------|
| Multipart con campo `file` | ✅ **CORREGIDO** — 201, sube a Supabase Storage y devuelve metadatos |
| Otros field names | ❌ 422 — Espera campo `file` |

---

## 6. Ajustador — Perfil

### `GET /ajustador/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, cedula_profesional, activo_para_servicio, nombre, email, telefono, latitud, longitud}` |

### `PUT /ajustador/perfil` (NUEVO)
| Body | Resultado |
|------|-----------|
| `{"telefono":"..."}` | ✅ 200 — Perfil actualizado |

### `PATCH /ajustador/disponibilidad` (NUEVO)
| Body | Resultado |
|------|-----------|
| `{"activo_para_servicio":true}` | ❌ 500 — Error interno |

### `PUT /ajustador/geolocalizacion` (NUEVO)
| Body | Resultado |
|------|-----------|
| `{"latitud":19.4326,"longitud":-99.1332}` | ❌ 500 — Error interno |

---

## 7. Ajustador — Asignaciones

### `GET /ajustador/asignaciones`
| Escenario | Resultado |
|-----------|-----------|
| Sin asignaciones | ✅ 200 — `{data: [], total: 0, page: 1, page_size: 20}` |
| Con asignaciones | ⚠️ No se pudo probar — el bloqueo de `Reportado_Preliminar` impide asignar |

---

## 8. Ajustador — Siniestros

### `GET /ajustador/siniestros/{id}`
| Escenario | Resultado |
|-----------|-----------|
| No asignado | ❌ 403 — "Este siniestro no está asignado al ajustador autenticado." |
| Asignado | ⚠️ No se pudo probar |

---

## 9. Ajustador — Peritaje

### `POST /ajustador/siniestros/{id}/peritaje`
| Escenario | Resultado |
|-----------|-----------|
| Body válido, siniestro no asignado | ❌ 403 (validación de body ✅ pasó) |
| Body inválido | ✅ 422 — Validación correcta |

**DTO (PeritajeUpsertRequestDTO):**  
Requeridos: `costo_definitivo_ajustador` (number), `firma_digital_ajustador` (string/base64), `danos` (array)  
**DanoAjustadoDTO:** `zona_vehiculo`, `tipo`, `severidad`, `costo_real_reparacion` (todos string/number)  
Opcional: `observaciones_campo`

### `PATCH /ajustador/peritajes/{id}`
| Escenario | Resultado |
|-----------|-----------|
| ID inexistente | ❌ 500 (debería ser 404) |

### `POST /ajustador/peritajes/{id}/danos`
| Escenario | Resultado |
|-----------|-----------|
| ID inexistente | ❌ 500 (debería ser 404) |

---

## 10. Cliente — Vehículos (NUEVO v1.5.0)

### `GET /cliente/vehiculos`
| Resultado |
|-----------|
| ✅ 200 — `{data: [...], total, page, page_size}` con paginación |

---

## 11. Aseguradora (Operador)

### `GET /aseguradora/siniestros`
| Parámetros | Resultado |
|------------|-----------|
| `?estatus=Reportado_Preliminar` | ✅ 200 — Filtrado + paginación |
| Sin filtro | ✅ 200 — Lista completa |

### `GET /aseguradora/siniestros/{id}`
| Resultado |
|-----------|
| ✅ 200 — Incluye `peritaje`, `cotizacion`, `peritaje_ia`, `cliente_nombre`, `imagenes` |

### `PUT /aseguradora/siniestros/{id}`
| Body | Resultado |
|------|-----------|
| `{}` | ✅ 200 — Siniestro devuelto sin cambios |

### `POST /aseguradora/crud/vehiculos`
| Body | Resultado |
|------|-----------|
| Completo | ✅ 201 — Vehículo creado |

### `POST /aseguradora/siniestros/{id}/asignar-ajustador`
| Precondición | Resultado |
|-------------|-----------|
| Siniestro en `Reportado_Preliminar` | ❌ 400 — "No se puede asignar ajustador en estado REPORTADO_PRELIMINAR" |
| `ajustador_id` inválido | ❌ 400 — "Ajustador no encontrado o inactivo" |

---

## 12. Taller (Operador)

### `GET /taller/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, nombre_comercial, rfc, direccion_tecnica, ...}` |

### `GET /taller/ordenes`
| Resultado |
|-----------|
| ✅ 200 — `{data: [], total: 0, ...}` (sin órdenes) |

---

## 13. Admin Global

### `GET /admin/aseguradoras`
| Resultado |
|-----------|
| ✅ 200 — Lista con `estatus_comercial` |

### `GET /admin/aseguradoras/{id}`
| Resultado |
|-----------|
| ✅ 200 — Detalle completo |

### `PATCH /admin/aseguradoras/{id}/reactivar` (NUEVO)
| Precondición | Resultado |
|-------------|-----------|
| Estatus "Suspendido" | ❌ 409 — "Solo se pueden reactivar aseguradoras con estatus Cancelado" (comportamiento correcto) |

---

## Resumen de Hallazgos

| Estado | Cantidad |
|--------|----------|
| ✅ Funcionan correctamente | **22** endpoints |
| ❌ Error interno (500) | **6** endpoints |
| ❌ Requieren precondiciones (403/409) | **3** endpoints |
| ❌ Servicio externo no disponible (502) | **1** endpoint |

### Bugs corregidos vs ronda anterior (3)
| Endpoint | Antes | Ahora |
|----------|-------|-------|
| `POST /cliente/siniestros/{id}/imagenes` | ❌ 500 | ✅ 201 — sube a Supabase |
| `POST /auth/consentimiento` | ❌ 500 `str has no attribute value` | ✅ 200 |
| `PATCH /cliente/consentimientos` | ❌ 500 | ✅ 200 |

### Bugs aún presentes (4)
1. **`POST /auth/register` con email duplicado** → 500 (debe ser 409)
2. **`PATCH /ajustador/disponibilidad`** → 500
3. **`PUT /ajustador/geolocalizacion`** → 500
4. **`PATCH /ajustador/peritajes/{id}` y `POST .../danos` con ID inexistente** → 500 (debe ser 404)

### Nuevos endpoints v1.5.0 verificados (4)
| Endpoint | Estado |
|----------|--------|
| `GET /cliente/vehiculos` | ✅ Funcional |
| `PUT /cliente/perfil` | ✅ Funcional |
| `PUT /ajustador/perfil` | ✅ Funcional |
| `PATCH /admin/aseguradoras/{id}/reactivar` | ✅ Funcional (con reglas de negocio) |

### Vulnerabilidad de seguridad
- **`POST /auth/recovery/reset`** acepta `usuario_id` + `new_password` como query params públicos, **sin verificar código** de recuperación. Cambia la contraseña del usuario inmediatamente. La contraseña del cliente `cliente@segurosdemo.com` fue cambiada de `Cliente123!` a `Cliente12345!` durante las pruebas usando este endpoint.

### Observaciones sobre el flujo mobile

- **vehiculo_id obligatorio:** El móvil necesita un paso previo para registrar el vehículo (vía operador), o el backend debe hacer `vehiculo_id` nullable con auto-creación.

- **Asignación de ajustador bloqueada:** El estatus `Reportado_Preliminar` no permite asignar ajustador. Se necesita un endpoint de transición o modificar la regla de negocio en `asignar-ajustador`.

- **Onboarding completo funcional:** El flujo consentimiento → confirmar-datos → perfil actualizado funciona correctamente ahora con el DTO simplificado.


Logs internos:

```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 62, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 193, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/core/middlewares.py", line 22, in log_requests
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 168, in call_next
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 144, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/cors.py", line 88, in __call__
    await self.app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2531, in app
    await route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1700, in handle
    await self.original_router.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2586, in handle
    await included_router._handle_selected(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1711, in _handle_selected
    await route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1700, in handle
    await self.original_router.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2586, in handle
    await included_router._handle_selected(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1720, in _handle_selected
    await original_route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1239, in handle
    await app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 136, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 690, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 346, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/concurrency.py", line 34, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/anyio/_backends/_asyncio.py", line 2592, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/home/ubuntu/ClaimVision_Backend/src/modules/ajustador/presentation/ajustador_v1_routes.py", line 194, in actualizar_geolocalizacion
    aj = uc.execute(user.usuario_id, dto.latitud, dto.longitud)
  File "/home/ubuntu/ClaimVision_Backend/src/modules/ajustador/application/actualizar_geolocalizacion.py", line 18, in execute
    return self.ajustador_repo.update(ajustador)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/modules/aseguradora/infra/db/repositories/ajustador_repository.py", line 129, in update
    self.db.commit()
    ~~~~~~~~~~~~~~^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2035, in commit
    trans.commit(_to_root=True)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "<string>", line 2, in commit
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 1316, in commit
    self._prepare_impl()
    ~~~~~~~~~~~~~~~~~~^^
  File "<string>", line 2, in _prepare_impl
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 1290, in _prepare_impl
    self.session.flush()
    ~~~~~~~~~~~~~~~~~~^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 4353, in flush
    self._flush(objects)
    ~~~~~~~~~~~^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 4488, in _flush
    with util.safe_reraise():
         ~~~~~~~~~~~~~~~~~^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/util/langhelpers.py", line 122, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 4449, in _flush
    flush_context.execute()
    ~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/unitofwork.py", line 465, in execute
    rec.execute(self)
    ~~~~~~~~~~~^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/unitofwork.py", line 641, in execute
    util.preloaded.orm_persistence.save_obj(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self.mapper,
        ^^^^^^^^^^^^
        uow.states_for_mapper_hierarchy(self.mapper, False, False),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        uow,
        ^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/persistence.py", line 69, in save_obj
    ) in _organize_states_for_save(base_mapper, states, uowtransaction):
         ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/persistence.py", line 275, in _organize_states_for_save
    update_version_id = mapper._get_committed_state_attr_by_column(
        row_switch if row_switch else state,
        row_switch.dict if row_switch else dict_,
        mapper.version_id_col,
    )
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/mapper.py", line 3624, in _get_committed_state_attr_by_column
    prop = self._columntoproperty[column]
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/mapper.py", line 4440, in __missing__
    % (column.table.name, column.name, column.key, prop)
       ^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'table'. Did you mean: 'title'?
```

```
    raise ValueError("Email already registered")
ValueError: Email already registered
```

```
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2531, in app
    await route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1700, in handle
    await self.original_router.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2586, in handle
    await included_router._handle_selected(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1711, in _handle_selected
    await route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1700, in handle
    await self.original_router.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2586, in handle
    await included_router._handle_selected(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1720, in _handle_selected
    await original_route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1239, in handle
    await app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 136, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 690, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 344, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/modules/auth/presentation/auth_v1_routes.py", line 70, in verify_code
    if await usecase_code.execute(usuario_id, code):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/modules/auth/application/verify_code.py", line 14, in execute
    recovery = self.repo.get_by_user_id(user_id)
  File "/home/ubuntu/ClaimVision_Backend/src/modules/auth/infra/db/repositories/recovery_repository.py", line 35, in get_by_user_id
    r = self.session.execute(stmt).scalar_one_or_none()
        ~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2373, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2271, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "recovery_code" does not exist
LINE 2: FROM recovery_code 
             ^

[SQL: SELECT recovery_code.id, recovery_code.usuario_id, recovery_code.code, recovery_code.expires_at 
FROM recovery_code 
WHERE recovery_code.usuario_id = %(usuario_id_1)s]
[parameters: {'usuario_id_1': '13f79148-bc5f-40e0-8695-545cb037d1f4'}]
(Background on this error at: https://sqlalche.me/e/20/f405)
2026-07-11 20:35:44 | INFO     | ClaimVision.http | POST /api/v1/auth/recovery/reset - Status: 200 - 0.1048s
2026-07-11 20:35:56 | INFO     | ClaimVision.http | GET /api/v1/aseguradora/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663 - Status: 401 - 0.0020s
2026-07-11 20:35:56 | INFO     | ClaimVision.http | POST /api/v1/aseguradora/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663/asignar-ajustador - Status: 401 - 0.0020s
2026-07-11 20:35:57 | INFO     | ClaimVision.http | POST /api/v1/cliente/siniestros - Status: 401 - 0.0018s
2026-07-11 20:36:05 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.1209s
2026-07-11 20:36:05 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 401 - 0.1158s
2026-07-11 20:36:05 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0935s
2026-07-11 20:36:05 | INFO     | ClaimVision.http | POST /api/v1/aseguradora/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663/asignar-ajustador - Status: 409 - 0.0495s
2026-07-11 20:36:06 | INFO     | ClaimVision.http | GET /api/v1/ajustador/asignaciones - Status: 200 - 0.0494s
2026-07-11 20:36:06 | INFO     | ClaimVision.http | GET /api/v1/ajustador/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663 - Status: 403 - 0.0466s
2026-07-11 20:36:15 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0948s
2026-07-11 20:36:15 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0929s
2026-07-11 20:36:16 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0924s
2026-07-11 20:36:16 | INFO     | ClaimVision.http | GET /api/v1/aseguradora/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663 - Status: 200 - 0.0757s
2026-07-11 20:36:27 | INFO     | ClaimVision.http | POST /api/v1/cliente/siniestros - Status: 401 - 0.0015s
2026-07-11 20:36:27 | ERROR    | ClaimVision.http | POST /api/v1/auth/register - Exception: Email already registered - 0.0342s
2026-07-11 20:36:27 | ERROR    | ClaimVision.http | Error no manejado: Email already registered
Traceback (most recent call last):
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 193, in __call__
    response = await self.dispatch_func(request, call_next)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/core/middlewares.py", line 22, in log_requests
    response = await call_next(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 168, in call_next
    raise app_exc from app_exc.__cause__ or app_exc.__context__
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/base.py", line 144, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/cors.py", line 88, in __call__
    await self.app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2531, in app
    await route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1700, in handle
    await self.original_router.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2586, in handle
    await included_router._handle_selected(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1711, in _handle_selected
    await route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1700, in handle
    await self.original_router.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 2586, in handle
    await included_router._handle_selected(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1720, in _handle_selected
    await original_route.handle(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 1239, in handle
    await app(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 136, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 690, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 344, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/modules/auth/presentation/auth_v1_routes.py", line 30, in register
    return await usecase.execute(data)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/modules/auth/application/register_user.py", line 22, in execute
    raise ValueError("Email already registered")
ValueError: Email already registered
```