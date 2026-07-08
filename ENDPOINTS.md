# ClaimVision API — Endpoints

Todas las rutas están bajo el prefijo global `/api`.

---

## Health

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Health check de la API |

---

# v1

### Auth

Prefijo: `/api/v1/auth`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/auth/register` | Registrar un nuevo usuario |
| `POST` | `/api/v1/auth/login` | Iniciar sesión con email/contraseña |
| `GET` | `/api/v1/auth/me` | Obtener usuario autenticado actual |
| `POST` | `/api/v1/auth/recovery/request` | Solicitar código de recuperación de contraseña |
| `POST` | `/api/v1/auth/recovery/verify` | Verificar código de recuperación |
| `POST` | `/api/v1/auth/recovery/reset` | Restablecer contraseña |
| `POST` | `/api/v1/auth/consentimiento` | Registrar consentimiento de privacidad |

### Admin

Prefijo: `/api/v1/admin`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/admin/aseguradoras` | Registrar una nueva aseguradora |
| `POST` | `/api/v1/admin/aseguradoras/{aseguradora_id}/operadores` | Crear operador para una aseguradora |
| `GET` | `/api/v1/admin/aseguradoras` | Listar aseguradoras (paginado) |
| `GET` | `/api/v1/admin/aseguradoras/desincorporadas` | Listar aseguradoras desincorporadas |
| `GET` | `/api/v1/admin/aseguradoras/{aseguradora_id}` | Obtener aseguradora por ID |
| `PUT` | `/api/v1/admin/aseguradoras/{aseguradora_id}` | Actualizar datos de la aseguradora |
| `POST` | `/api/v1/admin/aseguradoras/{aseguradora_id}/verificar` | Verificar una aseguradora |
| `PUT` | `/api/v1/admin/aseguradoras/{aseguradora_id}/suscripcion` | Actualizar suscripción de la aseguradora |
| `DELETE` | `/api/v1/admin/aseguradoras/{aseguradora_id}` | Desincorporar (baja lógica) una aseguradora |
| `POST` | `/api/v1/admin/usuarios/{usuario_id}/bloqueo-arco` | Aplicar bloqueo ARCO a un usuario |
| `GET` | `/api/v1/admin/usuarios` | Listar usuarios (paginado, filtros por rol/estatus/search) |
| `GET` | `/api/v1/admin/usuarios/{usuario_id}` | Obtener detalle de un usuario |
| `POST` | `/api/v1/admin/usuarios` | Crear usuario con cualquier rol |
| `PUT` | `/api/v1/admin/usuarios/{usuario_id}` | Actualizar datos de un usuario |
| `DELETE` | `/api/v1/admin/usuarios/{usuario_id}` | Baja lógica de un usuario (valida siniestros activos) |
| `GET` | `/api/v1/admin/talleres` | Listar todos los talleres (sin filtro por aseguradora) |
| `GET` | `/api/v1/admin/talleres/{taller_id}` | Obtener detalle de taller con aseguradoras vinculadas |
| `GET` | `/api/v1/admin/dashboard/resumen` | KPIs globales del sistema |
| `GET` | `/api/v1/admin/auditoria/logs` | Consultar logs de auditoría (paginado) |

### Cliente

Prefijo: `/api/v1/cliente`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/cliente/siniestros` | Reportar un siniestro (estatus → Reportado_Preliminar) |
| `GET` | `/api/v1/cliente/siniestros` | Listar mis siniestros (paginado, con filtro por estatus) |
| `GET` | `/api/v1/cliente/siniestros/{id}` | Detalle del siniestro con imágenes y timeline |
| `POST` | `/api/v1/cliente/siniestros/{id}/imagenes` | Registrar una imagen ya subida (vía URL prefirmada) |
| `GET` | `/api/v1/cliente/perfil` | Obtener perfil del cliente (póliza, consentimientos) |
| `PATCH` | `/api/v1/cliente/consentimientos` | Actualizar consentimientos LFPDPPP |
| `POST` | `/api/v1/cliente/onboarding/ocr` | Extraer datos de cédula y póliza mediante OCR |
| `POST` | `/api/v1/cliente/onboarding/confirmar-datos` | Confirmar y guardar datos del onboarding |

### Ajustador

Prefijo: `/api/v1/ajustador`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/ajustador/asignaciones` | Listar siniestros asignados al ajustador (paginado) |
| `GET` | `/api/v1/ajustador/siniestros/{id}` | Detalle del siniestro con imágenes y peritaje |
| `POST` | `/api/v1/ajustador/siniestros/{id}/peritaje` | Crear peritaje (estatus → Peritaje_Validado) |
| `PATCH` | `/api/v1/ajustador/peritajes/{id}` | Editar borrador del peritaje |
| `POST` | `/api/v1/ajustador/peritajes/{id}/danos` | Agregar daño manual al peritaje |
| `PATCH` | `/api/v1/ajustador/disponibilidad` | Activar/desactivar disponibilidad para servicio |
| `PUT` | `/api/v1/ajustador/geolocalizacion` | Actualizar geolocalización del ajustador |

