# Especificación de Requerimientos: Módulo Admin (Super Admin)

## 1. Definición del Contexto

El Super Admin opera a nivel global (**Multi-tenant**). Su función principal es registrar, verificar, modificar suscripciones y dar de baja corporaciones (Aseguradoras), además de auditar el sistema global y ejecutar acciones regulatorias de privacidad de datos (LFPDPPP).

---

## 2. Puertos y Endpoints (Capa de Presentación / Controladores)

La IA debe generar los siguientes controladores expuestos en FastAPI bajo el prefijo `/v1/admin`:

| Método | Endpoint | Rol requerido | Descripción Técnica |
| --- | --- | --- | --- |
| `POST` | `/v1/admin/aseguradoras` | `SUPER_ADMIN` | Alta inicial de una empresa aseguradora tenant. |
| `GET` | `/v1/admin/aseguradoras` | `SUPER_ADMIN` | Listado masivo y filtrado de tenants corporativos. |
| `POST` | `/v1/admin/aseguradoras/{id}/verificar` | `SUPER_ADMIN` | Activa el estatus transaccional tras validar datos fiscales. |
| `PUT` | `/v1/admin/aseguradoras/{id}/suscripcion` | `SUPER_ADMIN` | Modifica el plan y límite de peritajes por IA contratados. |
| `DELETE` | `/v1/admin/aseguradoras/{id}` | `SUPER_ADMIN` | Detona el flujo asíncrono de desincorporación de la empresa. |
| `POST` | `/v1/admin/usuarios/{id}/bloqueo-arco` | `SUPER_ADMIN` | Aplica aislamiento y cifrado inmediato por solicitud ARCO. |
| `GET` | `/v1/admin/auditoria/logs` | `SUPER_ADMIN` | Consulta la bitácora global inmutable Append-Only. |

---

## 3. Lógica de los Casos de Uso (`application/usecases`)

Indica a la IA que implemente la lógica de negocio basándose estrictamente en estas especificaciones operativas:

### `RegistrarAseguradoraUseCase`

* **Entrada:** Nombre de la compañía, RFC/Identificación fiscal, Correo del contacto legal, Plan inicial de suscripción.
* **Operación:**
1. Genera un `tenant_id` único (UUIDv4).
2. Crea el registro en la tabla `aseguradoras` con estatus `Pendiente_Verificacion`.
3. Asigna el plan de suscripción base configurando el límite de peritajes mensuales de IA a cero provisionalmente.



### `VerificarAseguradoraUseCase`

* **Entrada:** `aseguradora_id` (UUID).
* **Operación:** Cambia el estatus del tenant a `Activo`. A partir de este momento se habilita el aislamiento de datos para que esa aseguradora pueda empezar a dar de alta a sus propios usuarios (ajustadores, talleres, clientes).

### `ActualizarSuscripcionUseCase`

* **Entrada:** `aseguradora_id`, `nuevo_plan`, `limite_peritajes_mensuales`.
* **Operación:** Actualiza los parámetros comerciales del tenant.
* **Regla de negocio asociada:** Modifica los umbrales de consumo. La infraestructura del core debe disparar alertas preventivas cuando las peticiones a los microservicios de inferencia alcancen el 90% del límite establecido en este caso de uso.

### `DesincorporarAseguradoraUseCase` *(Soft-Delete & Dump Cifrado)*

* **Entrada:** `aseguradora_id`.
* **Operación:** No borra filas directamente (evita `DELETE` físicos en cascada). Ejecuta un *Background Job* asíncrono que realiza lo siguiente:
1. Cambia el estatus de la aseguradora a `Desincorporada` y bloquea inmediatamente cualquier autenticación de sus usuarios asociados.
2. Compila el histórico transaccional del tenant en un archivo contenedor ZIP.
3. Cifra el archivo utilizando **AES-256** mediante una clave simétrica robusta manejada en infraestructura.
4. Genera un enlace de descarga seguro tokenizado con expiración corta y lo envía al correo del contacto legal registrado.



### `AplicarBloqueoArcoUseCase` *(Privacidad LFPDPPP para Personas Físicas)*

* **Entrada:** `usuario_id` (Aplica a Clientes o Ajustadores, NO a la entidad Aseguradora).
* **Operación:**
1. Inhabilita las credenciales de acceso y revoca de forma inmediata todos los tokens JWT activos del usuario en el servicio de Redis local.
2. Aplica cifrado simétrico robusto (**AES-256**) sobre las columnas de identidad del usuario en la base de datos (nombres, direcciones, teléfonos).
3. El registro se mantiene congelado con estatus `Bloqueado_ARCO` para cumplimiento normativo de conservación legal, impidiendo su lectura ordinaria en el resto del sistema.



### `ConsultarAuditoriaUseCase`

* **Operación:** Permite la lectura secuencial de los registros de la bitácora global.
* **Restricción estricta de infraestructura:** El repositorio de auditoría carece por completo de métodos `update()` o `delete()`; opera estrictamente bajo el formato **Append-Only** (Solo Escritura/Lectura).