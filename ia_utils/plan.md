2026-07-11 21:24:21 | ERROR    | ClaimVision.http | Error no manejado: Object of type bytes is not JSON serializable
Traceback (most recent call last):
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 136, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 739, in app
    raise validation_error
fastapi.exceptions.RequestValidationError: 1 validation error:
  {'type': 'model_attributes_type', 'loc': ('body',), 'msg': 'Input should be a valid dictionary or object to extract fields from', 'input': b'--------------------------G0X7CxBntFneTfU6qBcaPU\r\nContent-Disposition: form-data; name="imagenes"; filename="test_image.png"\r\nContent-Type: image/png\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\xdacd\xf8\xcfP\x0f\x00\x03\x86\x01\x80Z4}k\x00\x00\x00\x00IEND\xaeB`\x82\r\n--------------------------G0X7CxBntFneTfU6qBcaPU--\r\n'}

  File "/home/ubuntu/ClaimVision_Backend/src/modules/ajustador/presentation/ajustador_v1_routes.py", line 156, in agregar_dano
    POST /api/v1/ajustador/peritajes/{id}/danos

The above exception was the direct cause of the following exception:

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
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 59, in wrapped_app
    response = await handler(conn, exc)  # type: ignore[arg-type]
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/core/exceptions.py", line 170, in validation_exception_handler
    return JSONResponse(
        status_code=422,
        content={"error": "Error de validación en la solicitud.", "details": exc.errors()}
    )
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/responses.py", line 192, in __init__
    super().__init__(content, status_code, headers, media_type, background)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/responses.py", line 45, in __init__
    self.body = self.render(content)
                ~~~~~~~~~~~^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/responses.py", line 195, in render
    return json.dumps(
           ~~~~~~~~~~^
        content,
        ^^^^^^^^
    ...<3 lines>...
        separators=(",", ":"),
        ^^^^^^^^^^^^^^^^^^^^^^
    ).encode("utf-8")
    ^
  File "/usr/lib/python3.14/json/__init__.py", line 242, in dumps
    **kw).encode(obj)
          ~~~~~~^^^^^
  File "/usr/lib/python3.14/json/encoder.py", line 202, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib/python3.14/json/encoder.py", line 263, in iterencode
    return _iterencode(o, 0)
  File "/usr/lib/python3.14/json/encoder.py", line 182, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeError: Object of type bytes is not JSON serializable
when serializing dict item 'input'
when serializing list item 0
when serializing dict item 'details'

ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 136, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/fastapi/routing.py", line 739, in app
    raise validation_error
fastapi.exceptions.RequestValidationError: 1 validation error:
  {'type': 'model_attributes_type', 'loc': ('body',), 'msg': 'Input should be a valid dictionary or object to extract fields from', 'input': b'--------------------------G0X7CxBntFneTfU6qBcaPU\r\nContent-Disposition: form-data; name="imagenes"; filename="test_image.png"\r\nContent-Type: image/png\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\xdacd\xf8\xcfP\x0f\x00\x03\x86\x01\x80Z4}k\x00\x00\x00\x00IEND\xaeB`\x82\r\n--------------------------G0X7CxBntFneTfU6qBcaPU--\r\n'}

  File "/home/ubuntu/ClaimVision_Backend/src/modules/ajustador/presentation/ajustador_v1_routes.py", line 156, in agregar_dano
    POST /api/v1/ajustador/peritajes/{id}/danos

The above exception was the direct cause of the following exception:

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
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 59, in wrapped_app
    response = await handler(conn, exc)  # type: ignore[arg-type]
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/src/core/exceptions.py", line 170, in validation_exception_handler
    return JSONResponse(
        status_code=422,
        content={"error": "Error de validación en la solicitud.", "details": exc.errors()}
    )
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/responses.py", line 192, in __init__
    super().__init__(content, status_code, headers, media_type, background)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/responses.py", line 45, in __init__
    self.body = self.render(content)
                ~~~~~~~~~~~^^^^^^^^^
  File "/home/ubuntu/ClaimVision_Backend/venv/lib/python3.14/site-packages/starlette/responses.py", line 195, in render
    return json.dumps(
           ~~~~~~~~~~^
        content,
        ^^^^^^^^
    ...<3 lines>...
        separators=(",", ":"),
        ^^^^^^^^^^^^^^^^^^^^^^
    ).encode("utf-8")
    ^
  File "/usr/lib/python3.14/json/__init__.py", line 242, in dumps
    **kw).encode(obj)
          ~~~~~~^^^^^
  File "/usr/lib/python3.14/json/encoder.py", line 202, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib/python3.14/json/encoder.py", line 263, in iterencode
    return _iterencode(o, 0)
  File "/usr/lib/python3.14/json/encoder.py", line 182, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeError: Object of type bytes is not JSON serializable