### Taller

Prefijo: `/api/v1/taller`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/taller/ordenes` | Listar órdenes de trabajo del taller (paginado) |
| `GET` | `/api/v1/taller/siniestros/{id}` | Expediente técnico (siniestro + peritaje + cotización) |
| `POST` | `/api/v1/taller/siniestros/{id}/cotizacion` | Crear cotización (estatus → Pendiente_Aprobacion) |
| `PATCH` | `/api/v1/taller/cotizaciones/{id}` | Editar cotización mientras esté pendiente |
| `POST` | `/api/v1/taller/siniestros/{id}/concluir-trabajo` | Concluir trabajo (estatus → Trabajo_Concluido) |
| `POST` | `/api/v1/taller/siniestros/{id}/listo-entrega` | Marcar listo para entrega (estatus → Listo_Para_Entrega) |

### Aseguradora — Siniestros

Prefijo: `/api/v1/aseguradora`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/aseguradora/siniestros` | Bandeja de siniestros del tenant (filtros + paginación) |
| `GET` | `/api/v1/aseguradora/siniestros/{id}` | Detalle completo (siniestro + imágenes + peritaje + cotización) |
| `POST` | `/api/v1/aseguradora/siniestros/{id}/asignar-ajustador` | Asignar ajustador al siniestro (estatus → Asignado_A_Ajustador) |
| `POST` | `/api/v1/aseguradora/siniestros/{id}/enviar-taller` | Enviar siniestro al taller (estatus → Asignado_A_Taller) |
| `POST` | `/api/v1/aseguradora/siniestros/{id}/autorizar-entrega` | Autorizar entrega del vehículo (estatus → Entregado) |
| `POST` | `/api/v1/aseguradora/cotizaciones/{id}/aprobar` | Aprobar cotización del taller |
| `POST` | `/api/v1/aseguradora/cotizaciones/{id}/rechazar` | Rechazar cotización del taller |
| `PUT` | `/api/v1/aseguradora/siniestros/{id}` | Editar datos de un siniestro existente |

### Aseguradora — CRUD

Prefijo: `/api/v1/aseguradora`

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/aseguradora/ajustadores` | Crear un ajustador (usuario + perfil) |
| `GET` | `/api/v1/aseguradora/ajustadores` | Listar ajustadores del tenant (paginado) |
| `GET` | `/api/v1/aseguradora/ajustadores/{id}` | Obtener ajustador por ID |
| `PUT` | `/api/v1/aseguradora/ajustadores/{id}` | Actualizar datos del ajustador |
| `DELETE` | `/api/v1/aseguradora/ajustadores/{id}` | Eliminar ajustador |
| `POST` | `/api/v1/aseguradora/clientes` | Crear un cliente (usuario + perfil) |
| `GET` | `/api/v1/aseguradora/clientes` | Listar clientes del tenant (paginado) |
| `GET` | `/api/v1/aseguradora/clientes/{id}` | Obtener cliente por ID |
| `POST` | `/api/v1/aseguradora/talleres` | Registrar un taller |
| `GET` | `/api/v1/aseguradora/talleres` | Listar talleres del tenant (paginado) |
| `GET` | `/api/v1/aseguradora/talleres/{id}` | Obtener taller por ID |
| `PUT` | `/api/v1/aseguradora/talleres/{id}` | Actualizar datos del taller |
| `DELETE` | `/api/v1/aseguradora/talleres/{id}` | Desvincular taller de la aseguradora |
| `POST` | `/api/v1/aseguradora/talleres/{id}/operadores` | Crear operador para un taller |
| `POST` | `/api/v1/aseguradora/usuarios/{id}/bloqueo-arco` | Aplicar bloqueo ARCO a un usuario del tenant |
| `POST` | `/api/v1/aseguradora/usuarios/{id}/desbloqueo-arco` | Desbloquear ARCO de un usuario del tenant |

---

## Totales

| Grupo | Endpoints |
|-------|----------|
| Auth | 7 |
| Admin | 19 |
| Cliente | 8 |
| Ajustador | 7 |
| Taller | 6 |
| Aseguradora (Siniestros) | 8 |
| Aseguradora (CRUD) | 16 |
| **Subtotal** | **71** |
| Health | 1 |
| **Total** | **72** |
