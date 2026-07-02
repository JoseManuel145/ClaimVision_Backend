# ClaimVision · Especificación de Endpoints faltantes (API v1)

> Para implementar en el backend (FastAPI). Basado en el esquema PostgreSQL real
> y la convención ya existente del contrato (`/api/v1/...`, acciones en kebab-case,
> soft-delete con `deleted_at`, columna `version` para bloqueo optimista).
>
> Leyenda: ✅ = ya existe en el contrato · 🆕 = falta implementar.

---

## 0. Convenciones globales (aplican a todo)

- **Base URL:** `/api/v1` (auth en `/api/auth`).
- **Auth:** `Authorization: Bearer <JWT>`. RBAC por `rol` (enum `rol_usuario`).
- **Multi-tenant:** todo lo no-admin se filtra por `aseguradora_id` del token. `Administrador_Global` ve todo.
- **Paginación:** `?page=1&page_size=20` → respuesta `{ "data": [...], "total": N, "page": 1, "page_size": 20 }`.
- **Soft-delete:** `DELETE` setea `deleted_at` (no borra físico). Los listados excluyen `deleted_at IS NOT NULL` por defecto.
- **Concurrencia optimista:** en `PATCH/PUT` enviar `version` actual; si no coincide → `409 Conflict`.
- **PII cifrada:** la API recibe/devuelve texto plano y cifra en reposo en estas columnas:
  `nombre_completo_cifrado`, `telefono_cifrado`, `curp_rfc_cifrado`.
- **Auditoría:** toda mutación escribe en `logs_auditoria`
  (`usuario_id`, `aseguradora_id`, `evento_modulo`, `accion_realizada`, `direccion_ip`, `user_agent`, `metadata_context`).
- **Errores:** `{ "code": "string", "message": "string", "detail": {...} }` con HTTP status correcto (400/401/403/404/409/422).
- **Uploads:** archivos vía URL prefirmada (ver §8). Las columnas `*_url` guardan la URL final.

---

## 1. Auth y cuenta — `/api/auth` y `/api/v1/me`

| Método | Ruta | Estado | Propósito / cuerpo |
|---|---|---|---|
| POST | `/api/auth/login` | ✅ | `{ email, password }` → `{ access_token, refresh_token, user }`. Maneja `estatus_usuario` (rechaza `Bloqueado_Temporal`/`Bloqueado_ARCO`/`Inactivo`). |
| POST | `/api/auth/refresh` | 🆕 | `{ refresh_token }` → nuevos tokens. |
| POST | `/api/auth/logout` | 🆕 | Invalida el refresh token actual. |
| POST | `/api/auth/forgot-password` | 🆕 | `{ email }` → envía código OTP al correo. (vista *Recuperar Contraseña*) |
| POST | `/api/auth/verify-otp` | 🆕 | `{ email, codigo }` → valida el código. (vista *Verificar Código*) |
| POST | `/api/auth/reset-password` | 🆕 | `{ email, codigo, nueva_password }` → actualiza `password_hash`. (vista *Nueva Contraseña*) |
| GET | `/api/v1/me` | 🆕 | Perfil del usuario autenticado + su perfil (`perfiles_clientes` / `perfiles_taller_usuarios` / `ajustadores`). |
| POST | `/api/v1/me/change-password` | 🆕 | `{ password_actual, password_nueva }`. |
| POST | `/api/v1/me/huella` | 🆕 | Vincular biometría `{ dispositivo_id, token_biometrico }` → `huella_vinculada = true`. |
| DELETE | `/api/v1/me/huella` | 🆕 | Desvincular biometría → `huella_vinculada = false`. |

---

## 2. Administrador Global — `/api/v1/admin`

