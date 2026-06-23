# Guía Técnica de Flujo y Endpoints para el Backend - ClaimVision v3.0

Este documento describe el comportamiento operativo del sistema basado en la especificación de requerimientos de software e historias de usuario v3.0. Su propósito es definir la lógica de negocio, las restricciones normativas y los eventos asíncronos que debe procesar la capa backend (SOA).

---

## 1. Módulo Común: Autenticación y Control de Acceso (RBAC)
**Requerimientos Relacionados:** RF-002, RF-010, RNF-011, RNF-012

### Flujo de Backend:
1. El cliente envía `email` y `password` en texto plano mediante un canal cifrado (HTTPS).
2. El backend busca el usuario en la base de datos centralizada.
3. Si la cuenta tiene un estado `'Bloqueado por ARCO'`, el servicio debe denegar inmediatamente el acceso emitiendo un código HTTP 403 (Forbidden).
4. El backend verifica el hash de la contraseña (`password_hash`). Si es erróneo, emite un HTTP 401 genérico para evitar la enumeración de cuentas.
5. Tras 5 intentos fallidos, el backend debe bloquear temporalmente el ID de usuario usando una llave de expiración rápida (p. ej., Redis TTL de 15 minutos).
6. Si la autenticación es exitosa, se genera un JSON Web Token (JWT) stateless firmado digitalmente que encapsula el `usuario_id`, `rol` y `aseguradora_id` (o `null` para Súper Administradores).

---

## 2. Flujo del Cliente (Aplicación Móvil)
**Requerimientos Relacionados:** RF-003, RF-004, RF-005, RF-006, RF-007, RF-012, RF-013, RF-014, RF-015, RF-016, RF-017, RF-018, RF-019, RF-020, RF-021, RF-022, RF-023, RF-024, RF-025, RF-042

### 2.1 Primer Login y Onboarding
* **Condición de Entrada:** El JWT del usuario indica un rol `'Cliente'` y su perfil marca `onboarding_completado = false`.
* **Lógica de Procesamiento:**
  1. **Despliegue Obligatorio de Privacidad:** El cliente no puede consumir ningún endpoint operativo hasta que acepte el Aviso de Privacidad Integral. El endpoint de aceptación (`POST /v1/auth/consentimiento`) debe persistir banderas verdaderas en base de datos para `consentimiento_aviso_privacidad` y `consentimiento_biometria`.
  2. **Procesamiento OCR Asíncrono:** El cliente captura su identificación oficial y la carátula de la póliza física. La app envía las imágenes al backend (`POST /v1/cliente/onboarding/ocr`). El motor OCR extrae de forma automatizada los campos con una precisión mínima del 90%: Nombre Completo, CURP/RFC, Número de Póliza y Vigencia.
  3. **Cifrado Inmediato de Datos Personales:** Antes de insertar los datos extraídos en la base de datos, el backend debe aplicar cifrado simétrico robusto (AES-256) sobre las columnas sensibles (`nombre_completo_cifrado`, `telefono_cifrado`, `curp_rfc_cifrado`).

### 2.2 Reporte e Inteligencia Artificial del Siniestro
* **Condición de Entrada:** El cliente autenticado selecciona "Reportar Siniestro" desde el Dashboard Móvil.
* **Lógica de Procesamiento:**
  1. **Geolocalización:** Se consume `POST /v1/siniestros/inicializar` enviando coordenadas GPS iniciales. El backend abre un expediente en estado `'Reportado'`.
  2. **Validación de Calidad de Fotos (IA):** Cada fotografía tomada se envía al backend (`POST /v1/siniestros/{id}/imagenes`). El servicio de visión artificial auto-hospedado evalúa los metadatos y pixeles en menos de 3 segundos para confirmar enfoque, iluminación y contraste adecuados. Si falla, el backend retorna una excepción indicando el motivo técnico específico del rechazo.
  3. **Detección, Localización y Clasificación:** Las imágenes aprobadas alimentan al motor de IA para detectar zonas afectadas y clasificar tipos de daño (abolladura, rayadura, fractura, rotura de cristal, deformación) con su severidad (bajo, medio, alto).
  4. **Procesamiento de Narración (NLP/Speech-to-Text):** Si el usuario envía una nota de voz, el backend la convierte a texto en español coloquial mexicano. El modelo NLP realiza un análisis semántico (`POST /v1/siniestros/{id}/narracion`) para extraer el mecanismo del accidente y buscar menciones de averías mecánicas internas (humo, ruidos extraños, pérdida de potencia), registrándolas como "Alertas de Daño No Visible" en el expediente técnico.
  5. **Generación del Informe Preliminar:** El backend consolida los daños de la IA, el texto transcrito y calcula un rango de costo de reparación por zona afectada, exponiendo un disclaimer obligatorio que aclara que el diagnóstico es únicamente un apoyo preliminar sujeto a confirmación humana.