when serializing dict item 'input'
when serializing list item 0
when serializing dict item 'details'


2026-07-11 21:24:21 | INFO     | ClaimVision.http | POST /api/v1/auth/recovery/request - Status: 422 - 0.0022s
2026-07-11 21:24:22 | INFO     | ClaimVision.http | POST /api/v1/auth/recovery/verify - Status: 422 - 0.0023s
2026-07-11 21:24:23 | INFO     | ClaimVision.http | POST /api/v1/aseguradora/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663/asignar-ajustador - Status: 401 - 0.0018s
2026-07-11 21:24:41 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0962s
2026-07-11 21:24:41 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0955s
2026-07-11 21:24:41 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.0954s
2026-07-11 21:24:44 | INFO     | ClaimVision.http | POST /api/v1/auth/recovery/request - Status: 200 - 1.9971s
2026-07-11 21:24:44 | INFO     | ClaimVision.http | POST /api/v1/auth/recovery/verify - Status: 400 - 0.0382s
2026-07-11 21:24:44 | INFO     | ClaimVision.http | POST /api/v1/auth/recovery/reset - Status: 422 - 0.0024s
2026-07-11 21:24:45 | INFO     | ClaimVision.http | POST /api/v1/cliente/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663/imagenes - Status: 201 - 0.6106s
2026-07-11 21:24:46 | INFO     | ClaimVision.http | POST /api/v1/aseguradora/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663/asignar-ajustador - Status: 409 - 0.0527s
2026-07-11 21:24:46 | INFO     | ClaimVision.http | PATCH /api/v1/ajustador/peritajes/dummy-id - Status: 404 - 0.0385s
2026-07-11 21:24:46 | INFO     | ClaimVision.http | GET /api/v1/ajustador/siniestros/0985d89e-d73f-438f-b1aa-2f44fdd40663 - Status: 403 - 0.0520s
2026-07-11 21:24:46 | INFO     | ClaimVision.http | GET /api/v1/ajustador/perfil - Status: 200 - 0.0262s
2026-07-11 21:25:01 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.1000s
2026-07-11 21:25:01 | INFO     | ClaimVision.http | POST /api/v1/ajustador/peritajes/dummy-id/danos - Status: 404 - 0.0695s
2026-07-11 21:25:01 | INFO     | ClaimVision.http | POST /api/v1/auth/login - Status: 200 - 0.2455s
2026-07-11 21:25:02 | INFO     | ClaimVision.http | POST /api/v1/cliente/siniestros - Status: 201 - 0.1735s
2026-07-11 21:25:02 | INFO     | ClaimVision.http | GET /api/v1/cliente/siniestros - Status: 200 - 0.0864s
2026-07-11 21:25:02 | INFO     | ClaimVision.http | GET /api/v1/auth/me - Status: 200 - 0.0022s




Notas del frontend:

# Reporte de Pruebas de Endpoints — ClaimVision API

**Fecha:** 2026-07-11 (3ª ronda)  
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

### `GET /auth/me`
| Resultado |
|-----------|
| ✅ 200 — `{usuario_id, email, rol, aseguradora_id}` |

### `POST /auth/register`
| Escenario | Resultado |
|-----------|-----------|
| Registro exitoso | ✅ 201 — Usuario creado, token devuelto |
| Email duplicado | ✅ **CORREGIDO** — 409 "Email already registered" |

### `POST /auth/consentimiento`
| Body | Resultado |
|------|-----------|
| `{"aviso_privacidad":true,"biometria":true,"transferencia_talleres":true}` | ✅ 200 — "Consentimiento registrado exitosamente" |
| Campos incorrectos | ✅ 422 — Validación correcta |