### 2.1 Usuarios (tabla `usuarios`)
| Método | Ruta | Estado | Notas |
|---|---|---|---|
| GET | `/api/v1/admin/usuarios?rol=&estatus_arco=&aseguradora_id=&q=&page=` | 🆕 | Listado + filtros + búsqueda por `email`/nombre. |
| POST | `/api/v1/admin/usuarios` | 🆕 | `{ email, nombre_completo, telefono?, rol, aseguradora_id?, password? , enviar_invitacion }` → crea con `estatus_arco='Activo'`. |
| GET | `/api/v1/admin/usuarios/{id}` | 🆕 | Detalle. |
| PATCH | `/api/v1/admin/usuarios/{id}` | 🆕 | Editar (incluye `version`). |
| DELETE | `/api/v1/admin/usuarios/{id}` | 🆕 | Baja lógica: `deleted_at` + `estatus_arco='Inactivo'`. |
| POST | `/api/v1/admin/usuarios/{id}/reactivar` | 🆕 | `estatus_arco='Activo'`. |
| POST | `/api/v1/admin/usuarios/{id}/desbloquear` | 🆕 | De `Bloqueado_Temporal`/`Bloqueado_ARCO` → `Activo`. |
| POST | `/api/v1/admin/usuarios/{id}/reenviar-invitacion` | 🆕 | Reenvía correo de alta. |

### 2.2 Aseguradoras (tabla `aseguradoras`)
| Método | Ruta | Estado | Notas |
|---|---|---|---|
| GET | `/api/v1/admin/aseguradoras` | 🆕 | Listado con métricas agregadas. |
| POST | `/api/v1/admin/aseguradoras` | 🆕 | `{ nombre, rfc, dominio_correo, contacto_legal_email, plan_suscripcion, limite_peritajes_mes }` → `estatus_comercial='Activo'`. |
| GET | `/api/v1/admin/aseguradoras/{id}` | 🆕 | Detalle. |
| PATCH | `/api/v1/admin/aseguradoras/{id}` | 🆕 | Editar plan/límite/datos (`version`). |
| POST | `/api/v1/admin/aseguradoras/{id}/suspender` | 🆕 | `estatus_comercial='Suspendido'`. |
| POST | `/api/v1/admin/aseguradoras/{id}/reactivar` | 🆕 | `estatus_comercial='Activo'`. |
| DELETE | `/api/v1/admin/aseguradoras/{id}` | 🆕 | Baja lógica. |

### 2.3 Talleres y convenios (`talleres`, `convenio_aseguradora_taller`)
| Método | Ruta | Estado | Notas |
|---|---|---|---|
| GET | `/api/v1/admin/talleres?estatus=&aseguradora_id=&q=` | 🆕 | Listado. |
| POST | `/api/v1/admin/talleres` | 🆕 | `{ nombre_comercial, rfc, direccion_tecnica, telefono_contacto }`. |
| GET/PATCH/DELETE | `/api/v1/admin/talleres/{id}` | 🆕 | Detalle/editar/baja. |
| GET | `/api/v1/admin/convenios?aseguradora_id=&taller_id=` | 🆕 | Listado de convenios. |
| POST | `/api/v1/admin/convenios` | 🆕 | `{ aseguradora_id, taller_id, fecha_convenio }` (PK compuesta). |
| DELETE | `/api/v1/admin/convenios?aseguradora_id=&taller_id=` | 🆕 | Disolver convenio. |

### 2.4 Dashboard y auditoría
| Método | Ruta | Estado | Notas |
|---|---|---|---|
| GET | `/api/v1/admin/dashboard` | 🆕 | KPIs globales: totales, conteo por `estatus_siniestro`, serie por mes. |
| GET | `/api/v1/admin/auditoria?evento_modulo=&accion=&usuario_id=&aseguradora_id=&from=&to=&page=` | 🆕 | Lee `logs_auditoria`. |
| GET | `/api/v1/admin/auditoria/export?...` | 🆕 | Exporta CSV. |

---

## 3. Operador Aseguradora — `/api/v1/aseguradora`