---

## 3. Flujo del Ajustador (Aplicación Móvil - Presencial)
**Requerimientos Relacionados:** RF-044, RF-045, RF-046, RF-047

### Flujo de Backend:
1. **Filtro de Casos Asignados:** El endpoint `GET /v1/ajustador/siniestros` recupera exclusivamente los registros donde `ajustador_id == usuario_id` y el estatus general es `'Asignado'`.
2. **Inspección Presencial Obligatoria:** El ajustador se traslada físicamente al punto GPS del choque. Al abrir el siniestro en la app, el backend descarga el modelo de datos tridimensional y las clasificaciones sugeridas por la IA.
3. **Corrección Manual del Peritaje:** El ajustador contrasta el reporte de la IA contra el vehículo físico en sitio. Si hay discrepancias, consume `PUT /v1/ajustador/siniestros/{id}/peritaje` para anular manualmente clasificaciones erróneas o añadir daños mecánicos ocultos para la cámara. El backend registra de manera inmutable en los logs de auditoría cada modificación realizada sobre la predicción original de la IA.
4. **Confirmación y Congelamiento:** El ajustador presiona "Confirmar Peritaje" (`POST /v1/ajustador/siniestros/{id}/confirmar`). El backend cambia de forma inmediata el estatus del siniestro a `'Peritaje Validado'` y congela el expediente técnico bloqueando cualquier edición futura por parte del ajustador.

---

## 4. Flujo de la Aseguradora (Panel Web Administrativo)
**Requerimientos Relacionados:** RF-035, RF-036, RF-037, RF-038, RF-039, RF-040, RF-041, RF-042, RF-043, RF-048, RNF-008

### Flujo de Backend:
1. **Gestión de Catálogo Jerárquico:** Expone servicios CRUD cerrados bajo RBAC (`/v1/aseguradora/ajustadores`, `/v1/aseguradora/clientes`, `/v1/aseguradora/talleres`). Al dar de alta a un ajustador, valida de forma obligatoria su cédula profesional y asocia sus credenciales al tenant de la aseguradora.
2. **Monitoreo en Tiempo Real:** Provee conexiones persistentes (Server-Sent Events o WebSockets) en `GET /v1/aseguradora/siniestros/stream` para actualizar el dashboard web de forma asíncrona ante incidentes entrantes de alta severidad.
3. **Asignación Manual:** El operador de la aseguradora despacha un ajustador disponible usando `POST /v1/siniestros/{id}/asignar-ajustador`. El backend actualiza la relación y gatilla una notificación push instantánea (menos de 5 segundos) al dispositivo móvil del ajustador.
4. **Canalización a Taller y Disociación Legal (LFPDPPP):** Cuando el peritaje del ajustador regresa como validado, la aseguradora selecciona un taller en convenio y ejecuta `POST /v1/siniestros/{id}/enviar-taller`. Aquí el backend ejecuta un proceso técnico de **Disociación Obligatoria**: clona el expediente omitiendo nombres, identificaciones, teléfonos, correos y datos de la póliza del asegurado, transmitiendo a la bandeja del taller únicamente la ficha técnica vehicular (marca, modelo, año, placas/número de serie) y el reporte técnico de daños.

---

## 5. Flujo del Taller / Hojalatería (Panel Web)
**Requerimientos Relacionados:** RF-028, RF-029, RF-030, RF-031, RF-032, RF-033, RF-034, RNF-013

### Flujo de Backend:
1. **Bandeja Unificada Multi-Tenant:** El endpoint `GET /v1/taller/expedientes` permite al operador agrupar y filtrar las órdenes de trabajo recibidas a través de un parámetro query de filtrado según la aseguradora contratante de origen.
2. **Visualización Restringida (Need to Know):** Al acceder al detalle del caso (`GET /v1/taller/expedientes/{id}`), el backend implementa un validador a nivel de controlador que intercepta la petición y asegura que bajo ninguna circunstancia se expongan datos de identidad del cliente, limitando la respuesta a las imágenes marcadas y componentes mecánicos a cotizar.
3. **Gestión del Presupuesto Económico:** El taller introduce los montos monetarios de refacciones y mano de obra a través de `POST /v1/taller/expedientes/{id}/presupuesto`. El backend valida que las entradas sean numéricas positivas y cambia el estado de la cotización interna a `'Pendiente_Aprobacion'`.
   * Si la aseguradora rechaza los costos, el backend habilita de nuevo la edición técnica para el taller.
   * Si la aseguradora aprueba, el estado del siniestro cambia a `'En Reparación'` y se congela el documento presupuestal.