### `POST /auth/recovery/request`
| Body | Resultado |
|------|-----------|
| `{"email":"..."}` (JSON body) | ✅ **CORREGIDO** — 200 `true` (ahora acepta body, no query params) |

### `POST /auth/recovery/verify`
| Body | Resultado |
|------|-----------|
| `{"usuario_id":"...","code":"..."}` | ✅ **CORREGIDO** — 400 "Código inválido o expirado." (acepta body) |

### `POST /auth/recovery/reset`
| Body | Resultado |
|------|-----------|
| `{"usuario_id":"...","code":"...","new_password":"..."}` | ✅ **CORREGIDO** — Validación correcta. Requiere `code` (ya no acepta query params sin verificación) |

---

## 2. Cliente — Onboarding

### `POST /cliente/onboarding/confirmar-datos`
| Precondición | Resultado |
|-------------|-----------|
| Sin consentimiento | ❌ 409 |
| Con consentimiento | ✅ 200 — "Datos de onboarding confirmados y guardados de forma segura." |

**DTO:** `numero_poliza`, `vigencia_poliza`, `curp_rfc` (3 campos requeridos)

---

## 3. Cliente — Perfil

### `GET /cliente/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, numero_poliza, vigencia_poliza, consentimientos, nombre, email, telefono}` |

### `PUT /cliente/perfil`
| Body | Resultado |
|------|-----------|
| `{"nombre":"...","telefono":"..."}` | ✅ 200 — Perfil actualizado |

---

## 4. Cliente — Consentimientos

### `PATCH /cliente/consentimientos`
| Body | Resultado |
|------|-----------|
| `{"consentimiento_aviso_privacidad":true,"consentimiento_biometria":true,"autoriza_transferencia_talleres":true}` | ✅ 200 — "Consentimientos registrados exitosamente." |

---

## 5. Cliente — Siniestros

### `POST /cliente/siniestros`
| Body | Resultado |
|------|-----------|
| Completo (con `vehiculo_id`) | ✅ 201 — `estatus: Reportado_Preliminar` |
| Con `fecha_siniestro` (opcional) | ✅ 201 — Fecha custom respetada |
| Sin `vehiculo_id` | ❌ 422 — Campo requerido |

### `GET /cliente/siniestros`
| Parámetros | Resultado |
|------------|-----------|
| `?estatus=...&page=...&page_size=...` | ✅ 200 — `{data, total, page, page_size}` |

### `GET /cliente/siniestros/{id}`
| Resultado |
|-----------|
| ✅ 200 — Detalle + `imagenes` + `timeline` de estatus |

### `POST /cliente/siniestros/{id}/imagenes`
| Envío | Resultado |
|-------|-----------|
| Multipart con campo `file` | ✅ 201 — Sube a Supabase Storage |

---

## 6. Cliente — Vehículos

### `GET /cliente/vehiculos`
| Resultado |
|-----------|
| ✅ 200 — `{data, total, page, page_size}` con paginación |

---

## 7. Ajustador — Perfil

### `GET /ajustador/perfil`
| Resultado |
|-----------|
| ✅ 200 — `{id, cedula_profesional, activo_para_servicio, nombre, email, telefono}` |

### `PUT /ajustador/perfil`
| Body | Resultado |
|------|-----------|
| `{"telefono":"..."}` | ✅ 200 — Perfil actualizado |

### `PATCH /ajustador/disponibilidad`
| Body | Resultado |
|------|-----------|
| `{"activo_para_servicio":true}` | ✅ **CORREGIDO** — 200, disponibilidad actualizada |

### `PUT /ajustador/geolocalizacion`
| Body | Resultado |
|------|-----------|
| `{"latitud":19.4326,"longitud":-99.1332}` | ✅ **CORREGIDO** — 200 (version incrementa, lat/long se almacenan) |

---

## 8. Ajustador — Asignaciones

### `GET /ajustador/asignaciones`
| Resultado |
|-----------|
| ✅ 200 — `{data, total, page, page_size}` (vacío si no hay asignaciones) |

---

## 9. Ajustador — Siniestros

