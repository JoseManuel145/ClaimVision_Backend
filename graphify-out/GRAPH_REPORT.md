# Graph Report - .  (2026-07-13)

## Corpus Check
- 109 files · ~65,397 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2200 nodes · 6658 edges · 160 communities (120 shown, 40 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 836 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Aseguradora CRUD Tests
- Entrega Authorization Flow
- Ajustador Module Ports
- Admin Taller Management
- Taller Expedientes
- Admin Aseguradora Operations
- Vehiculo Management
- Cotizacion Approval & Permissions
- Dano Registration
- Password Recovery Flow
- Siniestro Query Aseguradora
- Ajustador Schemas
- Cliente Management
- Ajustador Tests
- Cliente & Image Operations
- Password Change Flow
- Auth Routes & Exceptions
- IA Bridge Services
- Use Case Initializers
- Taller Operator Management
- Cliente Adapters
- Admin Application Logic
- Siniestro State Transitions
- Error Definitions
- Aseguradora Profile
- Database Architecture
- Core Infrastructure
- PDF Generation
- Ajustador Availability
- HTTP Error Types
- Siniestro DTOs
- Ajustador Profile Update
- Peritaje AI Models
- RBAC Authorization
- Siniestro Assignment List
- OCR Structured Service
- Admin User Repository
- Cliente Tests
- Cotizacion Repository
- Conflict & Auth Errors
- Usuario Creation
- Bloqueo ARCO
- Text Analysis Service
- Taller Profile Update
- Cliente Consent Flow
- Admin Schemas
- Vehiculo Repository Port
- Vehiculo DTOs
- Poliza Data Extraction
- Autorizar Entrega Flow
- App Configuration
- Taller Service Helpers
- Taller Repository
- Taller Cotizacion Helpers
- Admin Subscription & Audit
- Cliente Repository
- Desincorporar Aseguradora
- Admin Dashboard Enums
- Subir Imagen Siniestro
- Ajustador Repository
- Vehiculo Repository
- Cliente Profile Update
- AES Encryption
- Aseguradora Repository
- Cliente Repository Port
- Create Operador Taller
- Login Attempt Tracking
- Process OCR
- Imagen Siniestro Repository
- PDF Storage Port
- Cliente Profile Schemas
- Cliente Repository Impl
- Audio Transcription
- Taller Checker Port
- Taller DTOs
- HTTP Response Helpers
- Usuario Repository
- Cliente V1 Schemas
- Text Extraction Service
- Supabase Client
- Consultar Auditoria
- Get Perfil Cliente
- Extract & Validate Data
- Extract INE Data
- Fake Taller Adapter
- Design Principles
- Architecture Patterns
- List Aseguradoras
- Actualizar Aseguradora
- Registrar Aseguradora
- Crear Operador Aseguradora
- Create Usuario
- Update Usuario
- Predict Damage
- Cliente Negative Tests
- API Module Routing
- Get Aseguradora By ID
- Dashboard Resumen
- Get Taller Admin
- Get Usuario
- List Talleres Admin
- List Usuarios
- Get Dashboard Resumen
- Verificar Aseguradora
- API Module Declarations
- Auth Dependencies
- Account Deletion Flow
- No Content Response
- Test Runner
- List Siniestros Cliente
- Fake OCR Service
- Dual-format OCR
- Docker Infrastructure
- NLP Database Tables
- Purge Aseguradora
- Siniestro Validation Tests
- Siniestro Edge Case Tests
- Siniestro Filter Tests
- Siniestro Pagination Tests
- Siniestro Not Found Tests
- Cliente Onboarding Tests
- Cliente Idempotency Tests
- Consentimiento Tests
- Email Validation
- Aseguradora CRUD API
- Inferences Table
- NLP Jobs Table
- OCR Documents Table
- V2 Predictions Table
- V2 Retrain Jobs Table
- Error AuthUser Rename
- Error bcrypt/passlib
- Error Knowledge Base
- Error ModuleNotFoundError
- Error UUID JSON
- FastAPI Framework
- Cliente Repository Port
- Cliente Repository Port
- DateTime Utilities
- Cliente Repository Port
- Any Type
- Any Type
- Cliente Repository Port
- Any Type
- Upload File

## God Nodes (most connected - your core abstractions)
1. `NotFoundError` - 178 edges
2. `AuthenticatedUser` - 151 edges
3. `BusinessRuleError` - 120 edges
4. `SiniestroModel` - 89 edges
5. `SiniestroRepositoryPort` - 87 edges
6. `SiniestroRepository` - 53 edges
7. `AuditLogRepositoryPort` - 49 edges
8. `UserTable` - 48 edges
9. `AuthRepository` - 47 edges
10. `ForbiddenError` - 46 edges

## Surprising Connections (you probably didn't know these)
- `test_tester_global_bypass_ajustador()` --indirect_call--> `get_current_user()`  [INFERRED]
  tests/ajustador/test_routes.py → src/core/security.py
- `FakeAjustadorAdapter` --uses--> `AjustadorModulePort`  [INFERRED]
  tests/aseguradora/test_crud.py → src/modules/ajustador/domain/ports/ajustador_module_port.py
- `FakeAjustadorModel` --uses--> `AjustadorModulePort`  [INFERRED]
  tests/aseguradora/test_crud.py → src/modules/ajustador/domain/ports/ajustador_module_port.py
- `FakeClienteModel` --uses--> `AjustadorModulePort`  [INFERRED]
  tests/aseguradora/test_crud.py → src/modules/ajustador/domain/ports/ajustador_module_port.py
- `FakeClienteModuleAdapter` --uses--> `AjustadorModulePort`  [INFERRED]
  tests/aseguradora/test_crud.py → src/modules/ajustador/domain/ports/ajustador_module_port.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Siniestro Domain Core (claims processing entities)** — ia_utils_database_siniestros, ia_utils_database_peritajes_ia, ia_utils_database_danos_detectados_ia, ia_utils_database_peritajes_ajustador, ia_utils_database_danos_ajustados_manual, ia_utils_database_imagenes_siniestro, ia_utils_database_cotizaciones_taller [EXTRACTED 1.00]
- **Actor Identity Chain (users → roles → profiles)** — ia_utils_database_usuarios, ia_utils_database_perfiles_clientes, ia_utils_database_ajustadores, ia_utils_database_perfiles_taller_usuarios, ia_utils_database_rol_usuario [EXTRACTED 1.00]
- **IA Microservice Data Tables** — ia_utils_database_inferences, ia_utils_database_nlp_transcripciones, ia_utils_database_nlp_damage_entities, ia_utils_database_nlp_jobs, ia_utils_database_ocr_documents, ia_utils_database_v2_predictions, ia_utils_database_v2_retrain_jobs [EXTRACTED 1.00]
- **Siniestro Lifecycle Flow** — ia_utils_database_md_estatus_siniestro_enum, ia_utils_database_md_siniestros, endpoints_md_cliente, endpoints_md_aseguradora_siniestros, endpoints_md_ajustador, endpoints_md_taller [EXTRACTED 0.85]

## Communities (160 total, 40 thin omitted)

### Community 0 - "Aseguradora CRUD Tests"
Cohesion: 0.04
Nodes (17): FakeAjustadorAdapter, FakeAjustadorModel, FakeClienteModel, FakeClienteModuleAdapter, FakeTallerModel, Pruebas de Aseguradora CRUD v1 (`/api/v1/aseguradora/...`) — ajustadores, client, test_rol_no_operador_rechazado(), wired() (+9 more)

### Community 1 - "Entrega Authorization Flow"
Cohesion: 0.07
Nodes (24): AutorizarEntregaV1, Autorización de entrega por la aseguradora (§3). Corrige la transición respecto, ListSiniestrosAseguradora, ConfirmarPeritaje, AsignarAjustador, EnviarTaller, ListSiniestros, SiniestroModel (+16 more)

### Community 2 - "Ajustador Module Ports"
Cohesion: 0.09
Nodes (23): AjustadorModulePort, Protocol, CreateAjustador, DeleteAjustador, GetAjustador, ListAjustadores, UpdateAjustador, AjustadorModel (+15 more)

### Community 3 - "Admin Taller Management"
Cohesion: 0.08
Nodes (17): ListTalleresAdmin, CreateTaller, DeleteTaller, GetTaller, ListTalleres, UpdateTaller, TallerModel, Protocol (+9 more)

### Community 4 - "Taller Expedientes"
Cohesion: 0.05
Nodes (19): ListExpedientesTallerUseCase, list_expedientes_taller_service(), Tester_Global accede a todos los endpoints de ajustador., test_tester_global_bypass_ajustador(), Pruebas de §3 Aseguradora (`/api/v1/aseguradora/...`) — siniestros + acciones de, test_rol_no_operador_rechazado(), wired(), FakeAjustadorChecker (+11 more)

### Community 5 - "Admin Aseguradora Operations"
Cohesion: 0.08
Nodes (20): ActualizarAseguradoraUseCase, ActualizarSuscripcionUseCase, AplicarBloqueoArcoUseCase, CrearOperadorAseguradoraUseCase, DesincorporarAseguradoraUseCase, GetAseguradoraById, ListAseguradoras, RegistrarAseguradoraUseCase (+12 more)

### Community 6 - "Vehiculo Management"
Cohesion: 0.10
Nodes (18): CreateVehiculo, CreateVehiculoFromPoliza, DeleteVehiculo, GetVehiculo, ListVehiculos, UpdateVehiculo, VehiculoModel, Protocol (+10 more)

### Community 7 - "Cotizacion Approval & Permissions"
Cohesion: 0.12
Nodes (20): ForbiddenError, 403 Forbidden - Usuario autenticado pero sin permisos., AprobarCotizacion, _CotizacionDecisionBase, RechazarCotizacion, CrearCotizacion, EditarCotizacion, ConcluirExpedienteUseCase (+12 more)

### Community 8 - "Dano Registration"
Cohesion: 0.11
Nodes (23): AgregarDano, Any, _to_dano(), EditarPeritaje, GetMiSiniestro, resolver_ajustador_id(), ListMisAsignaciones, _PeritajeEditorBase (+15 more)

### Community 9 - "Password Recovery Flow"
Cohesion: 0.06
Nodes (16): GenerateRecoveryCode, datetime, VerifyRecoveryCode, VerifyUser, Pruebas de Auth v1 (`/api/v1/auth/...`) — registro, login, recovery, consentimie, test_consentimiento(), test_login_cuenta_arco_bloqueada(), test_me_autenticado_devuelve_usuario() (+8 more)

### Community 10 - "Siniestro Query Aseguradora"
Cohesion: 0.11
Nodes (16): GetSiniestroAseguradora, GetSiniestroCliente, Detalle de un siniestro para el cliente dueño, con sus imágenes. Valida la     p, ListSiniestrosCliente, Lista los siniestros del cliente autenticado (filtrados por su perfil)., Registra una imagen ya subida (vía URL prefirmada, §8) en     `imagenes_siniestr, RegistrarImagenSiniestro, ImagenSiniestroModel (+8 more)

### Community 11 - "Ajustador Schemas"
Cohesion: 0.12
Nodes (33): DanoRequest, AjustadorPerfilResponse, AjustadorPerfilUpdateRequest, DisponibilidadRequest, EditarPeritajeRequest, GeolocalizacionRequest, BaseModel, SiniestroDetalleAjustadorDTO (+25 more)

### Community 12 - "Cliente Management"
Cohesion: 0.12
Nodes (14): CreateClienteByAseguradora, GetCliente, ListClientes, ClienteModel, ClienteRepositoryPort, Protocol, ClienteAdapter, _adapter() (+6 more)

### Community 13 - "Ajustador Tests"
Cohesion: 0.06
Nodes (26): Pruebas de §5 Ajustador (`/api/v1/ajustador/...`)., Paginación con valores límite válidos funciona; inválidos dan 422., Filtrar asignaciones por estatus., Página más allá del total debe devolver lista vacía., UUID que no existe debe devolver 404., Peritaje sin firma digital es rechazado (422 por campo requerido)., Peritaje sobre siniestro que no existe → 404., Dos peticiones en paralelo: solo una crea el peritaje. (+18 more)

### Community 14 - "Cliente & Image Operations"
Cohesion: 0.13
Nodes (30): ClienteCheckerAdapter, RegistrarImagenSiniestro, ListVehiculosCliente, ClienteCheckerPort, ConfirmConsent, confirm_consent_service(), ConfirmData, ClienteRepository (+22 more)

### Community 15 - "Password Change Flow"
Cohesion: 0.11
Nodes (17): GenerateRecoveryCode, ChangePassword, ChangePasswordWithCode, RequestPasswordChangeCode, RecoveryCode, RecoveryCodePort, Session, RecoveryCodeService (+9 more)

### Community 16 - "Auth Routes & Exceptions"
Cohesion: 0.11
Nodes (31): HTTPException, LoginUser, ResetPassword, SendRecoveryCode, change_password(), change_password_with_code(), login(), me() (+23 more)

### Community 17 - "IA Bridge Services"
Cohesion: 0.11
Nodes (16): ThirdPartyServiceError, AnalizarService, Any, IaOcrService, Any, OcrStructuredService, Any, PredictService (+8 more)

### Community 18 - "Use Case Initializers"
Cohesion: 0.09
Nodes (13): PurgeAseguradoraUseCase, ReactivarAseguradoraUseCase, AdminPurgeRepositoryPort, AseguradoraRepositoryPort, AuditLogRepositoryPort, DesincorporacionJobPort, AseguradoraTenant, AuditLog (+5 more)

### Community 19 - "Taller Operator Management"
Cohesion: 0.09
Nodes (31): CreateOperadorTallerUseCase, CreateTaller, DeleteTaller, GetTaller, ListSiniestrosAseguradora, ListTalleres, OperadorTallerRequestDTO, listar_siniestros() (+23 more)

### Community 20 - "Cliente Adapters"
Cohesion: 0.16
Nodes (6): datetime, ResetPassword, TokenResult, User, AuthPort, PasswordPort

### Community 22 - "Siniestro State Transitions"
Cohesion: 0.12
Nodes (26): AprobarCotizacion, AsignarAjustador, AsignarAjustadorDTO, AutorizarEntregaV1, EnviarTaller, EnviarTallerDTO, GetSiniestroAseguradora, RechazarCotizacion (+18 more)

### Community 23 - "Error Definitions"
Cohesion: 0.12
Nodes (8): BusinessRuleError, NotFoundError, 404 Not Found - Recurso no encontrado., DeleteUsuario, GetTallerAdmin, AseguradoraTenant, UpdateUsuario, UpdateUsuarioRequestDTO

### Community 24 - "Aseguradora Profile"
Cohesion: 0.12
Nodes (15): ActualizarPerfilAseguradora, GetPerfilAseguradora, actualizar_perfil_aseguradora_service(), get_perfil_aseguradora_service(), Session, PerfilAseguradoraDTO, PerfilAseguradoraUpdateDTO, BaseModel (+7 more)

### Community 25 - "Database Architecture"
Cohesion: 0.11
Nodes (28): PostgreSQL Range Partitioning (logs_auditoria), PostGIS Geography spatial queries, Siniestro Lifecycle State Machine, ajustadores table, aseguradoras table, convenio_aseguradora_taller junction table, cotizaciones_taller table, danos_ajustados_manual table (+20 more)

### Community 26 - "Core Infrastructure"
Cohesion: 0.10
Nodes (18): FastAPI, Logger, get_session(), register_exception_handlers(), get_logger(), Cada módulo llama esto para obtener su logger con nombre jerárquico.     Ejemplo, Configura el sistema de logging de toda la app., setup_logging() (+10 more)

### Community 27 - "PDF Generation"
Cohesion: 0.10
Nodes (18): PdfGeneratorPort, Any, Protocol, PerfilTallerRepository, Session, PerfilTallerUsuariosTable, Base, Any (+10 more)

### Community 28 - "Ajustador Availability"
Cohesion: 0.13
Nodes (19): ActualizarDisponibilidad, AjustadorModel, AjustadorRepositoryPort, ActualizarGeolocalizacion, AjustadorModel, AjustadorRepositoryPort, actualizar_perfil_ajustador_service(), agregar_dano_service() (+11 more)

### Community 29 - "HTTP Error Types"
Cohesion: 0.08
Nodes (14): BadGatewayError, BadRequestError, InternalServerError, MethodNotAllowedError, 400 Bad Request - Datos inválidos: campos faltantes o formato incorrecto., 401 Unauthorized - Token ausente o inválido., 405 Method Not Allowed - Méthodo no permitido en el endpoint., 422 Unprocessable Entity - Error de validación de datos. (+6 more)

### Community 30 - "Siniestro DTOs"
Cohesion: 0.21
Nodes (23): AsignarAjustadorDTO, EnviarTallerDTO, BaseModel, RechazarCotizacionRequest, SiniestroDetalleAseguradoraDTO, PeritajeResponseDTO, SiniestroResponseDTO, actualizar_perfil() (+15 more)

### Community 31 - "Ajustador Profile Update"
Cohesion: 0.11
Nodes (8): ActualizarPerfilAjustador, GetPerfilAjustador, Pruebas de perfil del ajustador (GET + PUT /api/v1/ajustador/perfil)., test_perfil_rol_no_ajustador_rechazado(), wired(), default_ajustador(), FakeAjustadorRepo, Fakes del módulo Ajustador.

### Community 32 - "Peritaje AI Models"
Cohesion: 0.18
Nodes (14): DanoAjustadoManualModel, PeritajeAjustadorModel, PeritajeAjustadorRepositoryPort, AdminPurgeRepository, Session, ConvenioAseguradoraTallerTable, Base, _dano_to_domain() (+6 more)

### Community 33 - "RBAC Authorization"
Cohesion: 0.13
Nodes (18): Factory de dependencia para RBAC. Devuelve una dependencia que valida que el, require_roles(), listar_asignaciones(), §5 · Siniestros asignados a mí (paginado)., listar_ajustadores(), ClienteCreateDTO, ClienteResponseDTO, BaseModel (+10 more)

### Community 34 - "Siniestro Assignment List"
Cohesion: 0.17
Nodes (10): ListSiniestrosAsignados, Session, SiniestroRepositoryPort, SiniestroRepository, _to_domain(), Base, SiniestroTable, confirmar_peritaje_service() (+2 more)

### Community 35 - "OCR Structured Service"
Cohesion: 0.12
Nodes (9): OcrStructuredPort, CreateVehicleFromPoliza, OcrStructuredPort, ClienteRepositoryPort, OcrStructuredPort, ClienteProfile, Protocol, ConfirmDataRequestDTO (+1 more)

### Community 36 - "Admin User Repository"
Cohesion: 0.16
Nodes (8): AdminUserRepository, Session, _user_to_dict(), AuthRepository, Session, _to_domain(), Base, UserTable

### Community 37 - "Cliente Tests"
Cohesion: 0.09
Nodes (10): Pruebas de §4 Cliente (`/api/v1/cliente/...`) — siniestros + onboarding., Mismo payload dos veces → 201 ambos, IDs distintos., Paginación con valores límite válidos funciona; inválidos dan 422., URL vacía debe ser aceptada o rechazada elegantemente., test_listar_siniestros_paginacion_extrema(), test_onboarding_rol_no_cliente_rechazado(), test_put_perfil_rol_no_cliente_rechazado(), test_registrar_imagen_url_invalida() (+2 more)

### Community 38 - "Cotizacion Repository"
Cohesion: 0.20
Nodes (13): CotizacionRepositoryPort, CotizacionTallerModel, aprobar_cotizacion_service(), autorizar_entrega_service(), get_siniestro_service(), list_siniestros_service(), Session, rechazar_cotizacion_service() (+5 more)

### Community 39 - "Conflict & Auth Errors"
Cohesion: 0.15
Nodes (9): ConflictError, 409 Conflict - Conflicto de estado, p. ej. registro duplicado., LoginUser, RegisterUser, VerifyToken, TokenPayload, TokenPort, JwtTokenService (+1 more)

### Community 40 - "Usuario Creation"
Cohesion: 0.13
Nodes (6): CreateUsuario, Session, GetUsuario, ListUsuarios, AdminUserRepositoryPort, Any

### Community 41 - "Bloqueo ARCO"
Cohesion: 0.19
Nodes (10): BloqueoArcoAseguradora, DesbloqueoArcoAseguradora, Any, Protocol, UsuarioRepositoryPort, bloqueo_arco_service(), desbloqueo_arco_service(), aplicar_bloqueo_arco() (+2 more)

### Community 42 - "Text Analysis Service"
Cohesion: 0.15
Nodes (8): AnalyzeText, Any, AnalizarPort, OcrStructuredPort, PredictPort, Any, Protocol, analyze_text()

### Community 43 - "Taller Profile Update"
Cohesion: 0.13
Nodes (8): ActualizarPerfilTaller, GetPerfilTaller, FakePerfilTallerRepo, Fakes del módulo Taller., _make_taller(), Pruebas de perfil del taller (GET + PUT /api/v1/taller/perfil)., test_rol_no_taller_rechazado(), wired()

### Community 44 - "Cliente Consent Flow"
Cohesion: 0.14
Nodes (18): ConsentimientosRequest, actualizar_consentimientos(), confirmar_datos(), crear_vehiculo_desde_poliza(), detalle_siniestro(), ocr_extraction(), AuditLogger, GetSiniestroCliente (+10 more)

### Community 45 - "Admin Schemas"
Cohesion: 0.20
Nodes (16): AseguradoraRequestDTO, AseguradoraResponseDTO, AuditResponse, CreateUsuarioRequestDTO, DashboardResumenDTO, EstatusCountDTO, OperadorAseguradoraRequestDTO, PaginatedResponse (+8 more)

### Community 46 - "Vehiculo Repository Port"
Cohesion: 0.14
Nodes (9): Protocol, VehiculoRepositoryPort, §4 · Reporte preliminar → estatus = Reportado_Preliminar., reportar_siniestro(), InicializarSiniestro, ClienteCheckerPort, SiniestroRepositoryPort, inicializar_siniestro_service() (+1 more)

### Community 47 - "Vehiculo DTOs"
Cohesion: 0.24
Nodes (16): BaseModel, VehiculoCreateDTO, VehiculoResponseDTO, VehiculoUpdateDTO, actualizar_vehiculo(), crear_vehiculo(), crear_vehiculo_desde_poliza(), eliminar_vehiculo() (+8 more)

### Community 48 - "Poliza Data Extraction"
Cohesion: 0.19
Nodes (13): ExtractPolizaData, Any, OcrStructuredPort, extract_poliza_service(), extract_and_validate(), extract_poliza(), UploadFile, transcribe_audio() (+5 more)

### Community 49 - "Autorizar Entrega Flow"
Cohesion: 0.16
Nodes (12): AutorizarEntrega, AjustadorCheckerAdapter, ClienteCheckerAdapter, ClienteRepositoryPort, asignar_ajustador_service(), autorizar_entrega_service(), get_ajustador_checker(), get_cliente_checker() (+4 more)

### Community 50 - "App Configuration"
Cohesion: 0.14
Nodes (7): BaseSettings, Config, Settings, SendRecoveryCode, EmailPort, Protocol, EmailService

### Community 51 - "Taller Service Helpers"
Cohesion: 0.12
Nodes (17): actualizar_perfil_taller_service(), concluir_trabajo_service(), crear_cotizacion_service(), editar_cotizacion_service(), get_orden_service(), get_perfil_taller_service(), list_ordenes_service(), listo_entrega_service() (+9 more)

### Community 52 - "Taller Repository"
Cohesion: 0.28
Nodes (7): Session, TallerRepository, _to_domain(), Base, TallerTable, TallerModel, TallerRepositoryPort

### Community 53 - "Taller Cotizacion Helpers"
Cohesion: 0.15
Nodes (16): concluir_trabajo(), crear_cotizacion(), editar_cotizacion(), listo_entrega(), AuditLogger, ConcluirExpedienteUseCase, CrearCotizacion, EditarCotizacion (+8 more)

### Community 54 - "Admin Subscription & Audit"
Cohesion: 0.20
Nodes (11): ActualizarSuscripcionUseCase, AplicarBloqueoArcoUseCase, AuditLogTable, DeleteUsuario, AuditLogRepository, AuditLog, Session, _to_domain() (+3 more)

### Community 55 - "Cliente Repository"
Cohesion: 0.32
Nodes (6): ClienteModel, ClienteRepository, Session, _to_domain(), PerfilClienteTable, Base

### Community 56 - "Desincorporar Aseguradora"
Cohesion: 0.17
Nodes (15): DesincorporarAseguradoraUseCase, actualizar_suscripcion(), aplicar_bloqueo_arco(), desincorporar_aseguradora(), eliminar_usuario(), purgar_aseguradora(), AuditLogger, Request (+7 more)

### Community 57 - "Admin Dashboard Enums"
Cohesion: 0.28
Nodes (7): Enum, EstadoUsuario, EstatusComercialAseguradora, PlanSuscripcion, Rol, SeveridadDano, TipoDano

### Community 58 - "Subir Imagen Siniestro"
Cohesion: 0.17
Nodes (8): SubirImagenSiniestro, Protocol, Sube un archivo y retorna su URL pública., StoragePort, Client, SupabaseStorageAdapter, get_storage_port(), subir_imagen_siniestro_service()

### Community 59 - "Ajustador Repository"
Cohesion: 0.32
Nodes (6): _format_wkt(), _parse_wkt(), AjustadorModel, _to_domain(), AjustadorTable, Base

### Community 60 - "Vehiculo Repository"
Cohesion: 0.31
Nodes (5): Session, _to_domain(), VehiculoRepository, Base, VehiculoTable

### Community 61 - "Cliente Profile Update"
Cohesion: 0.23
Nodes (5): ActualizarPerfilCliente, ClienteProfile, default_cliente_profile(), FakeClienteRepo, Fakes del módulo Cliente.

### Community 62 - "AES Encryption"
Cohesion: 0.23
Nodes (10): AESGCM, decrypt_aes256(), encrypt_aes256(), _get_aesgcm(), Cifra un texto utilizando AES-256-GCM. Retorna string base64., Descifra un texto cifrado con AES-256-GCM desde string base64., decrypt_fields(), encrypt_fields() (+2 more)

### Community 63 - "Aseguradora Repository"
Cohesion: 0.40
Nodes (6): AseguradoraRepository, AseguradoraTenant, Session, _to_domain(), AseguradoraTable, Base

### Community 64 - "Cliente Repository Port"
Cohesion: 0.18
Nodes (6): ClienteRepositoryPort, _adapter(), Session, _adapter(), Session, PasswordService

### Community 65 - "Create Operador Taller"
Cohesion: 0.29
Nodes (7): CreateOperadorTallerUseCase, crear_operador_taller_service(), OperadorTallerRequestDTO, BaseModel, TallerCreateDTO, TallerResponseDTO, TallerUpdateDTO

### Community 67 - "Process OCR"
Cohesion: 0.27
Nodes (4): ProcessOcr, OcrStructuredPort, ClienteOcrStructuredService, process_ocr_service()

### Community 68 - "Imagen Siniestro Repository"
Cohesion: 0.36
Nodes (5): ImagenSiniestroRepository, Session, _to_domain(), ImagenSiniestroTable, Base

### Community 69 - "PDF Storage Port"
Cohesion: 0.24
Nodes (5): PdfStoragePort, Protocol, Client, SupabasePdfStorage, get_pdf_storage()

### Community 70 - "Cliente Profile Schemas"
Cohesion: 0.25
Nodes (9): PerfilClienteResponse, PerfilClienteUpdateRequest, actualizar_perfil(), get_perfil(), _perfil_completo(), ActualizarPerfilCliente, GetPerfilCliente, §4 · Perfil del cliente (numero_poliza, vigencia_poliza, consentimientos). (+1 more)

### Community 71 - "Cliente Repository Impl"
Cohesion: 0.44
Nodes (4): ClienteProfile, _to_domain(), ClienteProfileTable, Base

### Community 72 - "Audio Transcription"
Cohesion: 0.28
Nodes (4): Any, TranscribeAudio, TranscribirPort, transcribe_status()

### Community 73 - "Taller Checker Port"
Cohesion: 0.28
Nodes (4): Protocol, TallerCheckerPort, TallerCheckerAdapter, enviar_taller_service()

### Community 74 - "Taller DTOs"
Cohesion: 0.39
Nodes (8): CotizacionTallerDTO, DanoAjustadoDTO, ExpedienteTecnicoResponseDTO, GuardarPresupuestoRequestDTO, MessageResponseDTO, PeritajeAjustadorTecnicoDTO, BaseModel, SiniestroTecnicoDTO

### Community 75 - "HTTP Response Helpers"
Cohesion: 0.29
Nodes (8): JSONResponse, accepted_response(), created_response(), Any, 201 Created - Respuesta al crear un recurso. Se puede incluir Location., 202 Accepted - El trabajo fue aceptado para procesamiento asíncrono., 200 OK - Respuesta genérica con payload JSON., success_response()

### Community 76 - "Usuario Repository"
Cohesion: 0.36
Nodes (3): Session, UsuarioRepository, usuario_repo()

### Community 77 - "Cliente V1 Schemas"
Cohesion: 0.39
Nodes (7): ConsentimientosRequest, PerfilClienteResponse, PerfilClienteUpdateRequest, BaseModel, RegistrarImagenRequest, SiniestroDetalleClienteDTO, TimelineItemDTO

### Community 78 - "Text Extraction Service"
Cohesion: 0.29
Nodes (4): ExtractText, Any, OcrPort, extract_text()

### Community 79 - "Supabase Client"
Cohesion: 0.29
Nodes (6): AsyncClient, get_supabase_async_client(), get_supabase_client(), Client, Obtiene o crea la instancia global del cliente Supabase asíncrono., Obtiene o crea la instancia global del cliente Supabase.

### Community 80 - "Consultar Auditoria"
Cohesion: 0.29
Nodes (5): ConsultarAuditoriaUseCase, AuditLog, consultar_auditoria(), §6 · Consultar logs de auditoría (paginado)., consultar_auditoria_service()

### Community 81 - "Get Perfil Cliente"
Cohesion: 0.29
Nodes (5): GetPerfilCliente, ClienteRepositoryPort, Devuelve el perfil de cliente (`perfiles_clientes`) del usuario autenticado., Tester_Global accede a todos los endpoints de cliente., test_tester_global_bypass_cliente()

### Community 82 - "Extract & Validate Data"
Cohesion: 0.29
Nodes (4): ExtractAndValidateData, Any, OcrStructuredPort, extract_and_validate_service()

### Community 83 - "Extract INE Data"
Cohesion: 0.29
Nodes (5): ExtractIneData, Any, OcrStructuredPort, extract_ine_service(), extract_ine()

### Community 85 - "Design Principles"
Cohesion: 0.40
Nodes (6): Dependency Inversion Principle (SOLID D), Domain Ports (abc.ABC interfaces), FastAPI Depends() DI system, Hexagonal Architecture (Ports and Adapters), Error #1: Circular Import solved by Dependency Inversion, Error #9: Cross-module import between ia_bridge, cliente, aseguradora

### Community 86 - "Architecture Patterns"
Cohesion: 0.40
Nodes (6): Async/Await Pattern, Clean Architecture, Data Mapper Pattern, Dependency Inversion Pattern, Hexagonal Module Structure, Multi-Tenancy Pattern

### Community 87 - "List Aseguradoras"
Cohesion: 0.33
Nodes (6): ListAseguradoras, listar_aseguradoras(), listar_aseguradoras_desincorporadas(), §5 · Listar aseguradoras registradas (paginado, con filtro de baja)., §5 · Listar únicamente aseguradoras desincorporadas (baja lógica)., list_aseguradoras_service()

### Community 88 - "Actualizar Aseguradora"
Cohesion: 0.40
Nodes (5): ActualizarAseguradoraUseCase, actualizar_aseguradora(), §5 · Actualizar datos de una aseguradora existente., actualizar_aseguradora_service(), UpdateAseguradoraDTO

### Community 89 - "Registrar Aseguradora"
Cohesion: 0.40
Nodes (5): AseguradoraRequestDTO, RegistrarAseguradoraUseCase, §5 · Registrar una nueva aseguradora en la plataforma., registrar_aseguradora(), registrar_aseguradora_service()

### Community 90 - "Crear Operador Aseguradora"
Cohesion: 0.40
Nodes (5): CrearOperadorAseguradoraUseCase, OperadorAseguradoraRequestDTO, crear_operador_aseguradora(), §5 · Crear un operador para una aseguradora específica., crear_operador_aseguradora_service()

### Community 91 - "Create Usuario"
Cohesion: 0.40
Nodes (5): CreateUsuario, CreateUsuarioRequestDTO, crear_usuario(), Crear un nuevo usuario con cualquier rol., create_usuario_service()

### Community 92 - "Update Usuario"
Cohesion: 0.40
Nodes (5): actualizar_usuario(), Actualizar datos de un usuario existente., update_usuario_service(), UpdateUsuario, UpdateUsuarioRequestDTO

### Community 93 - "Predict Damage"
Cohesion: 0.40
Nodes (3): PredictDamage, Any, predict_damage()

### Community 94 - "Cliente Negative Tests"
Cohesion: 0.40
Nodes (3): test_detalle_de_otro_cliente_prohibido(), test_reportar_sin_onboarding_falla(), FakeClienteChecker

### Community 95 - "API Module Routing"
Cohesion: 0.67
Nodes (4): Admin API Module, Auth API Module, Cliente API Module, Account Deletion Plan

### Community 96 - "Get Aseguradora By ID"
Cohesion: 0.50
Nodes (4): GetAseguradoraById, obtener_aseguradora(), §5 · Obtener detalle de una aseguradora por ID., get_aseguradora_by_id_service()

### Community 97 - "Dashboard Resumen"
Cohesion: 0.50
Nodes (4): GetDashboardResumen, obtener_dashboard_resumen(), KPIs globales del sistema., get_dashboard_resumen_service()

### Community 98 - "Get Taller Admin"
Cohesion: 0.50
Nodes (4): GetTallerAdmin, obtener_taller_admin(), Obtener detalle de un taller con aseguradoras vinculadas., get_taller_admin_service()

### Community 99 - "Get Usuario"
Cohesion: 0.50
Nodes (4): GetUsuario, obtener_usuario(), Obtener detalle de un usuario por ID., get_usuario_service()

### Community 100 - "List Talleres Admin"
Cohesion: 0.50
Nodes (4): ListTalleresAdmin, listar_talleres_admin(), Listar todos los talleres del sistema (sin filtro por aseguradora)., list_talleres_admin_service()

### Community 101 - "List Usuarios"
Cohesion: 0.50
Nodes (4): ListUsuarios, listar_usuarios(), Listar usuarios con paginación y filtros., list_usuarios_service()

### Community 103 - "Verificar Aseguradora"
Cohesion: 0.50
Nodes (4): §5 · Marcar aseguradora como verificada., verificar_aseguradora(), verificar_aseguradora_service(), VerificarAseguradoraUseCase

### Community 104 - "API Module Declarations"
Cohesion: 0.67
Nodes (3): Ajustador API Module, Aseguradora Siniestros API, Taller API Module

### Community 105 - "Auth Dependencies"
Cohesion: 0.67
Nodes (3): HTTPAuthorizationCredentials, get_current_user(), Dependencia para obtener el usuario autenticado.     Lanza UnauthorizedError si

### Community 106 - "Account Deletion Flow"
Cohesion: 0.67
Nodes (3): POST /auth/eliminacion-cuenta/confirmar, GenerateRecoveryCode Reuse, POST /auth/eliminacion-cuenta/solicitar

### Community 107 - "No Content Response"
Cohesion: 0.67
Nodes (3): Response, no_content_response(), 204 No Content - Respuesta sin cuerpo (p. ej. DELETE exitoso).

### Community 109 - "List Siniestros Cliente"
Cohesion: 0.67
Nodes (3): listar_mis_siniestros(), ListSiniestrosCliente, §4 · Mis siniestros (paginado).

## Knowledge Gaps
- **27 isolated node(s):** `Admin API Module`, `Ajustador API Module`, `Taller API Module`, `Aseguradora CRUD API`, `POST /auth/eliminacion-cuenta/confirmar` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuthenticatedUser` connect `Taller Operator Management` to `Aseguradora CRUD Tests`, `Ajustador Module Ports`, `Admin Taller Management`, `Taller Expedientes`, `Admin Aseguradora Operations`, `Dano Registration`, `Password Recovery Flow`, `Ajustador Schemas`, `Ajustador Tests`, `Cliente & Image Operations`, `Auth Routes & Exceptions`, `Use Case Initializers`, `Cliente Adapters`, `Admin Application Logic`, `Siniestro State Transitions`, `Aseguradora Profile`, `Core Infrastructure`, `Siniestro DTOs`, `Ajustador Profile Update`, `RBAC Authorization`, `Cliente Tests`, `Bloqueo ARCO`, `Text Analysis Service`, `Taller Profile Update`, `Cliente Consent Flow`, `Vehiculo Repository Port`, `Vehiculo DTOs`, `Poliza Data Extraction`, `Taller Cotizacion Helpers`, `Desincorporar Aseguradora`, `AES Encryption`, `Cliente Profile Schemas`, `Audio Transcription`, `Text Extraction Service`, `Consultar Auditoria`, `Get Perfil Cliente`, `Extract INE Data`, `List Aseguradoras`, `Actualizar Aseguradora`, `Registrar Aseguradora`, `Crear Operador Aseguradora`, `Create Usuario`, `Update Usuario`, `Predict Damage`, `Get Aseguradora By ID`, `Dashboard Resumen`, `Get Taller Admin`, `Get Usuario`, `List Talleres Admin`, `List Usuarios`, `Verificar Aseguradora`, `Auth Dependencies`, `List Siniestros Cliente`, `Cliente Onboarding Tests`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `NotFoundError` connect `Error Definitions` to `Entrega Authorization Flow`, `Ajustador Module Ports`, `Admin Taller Management`, `Admin Aseguradora Operations`, `Vehiculo Management`, `Cotizacion Approval & Permissions`, `Dano Registration`, `Siniestro Query Aseguradora`, `Ajustador Schemas`, `Cliente Management`, `Cliente & Image Operations`, `Auth Routes & Exceptions`, `Use Case Initializers`, `Cliente Adapters`, `Admin Application Logic`, `Siniestro State Transitions`, `Aseguradora Profile`, `Ajustador Availability`, `HTTP Error Types`, `Siniestro DTOs`, `Ajustador Profile Update`, `Siniestro Assignment List`, `OCR Structured Service`, `Admin User Repository`, `Usuario Creation`, `Bloqueo ARCO`, `Taller Profile Update`, `Autorizar Entrega Flow`, `Taller Repository`, `Cliente Repository`, `Subir Imagen Siniestro`, `Ajustador Repository`, `Vehiculo Repository`, `Cliente Profile Update`, `Aseguradora Repository`, `Cliente Repository Impl`, `Get Perfil Cliente`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `BusinessRuleError` connect `Error Definitions` to `Entrega Authorization Flow`, `Ajustador Module Ports`, `Admin Taller Management`, `Taller Expedientes`, `Admin Aseguradora Operations`, `Vehiculo Management`, `Cotizacion Approval & Permissions`, `Dano Registration`, `Siniestro Query Aseguradora`, `Cliente Management`, `Cliente & Image Operations`, `Auth Routes & Exceptions`, `Use Case Initializers`, `Cliente Adapters`, `Admin Application Logic`, `Siniestro State Transitions`, `Ajustador Availability`, `HTTP Error Types`, `OCR Structured Service`, `Conflict & Auth Errors`, `Usuario Creation`, `Bloqueo ARCO`, `Vehiculo Repository Port`, `Autorizar Entrega Flow`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 54 inferred relationships involving `NotFoundError` (e.g. with `ActualizarAseguradoraUseCase` and `ActualizarSuscripcionUseCase`) actually correct?**
  _`NotFoundError` has 54 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `BusinessRuleError` (e.g. with `ActualizarAseguradoraUseCase` and `AplicarBloqueoArcoUseCase`) actually correct?**
  _`BusinessRuleError` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `SiniestroModel` (e.g. with `GetMiSiniestro` and `ListMisAsignaciones`) actually correct?**
  _`SiniestroModel` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `SiniestroRepositoryPort` (e.g. with `GetMiSiniestro` and `ListMisAsignaciones`) actually correct?**
  _`SiniestroRepositoryPort` has 27 INFERRED edges - model-reasoned connections that need verification._