4. **Notificación de Conclusión:** Una vez completadas las reparaciones físicas, el taller consume `POST /v1/taller/expedientes/{id}/concluir`. El backend cambia de manera síncrona el estatus a `'Trabajo Concluido'` y dispara una alerta interna exclusivamente al panel de la aseguradora. Toda comunicación directa entre el rol taller y el rol cliente está estrictamente deshabilitada por diseño a nivel de red y base de datos.

---

## 6. Cierre del Siniestro y Control de Entrega
**Requerimientos Relacionados:** RF-038.1, RF-042, RNF-008

### Flujo de Backend:
1. El personal de la aseguradora evalúa los vehículos marcados como `'Trabajo Concluido'`. Tras la validación interna de calidad, el operador aprueba la salida consumiendo `POST /v1/aseguradora/siniestros/{id}/autorizar-entrega`.
2. El backend procesa la orden de entrega y detona de forma asíncrona un evento (Broker de Mensajería / Workers) que despacha en un tiempo máximo de 5 segundos una notificación push nativa y un correo electrónico estructurado al dispositivo móvil del cliente.
3. El mensaje provee al cliente las instrucciones exactas y la dirección de la sucursal de la aseguradora correspondiente para presentarse a recoger su unidad vehicular de forma segura.

---

## 7. Módulo de Administración de la Plataforma (Auditoría y LFPDPPP Global)
**Requerimientos Relacionados:** RF-043, RF-046, RF-047, RF-048, RF-049, RF-050, RF-051, RF-052, RNF-014, RNF-015

### 7.1 Gestión Jurídica de Derechos ARCO (Aseguradora/Administrador)
* **Endpoint:** `POST /v1/admin/usuarios/{id}/bloqueo-arco`
* **Lógica de Procesamiento:** Ante una solicitud de Cancelación u Oposición de datos, el backend revoca de inmediato todos los tokens JWT activos del usuario afectado. Posteriormente, aplica un cifrado simétrico reforzado sobre sus identificadores personales y los marca con el estado operativo `'Bloqueado por ARCO'`. La información se aísla de las consultas de producción ordinarias y se confina en una tabla restringida únicamente para atender auditorías legales vigentes de las autoridades mexicanas durante el periodo de retención obligatorio prescrito por la ley.

### 7.2 Baja de Aseguradora Corporativa y Respaldo Técnico
* **Endpoint:** `DELETE /v1/admin/aseguradoras/{id}`
* **Lógica de Procesamiento:**
  1. El sistema inicia un proceso en segundo plano (*Background Job*) que compila de manera atómica todo el historial operativo de la organización (usuarios, peritajes analizados por la IA, cotizaciones e imágenes históricas de siniestros).
  2. Genera un contenedor comprimido comprimido y cifrado bajo el algoritmo AES-256.
  3. Almacena temporalmente el archivo en un bucket de almacenamiento seguro y genera un enlace tokenizado de descarga segura con validez de expiración estricta, enviándolo exclusivamente al correo del contacto legal corporativo registrado.
  4. Una vez confirmada la descarga o vencido el plazo, el backend aplica la política de aislamiento definitivo del tenant, bloqueando los accesos de escritura y lectura sobre la base de datos de los servidores de la aseguradora desincorporada.

### 7.3 Bitácora de Auditoría Global e Inmutable
* **Restricción Técnica (Security by Design):** Todas las acciones críticas de los usuarios (inicios de sesión, cambios de presupuesto, modificaciones de peritajes del ajustador o autorizaciones de entrega) deben ser registradas mediante un servicio de logging inmutable. Las inserciones a la tabla de auditoría se realizan de manera estrictamente asíncrona en un formato *Append-Only* (Solo Escritura). El backend debe carecer por completo de endpoints o funciones de base de datos que permitan ejecutar sentencias de actualización (`UPDATE`) o eliminación (`DELETE`) sobre estos registros de auditoría.