# Definición de Módulos del Backend - ClaimVision

Este plan define y organiza los módulos que deben ser desarrollados para la API de ClaimVision v3.0, estructurados bajo los principios de Arquitectura Limpia (Domain-Driven Design / Bounded Contexts) definidos en la documentación técnica del proyecto.

## User Review Required

> [!IMPORTANT]
> El proyecto está organizado utilizando Arquitectura Limpia. Cada módulo propuesto contará con sus carpetas independientes (`domain`, `application`, `infra`, `presentation`) para mantener el desacoplamiento total y permitir el crecimiento modular del backend.

> [!WARNING]
> La base de datos utiliza enums y UUIDs específicos definidos en `ia_utils/database.md`. Todos los módulos nuevos deben mapear sus tablas a través de mappers (`_to_domain`) para evitar fugas de modelos de infraestructura a la capa de dominio.

## Módulos Propuestos y Estructura

En base al [README.md](file:///home/manu/Documentos/Clases/Proyecto Integrador/ClaimVision_Backend/README.md) y al esquema de base de datos en [database.md](file:///home/manu/Documentos/Clases/Proyecto Integrador/ClaimVision_Backend/ia_utils/database.md), se definen los siguientes **8 módulos**:

---

## Arquitectura de Despliegue y Microservicios (SOA)

Para garantizar la fiabilidad, aislamiento de fallos y escalabilidad del sistema, la solución se desacopla en una arquitectura orientada a servicios independientes:

- **Core API Gateway / Backend Transaccional:** Administra la persistencia relacional, control RBAC, gestión de estados del siniestro y orquestación de llamadas.
- **Ecosistema de Inferencia Descentralizado:** Los componentes de IA se dividen en microservicios independientes encapsulados en contenedores Docker dedicados (`service-vision-ai`, `service-speech-to-text`, `service-nlp`, `service-ocr`, `service-estimation`). La comunicación inter-servicio se realizará internamente en la red local mediante protocolos de alta velocidad (gRPC o peticiones HTTP internas), evitando la sobrecarga de dependencias pesadas de Machine Learning en el backend transaccional.

Por lo tanto, nos centraremos en hacer el Core API Gateway en esta entrega.
---

### 1. Módulo de Autenticación y Control de Acceso (`auth`)
* **Estado Actual:** Parcialmente implementado.
* **Acciones Pendientes:**
  - Integrar el bloqueo de intentos fallidos (5 intentos) usando un servicio de caché/Redis (o similar con TTL) en `infra/security`.
  - Integrar la validación y persistencia del consentimiento del aviso de privacidad y biometría en el flujo de registro o mediante un endpoint dedicado (`POST /v1/auth/consentimiento`).
* **Endpoints:**
  - `POST /v1/auth/register` (registro)
  - `POST /v1/auth/login` (login con RBAC)
  - `POST /v1/auth/consentimiento` (consentimiento legal)
  - `GET /v1/auth/me` (perfil del usuario autenticado)
  - `POST /v1/auth/recovery/request` & `/verify` & `/reset` (recuperación de contraseña)

---

### 2. Módulo de Cliente y Onboarding (`cliente`)
* **Descripción:** Administra el proceso de registro inicial del cliente, aceptación de avisos de privacidad, datos generales y procesamiento de OCR para documentos (cédula, póliza) con cifrado de datos personales.
* **Datos Recabados (Payload del Cliente):** Los datos que el backend debe procesar, validar mediante el mapper de infraestructura a dominio y persistir se dividen en:
    * **Datos de Identidad Personal (Tabla `usuarios` - Cifrados con AES-256):**
      - Nombre completo del asegurado.
      - Teléfono de contacto.
      - Correo electrónico (utilizado como identificador único de inicio de sesión).
    * **Datos de la Póliza y Fiscales (Tabla `perfiles_clientes`) (Con o Sin `OCR`):**
      - Número de póliza de seguro vigente.
      - Fecha de vigencia de la póliza (para validación de cobertura en siniestros).
      - Clave CURP o RFC del titular (extraída del documento de identidad escaneado).
    * **Metadatos de Control Regulatorio (LFPDPPP):**
      - Estado de consentimiento del Aviso de Privacidad (`true`/`false`).
      - Estado de consentimiento para el uso de Datos Biométricos (`true`/`false`).
      - Estado de autorización para transferencia disociada a talleres (`true`/`false`).
      - Timestamp exacto de la firma electrónica o aceptación del consentimiento.

* **Componentes clave:**
  - **OCR Asíncrono:** Procesar e identificar imágenes de identificación oficial y carátula de póliza.
  - **Cifrado AES-256:** Cifrado simétrico robusto para las columnas `nombre_completo_cifrado`, `telefono_cifrado`, `curp_rfc_cifrado`, `numero_poliza_cifrado`, `vigencia_poliza_cifrado`, `fecha_firma_consentimiento_cifrado` antes de persistir.
  - **Consentimientos Legales:** Firma de consentimiento de datos y metadatos de control regulatorio - LFPDPPP.
  - **Confirmación de Datos:** Confirmación de datos/persistir datos.
* **Endpoints:**
  - `POST /v1/cliente/onboarding/ocr` (carga de documentos y extracción de datos)
  - `POST /v1/cliente/onboarding/confirmar-consentimientos` (firma de consentimiento de datos y metadatos de control regulatorio - LFPDPPP)
  - `POST /v1/cliente/onboarding/confirmar-datos` (confirmación de datos/persistir datos)

---

### 3. Módulo de Siniestros e Inteligencia Artificial (`siniestro`)

* **Descripción:** Administra el ciclo de vida transaccional completo de un siniestro automovilístico, desde su inicialización geolocalizada por el cliente hasta su validación pericial en sitio y resolución final. Centraliza los servicios de inferencia de los modelos auto-hospedados de visión por computadora y procesamiento de lenguaje natural (NLP).
* **Componentes clave:**
* **Inicialización:** Apertura del expediente técnico con captura de coordenadas GPS in situ.
* **Filtro de Calidad Fotográfica (IA):** Servicio de inferencia síncrono para validar enfoque, iluminación y contraste de las capturas.
* **Análisis de Daños Externos (IA):** Identificación de zonas colisionadas, estimación de severidad (bajo, medio, alto) y pre-clasificación de daños (abolladura, rayadura, fractura, rotura de cristal, deformación).
* **Procesamiento de Narración (NLP):** Transcripción de notas de voz (Speech-to-Text) y extracción semántica en español coloquial mexicano para registrar alertas de daños mecánicos internos (no visibles).
* **Generación de Informe Preliminar:** Consolidación automatizada de costos sugeridos por la IA previo al arribo del perito.
* **Validación e Inmutabilidad Pericial:** Interfaz de control para que el ajustador en sitio corrija y confirme el inventario definitivo de daños, bloqueando el expediente contra futuras modificaciones y auditando cada cambio en la bitácora.

* **Endpoints:**
* `POST /v1/siniestros/inicializar` (Cliente: Abre expediente y guarda coordenadas GPS) 
* `POST /v1/siniestros/{id}/imagenes` (Cliente: Sube fotografías fijas al almacenamiento seguro) 
* `POST /v1/siniestros/{id}/analisis-ia` (Interno: Dispara la inferencia de la IA sobre las imágenes validadas) 
* `POST /v1/siniestros/{id}/narracion` (Cliente: Recibe texto o audio; extrae alertas de daño no visible mediante NLP) 
* `GET /v1/siniestros/{id}/reporte-preliminar` (Cliente/Aseguradora: Recupera el desglose marcado por la IA con su respectivo disclaimer legal) 
* `GET /v1/siniestros/asignados` (Ajustador: Lista de casos asignados exclusivamente a su ID) 
* `PUT /v1/siniestros/{id}/peritaje` (Ajustador: Corrige de forma presencial los componentes, severidades o costos determinados por la IA) 
* `POST /v1/siniestros/{id}/confirmar` (Ajustador: Aplica la firma digital, congela los datos técnicos del siniestro y cambia el estado a 'Peritaje Validado') 

---

### 4. Módulo de la Aseguradora (`aseguradora`)

* **Descripción:** Panel web para administradores y operadores de la aseguradora. Permite administrar jerárquicamente a sus usuarios (clientes, ajustadores, talleres en convenio), monitorear incidentes, despachar ajustadores en sitio, canalizar reparaciones mediante privacidad desde el diseño y ejecutar cierres de siniestros y bloqueos ARCO sobre su red operativa.
* **Componentes clave:**
* **Gestión Jerárquica de la Red:** Operaciones CRUD sobre los perfiles de su red. El alta de ajustadores exige obligatoriamente la captura de su cédula profesional.
* **Monitoreo en Tiempo Real:** Panel unificado que recibe y actualiza el flujo de incidentes de los asegurados sin requerir actualización manual de la interfaz web, incluyendo alertas visuales prioritarias calculadas por la IA para colisiones de alta severidad.
* **Delegación en Sitio:** Asignación manual de siniestros a ajustadores disponibles. El sistema detona una notificación push al dispositivo móvil del ajustador en un lapso no mayor a 5 segundos.
* **Disociación Legal de Datos (LFPDPPP):** Proceso automatizado de canalización hacia el taller receptor. El sistema aplica una política de exclusión técnica, transfiriendo únicamente los reportes fotográficos, el peritaje final y los datos del vehículo, omitiendo los datos de identidad del cliente.
* **Control de Entrega (Cierre de Siniestro):** Validación del estatus de "Trabajo Concluido" emitido por el taller. El operador autoriza la orden de entrega, disparando notificaciones (push y correo electrónico) directamente al asegurado con las instrucciones de recolección.
* **Ejecución de Bloqueos ARCO (Tenant-Level):** Mecanismo para inhabilitar cuentas de clientes o personal que ejerzan derechos de Cancelación u Oposición. El sistema revoca tokens instantáneamente, cifra nombres y direcciones con AES-256 e invisibiliza los datos en reportes históricos y pantallas operativas.

* **Endpoints:**
* `GET/POST/PUT/DELETE /v1/aseguradora/ajustadores` (Operaciones sobre ajustadores, incluyendo captura de cédula profesional).
* `GET/POST/PUT/DELETE /v1/aseguradora/clientes` (Operaciones sobre clientes, incluyendo suspensión de servicios).
* `GET/POST/PUT/DELETE /v1/aseguradora/talleres` (Operaciones sobre talleres en convenio, incluyendo altas y desvinculación).
* `GET /v1/aseguradora/siniestros/stream` (Conexión SSE/WebSockets para el monitoreo pasivo de incidentes entrantes y alertas de severidad).
* `GET /v1/aseguradora/siniestros` (Consulta paginada del historial y seguimiento general de todos los incidentes del tenant).
* `POST /v1/aseguradora/siniestros/{id}/asignar-ajustador` (Ejecuta la relación de la tabla y detona la alerta push al perito).
* `POST /v1/aseguradora/siniestros/{id}/enviar-taller` (Clona y despacha el expediente al taller ejecutando la disociación de identidad por diseño).
* `POST /v1/aseguradora/siniestros/{id}/autorizar-entrega` (Valida la conclusión del trabajo e informa asíncronamente al cliente).
* `POST /v1/aseguradora/usuarios/{id}/bloqueo-arco` (Aplica el cifrado AES-256 y bloqueo normativo sobre un cliente o ajustador específico perteneciente a la aseguradora).

---

### 5. Módulo del Taller / Hojalatería (`taller`)
* **Descripción:** Panel web para que los talleres afiliados coticen, reparen y notifiquen la conclusión de los trabajos.
* **Componentes clave:**
  - Bandeja multi-tenant filtrada por aseguradora de origen.
  - Visualización restringida ("Need to know") sin datos personales del asegurado.
  - Presupuesto económico (refacciones y mano de obra) con control de estados y flujos de aprobación.
  - Notificación de conclusión de reparaciones.
* **Endpoints:**
  - `GET /v1/taller/expedientes` (bandeja de entrada)
  - `GET /v1/taller/expedientes/{id}` (vista restringida técnica)
  - `POST /v1/taller/expedientes/{id}/presupuesto` (carga/modificación de cotización)
  - `POST /v1/taller/expedientes/{id}/concluir` (notificación de fin del trabajo)

---

### 6. Módulo de Cierre y Entrega (`entrega`)
* **Descripción:** Proceso de control de calidad final por parte de la aseguradora y entrega del vehículo al cliente con notificaciones automatizadas.
* **Endpoints:**
  - `POST /v1/aseguradora/siniestros/{id}/autorizar-entrega` (detona evento asíncrono push/correo de recogida)

---

### 7. Módulo de Administración de la Plataforma (`admin` y `auditoria`)
**Descripción:** Panel global de administración centralizada y consola multi-tenant de la plataforma ClaimVision. Administra el ciclo de vida comercial e institucional de las empresas aseguradoras afiliadas, supervisa la vigencia de sus contratos, ejecuta el control normativo de la LFPDPPP (Derechos ARCO) y garantiza la persistencia inmutable de la actividad del ecosistema.
* **Componentes clave:**
* **Gestión Multi-tenant de Aseguradoras:** Alta de nuevas firmas de seguros corporativas, verificación remota de credenciales fiscales y aislamiento de su base de datos (identificador único organizacional).
* **Control de Planes y Suscripciones:** Configuración de planes comerciales, renovación de contratos y un servicio de alertas preventivas que detona al alcanzar el 90% del consumo de peritajes mensuales por IA contratados.
**Bloqueo y Cifrado por Derechos ARCO:** Inhabilitación instantánea de credenciales, revocación de tokens JWT activos y cifrado simétrico (AES-256) de nombres y direcciones de usuarios que ejercen su derecho de Cancelación u Oposición.
**Desincorporación Técnica de Tenants:** *Background Job* asíncrono para la baja definitiva de aseguradoras, compilando su base de datos histórica en un archivo contenedor ZIP cifrado con AES-256, enviando un enlace seguro tokenizado al contacto legal y bloqueando permanentemente el acceso al servidor de origen.
**Bitácora de Auditoría Inmutable:** Servicio de *logging* asíncrono en formato *Append-Only* (Solo Escritura) para registrar inicios de sesión, transacciones y peticiones críticas, careciendo por completo de funciones o endpoints `UPDATE` o `DELETE`.

* **Endpoints:**
* `POST /v1/admin/aseguradoras` (Administrador: Da de alta y registra una nueva aseguradora en la plataforma) 
* `GET /v1/admin/aseguradoras` (Administrador: Lista y filtra las aseguradoras corporativas registradas y sus estatus) 
* `PUT /v1/admin/aseguradoras/{id}/suscripcion` (Administrador: Modifica, renueva o actualiza el plan comercial y límite de peritajes de una aseguradora) 
* `POST /v1/admin/aseguradoras/{id}/verificar` (Administrador: Valida credenciales fiscales e institucionales para activar la cuenta corporativa) 
* `POST /v1/admin/usuarios/{id}/bloqueo-arco` (Administrador/Aseguradora: Aplica el aislamiento, cifrado y suspensión de una cuenta por solicitud ARCO) 
* `DELETE /v1/admin/aseguradoras/{id}` (Administrador: Detona el flujo de baja definitiva, compilación de respaldo cifrado y bloqueo de base de datos) 
* `GET /v1/admin/auditoria/logs` (Administrador: Consulta las bitácoras inmutables de transacciones técnicas de datos del sistema global)
---
## Plan de Ejecución Propuesto

La construcción de los módulos se organiza en el siguiente orden lógico de dependencias transaccionales y de negocio, respetando la unificación de contextos de dominio (DDD):

1. **Módulo de Autenticación y Control de Acceso (`auth`):** Base de la plataforma global. Implementación de criptografía, lógica RBAC básica y persistencia inmediata de los consentimientos legales de la LFPDPPP en la base de datos transaccional.
2. **Módulo de Cliente y Onboarding (`cliente`):** Flujo de entrada de usuarios asegurados. Desarrollo de la extracción OCR local y la capa de cifrado simétrico (AES-256) en infraestructura para blindar la identidad de los registros iniciales.
3. **Módulo de Siniestros e Inteligencia Artificial - Fase 1 (`siniestro`):** Inicialización del core transaccional. Endpoints de apertura del expediente con coordenadas GPS, almacenamiento seguro de archivos fotográficos fijos y control de estados base (`Reportado` -> `Asignado`).
4. **Módulo de Siniestros e Inteligencia Artificial - Fase 2 (`siniestro - Inferencia Local`):** Integración de los pipelines de visión artificial (calidad de imagen, localización de abolladuras/fracturas y severidad) y el modelo local de transcripción de voz con extracción semántica (NLP) para registrar alertas de daños mecánicos internos.
5. **Módulo de Siniestros e Inteligencia Artificial - Fase 3 (`siniestro - Flujo del Perito`):** Incorporación de la lógica pericial sobre el mismo contexto de siniestros. Endpoints de consulta para el ajustador en campo, interfaz de edición manual y firma electrónica para el congelamiento definitivo del peritaje técnico validado.
6. **Módulo de la Aseguradora (`aseguradora`):** Consola web de despacho. Altas de catálogos jerárquicos de usuarios del tenant, asignación manual de ajustadores, canalización automatizada mediante clonación y el microservicio de disociación de identidad hacia los talleres.
7. **Módulo del Taller / Hojalatería (`taller`):** Bandeja multi-tenant protegida bajo el principio de "necesidad de conocer". Flujo de negociación del presupuesto económico (refacciones y mano de obra), control de transiciones de aprobación económica por la aseguradora y notificación física de fin de obra.
8. **Módulo de Cierre y Entrega (`entrega`):** Orquestación del fin del siniestro. Mecanismo de validación por la aseguradora y disparador asíncrono de alertas push/correo hacia el cliente móvil indicando la recolección física.
9. **Módulo de Administración de la Plataforma (`admin` y `auditoria`):** Gobernanza global, consola de administración global multi-tenant, automatización del background job de desincorporación de aseguradoras con dump cifrado, y el servicio de auditoría inmutable en formato append-only (sin sentencias UPDATE/DELETE).

---

## Decisiones Arquitectónicas (Open Questions Resueltas)

1. **Servicio de OCR para Onboarding (`cliente`):** Queda descartado cualquier uso de APIs cloud (Google/Azure). Se implementará un microservicio local e independiente en la capa de infraestructura utilizando **Tesseract OCR** u **EasyOCR** embebido en un contenedor Docker optimizado, exponiendo la extracción de datos al caso de uso de la aplicación mediante gRPC o peticiones HTTP internas.
2. **Procesamiento Speech-to-Text y NLP (`siniestro`):** Se descarta por completo el uso de la API comercial en la nube de OpenAI, Gemini o cualquier proveedor externo, cumpliendo con la restricción de no delegar funcionalidades clave a servicios de terceros. El procesamiento se realizará mediante un componente innovador de PLN local:
   - **Transcripción:** Se utilizará la biblioteca de código abierto `faster-whisper` ejecutada de manera nativa en un contenedor Docker aislado (`infra/inference`). El contenedor alojará localmente los archivos de pesos del modelo (formato parametrizado CTranslate2), realizando la conversión de audio a texto directamente en el hardware del servidor mediante cómputo local.
   - **Extracción Semántica (NLP):** El texto resultante será procesado localmente mediante modelos de Procesamiento de Lenguaje Natural auto-hospedados (utilizando arquitecturas basadas en `spaCy` con pipelines en español o modelos Transformers sintonizados localmente). Este componente se encargará de identificar entidades y registrar de forma autónoma las "Alertas de Daño No Visible" en el lenguaje coloquial mexicano, garantizando que el núcleo de inteligencia artificial sea un desarrollo propio y privado.
3. **Servicio de Visión y Estimación (`service-vision-ai` / `service-estimation`):** Los modelos de detección de daños externos y cálculo de costos se mantendrán en contenedores locales dedicados. La API Gateway enviará las imágenes al servicio de visión para la segmentación de piezas afectadas y el resultado técnico se transferirá al servicio de estimación para mapear los rangos monetarios basados en matrices locales indexadas por marca, año y modelo del auto.
4. **Servicio de Caché y Seguridad (`auth`):** Se confirma el despliegue de **Redis local** como parte de la infraestructura compartida del backend desde el inicio del desarrollo. No se utilizarán soluciones volátiles en la memoria de los controladores de FastAPI, asegurando que el control de los 5 intentos fallidos de login y la lista negra (blacklist) de tokens JWT invalidados por cierre de sesión sean consistentes en una arquitectura SOA escalable y distribuida.

---

## Plan de Verificación

### Automated Tests
- **Pruebas Unitarias (`pytest`):** Cobertura estricta sobre la lógica pura del dominio (`domain/entities`) y las reglas de los casos de uso (`application/usecases`), abstrayendo e inyectando mocks de los repositorios de bases de datos, sistema de archivos e inferencia de IA para aislar los tests de la infraestructura.
- **Pruebas de Integración:** Validación de los mappers (`_to_domain`) y de la persistencia de datos simulando transiciones completas de estados del siniestro.

### Manual Verification
- **Swagger UI (`/docs`):** Verificación directa y exploración de payloads/contratos de datos consumiendo los controladores expuestos de FastAPI a través de la interfaz nativa interactiva y el log de la consola de desarrollo.\