| Método | Ruta | Estado | Transición / cuerpo |
|---|---|---|---|
| GET | `/api/v1/aseguradora/dashboard` | 🆕 | KPIs + `peritajes_consumidos_mes` / `limite_peritajes_mes`. |
| GET | `/api/v1/aseguradora/siniestros?estatus=&ajustador_id=&taller_id=&q=&page=` | 🆕 | Bandeja de siniestros del tenant. |
| GET | `/api/v1/aseguradora/siniestros/{id}` | 🆕 | Detalle completo (siniestro + `peritajes_ia` + `peritajes_ajustador` + `cotizaciones_taller` + imágenes). |
| POST | `/api/v1/aseguradora/siniestros/{id}/asignar-ajustador` | ✅ | `{ ajustador_id }` → `estatus = Asignado_A_Ajustador`. |
| POST | `/api/v1/aseguradora/siniestros/{id}/enviar-taller` | ✅ | `{ taller_id }` → `estatus = Asignado_A_Taller`. |
| POST | `/api/v1/aseguradora/siniestros/{id}/autorizar-entrega` | ✅ | → `estatus = Entregado`. |
| POST | `/api/v1/aseguradora/cotizaciones/{id}/aprobar` | 🆕 | `estatus_cotizacion = Aprobada`. |
| POST | `/api/v1/aseguradora/cotizaciones/{id}/rechazar` | 🆕 | `{ motivo }` → `estatus_cotizacion = Rechazada`. |
| GET | `/api/v1/aseguradora/ajustadores?activo_para_servicio=&cerca_de=lat,lng` | 🆕 | Para asignación (usa `geolocalizacion_actual`). |
| GET | `/api/v1/aseguradora/talleres` | 🆕 | Talleres con convenio vigente (para *enviar-taller*). |

---

## 4. Cliente (móvil) — `/api/v1/cliente`

| Método | Ruta | Estado | Transición / cuerpo |
|---|---|---|---|
| POST | `/api/v1/cliente/siniestros` | 🆕 | Reporte preliminar: `{ vehiculo_marca, vehiculo_modelo, vehiculo_anio, vehiculo_placas, vehiculo_vin?, latitud_siniestro, longitud_siniestro, narracion_texto?, narracion_audio_url?, indicaciones_dano_interno, fecha_siniestro }` → `estatus = Reportado_Preliminar`. |
| GET | `/api/v1/cliente/siniestros?page=` | 🆕 | Mis siniestros. |
| GET | `/api/v1/cliente/siniestros/{id}` | 🆕 | Seguimiento (timeline de `estatus_siniestro`). |
| POST | `/api/v1/cliente/siniestros/{id}/imagenes` | 🆕 | Registra `imagenes_siniestro` `{ imagen_url, metadatos_json }` tras subir (§8). |
| GET | `/api/v1/cliente/perfil` | 🆕 | `perfiles_clientes` (`numero_poliza`, `vigencia_poliza`). |
| PATCH | `/api/v1/cliente/consentimientos` | 🆕 | `{ consentimiento_aviso_privacidad, consentimiento_biometria, autoriza_transferencia_talleres }` → setea `fecha_consentimiento`. |

---

## 5. Ajustador (móvil) — `/api/v1/ajustador`

| Método | Ruta | Estado | Transición / cuerpo |
|---|---|---|---|
| GET | `/api/v1/ajustador/asignaciones?estatus=&page=` | 🆕 | Siniestros asignados a mí. |
| GET | `/api/v1/ajustador/siniestros/{id}` | 🆕 | Detalle + `peritajes_ia` + `danos_detectados_ia` (sugerencia IA con `costo_estimado_ia_min/max`). |
| POST | `/api/v1/ajustador/siniestros/{id}/peritaje` | 🆕 | Crea `peritajes_ajustador` `{ costo_definitivo_ajustador, firma_digital_ajustador, observaciones_campo }` + `danos_ajustados_manual[]` → `estatus = Peritaje_Validado`. |
| PATCH | `/api/v1/ajustador/peritajes/{id}` | 🆕 | Editar borrador antes de validar. |
| POST | `/api/v1/ajustador/peritajes/{id}/danos` | 🆕 | Agregar/editar `danos_ajustados_manual` `{ zona_vehiculo, tipo, severidad, costo_real_reparacion, origen_cambio }`. |
| PATCH | `/api/v1/ajustador/disponibilidad` | 🆕 | `{ activo_para_servicio }`. |
| PUT | `/api/v1/ajustador/geolocalizacion` | 🆕 | `{ latitud, longitud }` → `geolocalizacion_actual` (geography). |