### `GET /ajustador/siniestros/{id}`
| Escenario | Resultado |
|-----------|-----------|
| No asignado al ajustador | ❌ 403 |

---

## 10. Ajustador — Peritaje

### `POST /ajustador/siniestros/{id}/peritaje`
| Escenario | Resultado |
|-----------|-----------|
| Body válido, no asignado | ❌ 403 (validación de body ✅) |

**DTO requerido:** `costo_definitivo_ajustador`, `firma_digital_ajustador`, `danos[]`  
**DanoAjustadoDTO:** `zona_vehiculo`, `tipo`, `severidad`, `costo_real_reparacion`  
**Opcional:** `observaciones_campo`

### `PATCH /ajustador/peritajes/{id}`
| Escenario | Resultado |
|-----------|-----------|
| ID inexistente | ✅ **CORREGIDO** — 404 "Peritaje no encontrado" |

### `POST /ajustador/peritajes/{id}/danos`
| Escenario | Resultado |
|-----------|-----------|
| ID inexistente | ✅ **CORREGIDO** — 404 "Peritaje no encontrado" |

---

## 11. Aseguradora (Operador)

### `GET /aseguradora/siniestros`
| Resultado |
|-----------|
| ✅ 200 — Lista con filtro `?estatus=` y paginación |

### `GET /aseguradora/siniestros/{id}`
| Resultado |
|-----------|
| ✅ 200 — Incluye `imagenes`, `peritaje`, `cotizacion`, `cliente_nombre` |

### `PUT /aseguradora/siniestros/{id}`
| Body | Resultado |
|------|-----------|
| `{}` o con campos | ✅ 200 — Siniestro actualizado |

### `POST /aseguradora/siniestros/{id}/asignar-ajustador`
| Precondición | Resultado |
|-------------|-----------|
| Siniestro en `Reportado_Preliminar` | ❌ 409 — "No se puede asignar ajustador en estado REPORTADO_PRELIMINAR" |
| `ajustador_id` inválido | ❌ 400 — "Ajustador no encontrado o inactivo" |

### `POST /aseguradora/crud/vehiculos`
| Body | Resultado |
|------|-----------|
| Completo | ✅ 201 — Vehículo creado |

---

## 12. Taller (Operador)

### `GET /taller/perfil`
| Resultado |
|-----------|
| ✅ 200 |

### `GET /taller/ordenes`
| Resultado |
|-----------|
| ✅ 200 — `{data: [], total: 0, ...}` |

---

## 13. Admin Global

### `GET /admin/aseguradoras`
| Resultado |
|-----------|
| ✅ 200 |

### `GET /admin/aseguradoras/{id}`
| Resultado |
|-----------|
| ✅ 200 |

### `PATCH /admin/aseguradoras/{id}/reactivar`
| Precondición | Resultado |
|-------------|-----------|
| Estatus "Suspendido" | ❌ 409 — Solo acepta "Cancelado" (comportamiento correcto) |

---

## Resumen

| Estado | Cantidad |
|--------|----------|
| ✅ Funcionan | **27** endpoints |
| ❌ Requieren precondiciones | **3** endpoints |

### Bugs corregidos en esta ronda (8)
| Endpoint | Ronda 2 → Ronda 3 |
|----------|-------------------|
| `POST /auth/register` (duplicado) | ❌ 500 → ✅ **409** |
| `PATCH /ajustador/disponibilidad` | ❌ 500 → ✅ **200** |
| `PUT /ajustador/geolocalizacion` | ❌ 500 → ✅ **200** |
| `PATCH /ajustador/peritajes/{id}` (ID inexistente) | ❌ 500 → ✅ **404** |
| `POST /ajustador/peritajes/{id}/danos` (ID inexistente) | ❌ 500 → ✅ **404** |
| Recovery request | ❌ 500 → ✅ **200** (body JSON) |
| Recovery verify | ❌ 500 → ✅ **400** (body JSON) |
| Recovery reset | ❌ vulnerabilidad → ✅ **requiere code** |

### Único hallazgo pendiente
- **Asignación de ajustador bloqueada** en estatus `Reportado_Preliminar` — el flujo requiere que el backend permita la transición o exponga un endpoint de revisión.