---

## 6. Operador Taller (web) — `/api/v1/taller`

| Método | Ruta | Estado | Transición / cuerpo |
|---|---|---|---|
| GET | `/api/v1/taller/ordenes?estatus=&page=` | 🆕 | Siniestros en `Asignado_A_Taller` / en proceso. |
| GET | `/api/v1/taller/siniestros/{id}` | 🆕 | Detalle (incluye peritaje validado para cotizar). |
| POST | `/api/v1/taller/siniestros/{id}/cotizacion` | 🆕 | Crea `cotizaciones_taller` `{ monto_mano_obra, monto_refacciones, monto_total, desglose_pdf_url, observaciones_tecnicas? }` → `estatus_cotizacion = Pendiente_Aprobacion`. |
| PATCH | `/api/v1/taller/cotizaciones/{id}` | 🆕 | Editar cotización (si aún `Pendiente_Aprobacion`). |
| POST | `/api/v1/taller/siniestros/{id}/concluir-trabajo` | 🆕 | → `estatus = Trabajo_Concluido`. |
| POST | `/api/v1/taller/siniestros/{id}/listo-entrega` | 🆕 | → `estatus = Listo_Para_Entrega`. |

---

## 7. Peritaje IA (motor automático) — `/api/v1/ia`

> Se dispara tras subir imágenes; suele ser asíncrono (cola/worker). Documentar aunque sea interno.

| Método | Ruta | Estado | Propósito |
|---|---|---|---|
| POST | `/api/v1/ia/siniestros/{id}/analizar` | 🆕 | Lanza análisis → genera `peritajes_ia` (`costo_estimado_ia_min/max`) + `danos_detectados_ia[]` (`zona_vehiculo, tipo, severidad, costo_estimado_reparacion`). |
| POST | `/api/v1/ia/imagenes/{id}/validar-calidad` | 🆕 | Valida foto → `imagenes_siniestro.es_calidad_valida` (gate antes de peritar). |
| GET | `/api/v1/ia/siniestros/{id}/resultado` | 🆕 | Estado/resultado del análisis (polling o webhook). |

---

## 8. Transversales

| Método | Ruta | Estado | Propósito |
|---|---|---|---|
| GET | `/api/v1/notificaciones?leida=&page=` | 🆕 | Bandeja de notificaciones del usuario. ⚠️ **No hay tabla `notificaciones` en el esquema** — crear tabla o integrar push (FCM). |
| GET | `/api/v1/notificaciones/no-leidas/count` | 🆕 | Badge de no leídas. |
| POST | `/api/v1/notificaciones/{id}/marcar-leida` | 🆕 | Marca una. |
| POST | `/api/v1/notificaciones/marcar-todas-leidas` | 🆕 | Marca todas. |
| POST | `/api/v1/uploads/signed-url` | 🆕 | `{ tipo, content_type }` → URL prefirmada para `imagen_url` / `narracion_audio_url` / `desglose_pdf_url` / `firma_digital_ajustador`. |
| GET | `/api/v1/catalogos/enums` | 🆕 | Devuelve valores de enums para dropdowns: `rol_usuario`, `estatus_siniestro`, `estatus_cotizacion`, `estatus_comercial_aseguradora`, `estatus_usuario`, `tipo_dano`, `severidad_dano`. |

---

## Resumen de prioridad

1. **P0 (flujo central):** §4 Cliente (reportar+imágenes), §5 Ajustador (peritaje), §6 Taller (cotización+trabajo), §3 cotizaciones aprobar/rechazar + listados de siniestros.
2. **P1 (operación):** §2 Admin (usuarios/aseguradoras/talleres/convenios), §1 recuperación de contraseña + `/me`, §3 dashboards.
3. **P2 (soporte):** §7 IA, §8 notificaciones/uploads/catálogos, §2.4 auditoría/export.

> Ya existen solo: `POST /api/auth/login` y las 3 transiciones de `/api/v1/aseguradora/siniestros/{id}/...`. Todo lo demás (🆕) está por implementar.
