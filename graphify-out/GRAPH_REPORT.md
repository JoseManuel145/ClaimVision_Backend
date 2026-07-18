# Graph Report - .  (2026-07-18)

## Corpus Check
- 317 files · ~67,088 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2093 nodes · 7094 edges · 98 communities (95 shown, 3 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 847 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Daños y Siniestros
- Logging y Config
- CRUD Clientes
- Auth y Passwords
- Inicializar Siniestro
- Admin Aseguradora Routes
- Casos de Uso Admin
- Ajustador Module
- Errores de Negocio
- Vehículos y Perfil Cliente
- CRUD Talleres Admin
- Peritajes y Daños
- Errores 403/404
- Asignaciones Ajustador
- Recuperación Contraseña
- Aseguradora Use Cases
- Cotizaciones Taller
- Tests Ajustador
- Excepciones FastAPI
- Tests Aseguradora CRUD
- Config
- Admin Operaciones
- Auditoría
- NotFound Error
- Disponibilidad Ajustador
- Admin User Repo
- Perfil Aseguradora
- Supabase Cliente
- Taller Admin CRUD
- Errores Terceros
- Dashboard
- Auth Routes
- Auth Repos
- Errores HTTP Base
- OCR y Datos Póliza
- Perfil Cliente
- Vehículo Repo
- Siniestros Asignados
- Análisis de Texto
- CRUD Usuarios
- Perfil Ajustador
- CRUD Vehículos
- Update Vehículo
- PDF Generator Port
- Vehículo desde Póliza
- DB Session
- Audit Log Repo
- Conflict Error
- Crear Ajustador
- Get Perfil Cliente
- Router Principal
- Admin Purge
- Taller DTO
- Consentimiento
- Recovery Code
- Ajustador Repo
- Perfil Taller Repo
- Eliminar Ajustador
- Vehículo SQL Repo
- OCR Service
- Usuario SQL Repo
- Tests Perfil Ajustador
- PDF Storage Port
- Cotización Repo
- Desincorporar Aseguradora
- Login Attempt
- Auth Dependencies
- Security Crypto
- Taller Cotización DTO
- HTTP Responses
- Usuario Port
- Transcripción Audio
- Fake Ajustador Repo
- Delete Usuario
- INE Data Extraction
- Text Extraction
- Damage Prediction
- Get Vehículo
- No Content Response

## God Nodes (most connected - your core abstractions)
1. `NotFoundError` - 182 edges
2. `AuthenticatedUser` - 154 edges
3. `BusinessRuleError` - 129 edges
4. `SiniestroRepositoryPort` - 95 edges
5. `SiniestroModel` - 89 edges
6. `AuditLogger` - 62 edges
7. `AuditLog` - 61 edges
8. `AjustadorModel` - 58 edges
9. `SiniestroRepository` - 53 edges
10. `AuditLogRepositoryPort` - 51 edges

## Surprising Connections (you probably didn't know these)
- `FakeCotizacionRepo` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py
- `FakeSiniestroRepo` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py
- `test_tester_global_bypass_ajustador()` --indirect_call--> `get_current_user()`  [INFERRED]
  tests/ajustador/test_routes.py → src/core/security.py
- `FakeAseguradoraTenant` --uses--> `ActualizarAseguradoraUseCase`  [INFERRED]
  tests/admin/test_routes.py → src/modules/admin/application/actualizar_aseguradora.py
- `FakeDesincorporacionJob` --uses--> `ActualizarAseguradoraUseCase`  [INFERRED]
  tests/admin/test_routes.py → src/modules/admin/application/actualizar_aseguradora.py

## Import Cycles
- 1-file cycle: `src/core/supabase.py -> src/core/supabase.py`

## Communities (98 total, 3 thin omitted)

### Community 0 - "Daños y Siniestros"
Cohesion: 0.06
Nodes (72): DanoRequest, Factory de dependencia para RBAC. Devuelve una dependencia que valida que el, require_roles(), AjustadorPerfilResponse, AjustadorPerfilUpdateRequest, DisponibilidadRequest, EditarPeritajeRequest, GeolocalizacionRequest (+64 more)

### Community 1 - "Logging y Config"
Cohesion: 0.05
Nodes (33): Logger, get_logger(), Configura el sistema de logging de toda la app., Cada módulo llama esto para obtener su logger con nombre jerárquico.     Ejemplo, setup_logging(), get_siniestro_notifier(), Session, FastAPI (+25 more)

### Community 2 - "CRUD Clientes"
Cohesion: 0.07
Nodes (28): UpdateCliente, ClienteModel, ClienteRepositoryPort, Protocol, ClienteAdapter, ClienteRepositoryPort, ClienteRepository, ClienteRepositoryPort (+20 more)

### Community 3 - "Auth y Passwords"
Cohesion: 0.08
Nodes (19): ChangePassword, ChangePasswordWithCode, GenerateRecoveryCode, LoginUser, RegisterUser, RequestPasswordChangeCode, ResetPassword, VerifyToken (+11 more)

### Community 4 - "Inicializar Siniestro"
Cohesion: 0.04
Nodes (38): InicializarSiniestro, inicializar_siniestro_service(), Pruebas de §4 Cliente (`/api/v1/cliente/...`) — siniestros + onboarding., 422 si faltan campos obligatorios en el reporte., Acepta strings largos, SQL injection, años extremos., Mismo payload dos veces → 201 ambos, IDs distintos., Paginación con valores límite válidos funciona; inválidos dan 422., Filtrar por estatus existente e inexistente. (+30 more)

### Community 5 - "Admin Aseguradora Routes"
Cohesion: 0.09
Nodes (52): HTTPException, actualizar_aseguradora(), actualizar_suscripcion(), actualizar_usuario(), aplicar_bloqueo_arco(), crear_operador_aseguradora(), crear_usuario(), desincorporar_aseguradora() (+44 more)

### Community 6 - "Casos de Uso Admin"
Cohesion: 0.06
Nodes (18): AplicarBloqueoArcoUseCase, CrearOperadorAseguradoraUseCase, RegistrarAseguradoraUseCase, VerificarAseguradoraUseCase, crear_operador_aseguradora_service(), registrar_aseguradora_service(), verificar_aseguradora_service(), FakeAseguradoraTenant (+10 more)

### Community 7 - "Ajustador Module"
Cohesion: 0.10
Nodes (21): AjustadorModulePort, Protocol, CreateAjustador, DeleteAjustador, GetAjustador, ListAjustadores, UpdateAjustador, CreateClienteByAseguradora (+13 more)

### Community 8 - "Errores de Negocio"
Cohesion: 0.05
Nodes (14): BusinessRuleError, 409 Conflict - Conflicto de estado, p. ej. registro duplicado., AsignarAjustador, EditarSiniestro, EnviarTaller, Tester_Global accede a todos los endpoints de ajustador., test_tester_global_bypass_ajustador(), Pruebas de §3 Aseguradora (`/api/v1/aseguradora/...`) — siniestros + acciones de (+6 more)

### Community 9 - "Vehículos y Perfil Cliente"
Cohesion: 0.09
Nodes (37): ListVehiculosCliente, ActualizarPerfilCliente, CreateVehicleFromPoliza, actualizar_perfil_cliente_service(), _cliente_checker(), cliente_checker_service(), confirm_consent_service(), create_vehicle_from_poliza_service() (+29 more)

### Community 10 - "CRUD Talleres Admin"
Cohesion: 0.10
Nodes (18): CreateTaller, CreateOperadorTallerUseCase, DeleteTaller, GetTaller, ListTalleres, UpdateTaller, TallerModel, TallerAdapter (+10 more)

### Community 11 - "Peritajes y Daños"
Cohesion: 0.10
Nodes (23): AgregarDano, Any, _to_dano(), EditarPeritaje, resolver_ajustador_id(), _PeritajeEditorBase, Any, RegistrarPeritaje (+15 more)

### Community 12 - "Errores 403/404"
Cohesion: 0.09
Nodes (17): ForbiddenError, 403 Forbidden - Usuario autenticado pero sin permisos., ActualizarPerfilTaller, CrearCotizacion, EditarCotizacion, ConcluirExpedienteUseCase, ListExpedientesTallerUseCase, MarcarListoEntrega (+9 more)

### Community 13 - "Asignaciones Ajustador"
Cohesion: 0.09
Nodes (12): ListMisAsignaciones, AutorizarEntregaV1, ListSiniestrosAseguradora, ConfirmarPeritaje, AutorizarEntrega, ListSiniestros, SiniestroModel, Protocol (+4 more)

### Community 14 - "Recuperación Contraseña"
Cohesion: 0.06
Nodes (15): SendRecoveryCode, VerifyRecoveryCode, VerifyUser, Pruebas de Auth v1 (`/api/v1/auth/...`) — registro, login, recovery, consentimie, test_consentimiento(), test_login_cuenta_arco_bloqueada(), test_me_autenticado_devuelve_usuario(), test_recovery_request() (+7 more)

### Community 15 - "Aseguradora Use Cases"
Cohesion: 0.11
Nodes (17): ActualizarAseguradoraUseCase, ActualizarSuscripcionUseCase, GetAseguradoraById, ListAseguradoras, ReactivarAseguradoraUseCase, AseguradoraTenant, AseguradoraRepositoryPort, AseguradoraRepository (+9 more)

### Community 16 - "Cotizaciones Taller"
Cohesion: 0.12
Nodes (15): AprobarCotizacion, _CotizacionDecisionBase, RechazarCotizacion, aprobar_cotizacion_service(), autorizar_entrega_service(), get_siniestro_service(), list_siniestros_service(), Session (+7 more)

### Community 17 - "Tests Ajustador"
Cohesion: 0.06
Nodes (27): Pruebas de §5 Ajustador (`/api/v1/ajustador/...`)., Paginación con valores límite válidos funciona; inválidos dan 422., Filtrar asignaciones por estatus., Página más allá del total debe devolver lista vacía., UUID que no existe debe devolver 404., Peritaje sin firma digital es rechazado (422 por campo requerido)., Peritaje sobre siniestro que no existe → 404., Dos peticiones en paralelo: solo una crea el peritaje. (+19 more)

### Community 18 - "Excepciones FastAPI"
Cohesion: 0.17
Nodes (14): Enum, FastAPI, register_exception_handlers(), Autorización de entrega por la aseguradora (§3). Corrige la transición respecto, EstatusSiniestro, PlanSuscripcion, SeveridadDano, TipoDano (+6 more)

### Community 19 - "Tests Aseguradora CRUD"
Cohesion: 0.06
Nodes (5): Pruebas de Aseguradora CRUD v1 (`/api/v1/aseguradora/...`) — ajustadores, client, test_rol_no_operador_rechazado(), FakeTallerCrudRepo, FakeUsuarioRepo, Fakes del módulo Aseguradora (CRUD: ajustadores, clientes, talleres, usuarios).

### Community 20 - "Config"
Cohesion: 0.10
Nodes (22): BaseSettings, Config, Settings, _adapter(), Session, AuthRepository, Session, Session (+14 more)

### Community 21 - "Admin Operaciones"
Cohesion: 0.19
Nodes (7): ConsultarAuditoriaUseCase, CreateUsuario, PurgeAseguradoraUseCase, AuditLog, AuditLogRepositoryPort, consultar_auditoria_service(), create_usuario_service()

### Community 22 - "Auditoría"
Cohesion: 0.11
Nodes (32): consultar_auditoria(), listar_aseguradoras(), listar_aseguradoras_desincorporadas(), listar_talleres_admin(), listar_usuarios(), §5 · Listar aseguradoras registradas (paginado, con filtro de baja)., §5 · Listar únicamente aseguradoras desincorporadas (baja lógica)., §6 · Consultar logs de auditoría (paginado). (+24 more)

### Community 23 - "NotFound Error"
Cohesion: 0.16
Nodes (10): NotFoundError, 404 Not Found - Recurso no encontrado., GetMiSiniestro, GetSiniestroAseguradora, Registra una imagen ya subida (vía URL prefirmada, §8) en     `imagenes_siniestr, RegistrarImagenSiniestro, ImagenSiniestroModel, ImagenSiniestroRepositoryPort (+2 more)

### Community 24 - "Disponibilidad Ajustador"
Cohesion: 0.14
Nodes (7): ActualizarDisponibilidad, ActualizarGeolocalizacion, AjustadorModel, AjustadorRepositoryPort, Protocol, default_ajustador(), Fakes del módulo Ajustador.

### Community 25 - "Admin User Repo"
Cohesion: 0.11
Nodes (9): _user_to_dict(), User, _to_domain(), Base, UserTable, EstadoUsuario, Rol, encrypt_fields() (+1 more)

### Community 26 - "Perfil Aseguradora"
Cohesion: 0.12
Nodes (15): ActualizarPerfilAseguradora, GetPerfilAseguradora, actualizar_perfil_aseguradora_service(), get_perfil_aseguradora_service(), Session, PerfilAseguradoraDTO, PerfilAseguradoraUpdateDTO, BaseModel (+7 more)

### Community 27 - "Supabase Cliente"
Cohesion: 0.11
Nodes (20): AsyncClient, get_supabase_async_client(), get_supabase_client(), Client, Obtiene o crea la instancia global del cliente Supabase asíncrono., Obtiene o crea la instancia global del cliente Supabase., SubirImagenSiniestro, Protocol (+12 more)

### Community 28 - "Taller Admin CRUD"
Cohesion: 0.09
Nodes (10): GetTallerAdmin, ListTalleresAdmin, get_taller_admin_service(), list_talleres_admin_service(), Protocol, TallerRepositoryPort, Protocol, TallerCheckerPort (+2 more)

### Community 29 - "Errores Terceros"
Cohesion: 0.13
Nodes (13): 502 Bad Gateway - Error en un servicio de terceros., ThirdPartyServiceError, AnalizarService, Any, IaOcrService, Any, PredictService, Any (+5 more)

### Community 30 - "Dashboard"
Cohesion: 0.15
Nodes (11): GetDashboardResumen, Session, get_dashboard_resumen_service(), Session, TallerRepository, _to_domain(), ConvenioAseguradoraTallerTable, Base (+3 more)

### Community 31 - "Auth Routes"
Cohesion: 0.13
Nodes (22): change_password(), change_password_with_code(), delete_device_token(), login(), Request, register(), register_device_token(), request_recovery() (+14 more)

### Community 32 - "Auth Repos"
Cohesion: 0.11
Nodes (11): wired(), FakeAuthRepo, FakeUser, Fakes del módulo Auth., Minimal User domain model para pruebas., FakePerfilTallerRepo, Fakes del módulo Taller., _make_taller() (+3 more)

### Community 33 - "Errores HTTP Base"
Cohesion: 0.08
Nodes (14): BadGatewayError, BadRequestError, InternalServerError, MethodNotAllowedError, 400 Bad Request - Datos inválidos: campos faltantes o formato incorrecto., 401 Unauthorized - Token ausente o inválido., 405 Method Not Allowed - Méthodo no permitido en el endpoint., 422 Unprocessable Entity - Error de validación de datos. (+6 more)

### Community 34 - "OCR y Datos Póliza"
Cohesion: 0.13
Nodes (19): ExtractAndValidateData, Any, OcrStructuredPort, ExtractPolizaData, Any, OcrStructuredPort, extract_and_validate_service(), extract_poliza_service() (+11 more)

### Community 35 - "Perfil Cliente"
Cohesion: 0.17
Nodes (10): ClienteProfile, ClienteRepositoryPort, OcrStructuredPort, Protocol, ClienteRepository, ClienteRepositoryPort, Session, _to_domain() (+2 more)

### Community 36 - "Vehículo Repo"
Cohesion: 0.14
Nodes (8): VehiculoModel, Protocol, VehiculoRepositoryPort, ClienteRepositoryPort, VehiculoAdapter, _adapter(), create_vehiculo_from_poliza_service(), Session

### Community 37 - "Siniestros Asignados"
Cohesion: 0.17
Nodes (10): ListSiniestrosAsignados, Session, SiniestroRepository, _to_domain(), Base, SiniestroTable, confirmar_peritaje_service(), guardar_peritaje_service() (+2 more)

### Community 38 - "Análisis de Texto"
Cohesion: 0.15
Nodes (8): AnalyzeText, Any, AnalizarPort, OcrStructuredPort, Any, Protocol, TranscribirPort, analyze_text()

### Community 39 - "CRUD Usuarios"
Cohesion: 0.13
Nodes (7): GetUsuario, ListUsuarios, UpdateUsuario, AdminUserRepositoryPort, Any, get_usuario_service(), list_usuarios_service()

### Community 40 - "Perfil Ajustador"
Cohesion: 0.20
Nodes (14): ActualizarPerfilAjustador, GetPerfilAjustador, actualizar_perfil_ajustador_service(), agregar_dano_service(), disponibilidad_service(), editar_peritaje_service(), geolocalizacion_service(), get_perfil_ajustador_service() (+6 more)

### Community 41 - "CRUD Vehículos"
Cohesion: 0.17
Nodes (6): CreateVehiculo, DeleteVehiculo, ListVehiculos, create_vehiculo_service(), delete_vehiculo_service(), list_vehiculos_service()

### Community 42 - "Update Vehículo"
Cohesion: 0.11
Nodes (9): ClienteRepositoryPort, OcrStructuredPort, UpdateVehiculo, Protocol, VehiculoModulePort, update_vehiculo_service(), ClienteRepositoryPort, ClienteRepositoryPort (+1 more)

### Community 43 - "PDF Generator Port"
Cohesion: 0.14
Nodes (15): PdfGeneratorPort, Any, Protocol, Any, ReportLabPdfGenerator, concluir_expediente_service(), get_cotizacion_repo(), get_expediente_taller_service() (+7 more)

### Community 44 - "Vehículo desde Póliza"
Cohesion: 0.20
Nodes (15): CreateVehiculoFromPoliza, BaseModel, VehiculoCreateDTO, VehiculoResponseDTO, VehiculoUpdateDTO, actualizar_vehiculo(), crear_vehiculo(), crear_vehiculo_desde_poliza() (+7 more)

### Community 45 - "DB Session"
Cohesion: 0.16
Nodes (10): get_session(), ConfirmData, ProcessOcr, OcrStructuredPort, confirmar_datos(), §1 · Confirmar datos del onboarding: guardar perfil + registrar vehículo., confirm_data_service(), process_ocr_service() (+2 more)

### Community 46 - "Audit Log Repo"
Cohesion: 0.19
Nodes (11): AdminUserRepository, Session, AuditLogRepository, Session, _to_domain(), AuditLogTable, Base, aplicar_bloqueo_arco_service() (+3 more)

### Community 47 - "Conflict Error"
Cohesion: 0.25
Nodes (9): ConflictError, 409 Conflict - Conflicto de estado, p. ej. registro duplicado., _dano_to_domain(), _peritaje_to_domain(), PeritajeAjustadorRepository, Session, DanosAjustadosManualTable, PeritajeAjustadorTable (+1 more)

### Community 48 - "Crear Ajustador"
Cohesion: 0.21
Nodes (12): AjustadorCreateDTO, AjustadorResponseDTO, AjustadorUpdateDTO, BaseModel, actualizar_ajustador(), crear_ajustador(), eliminar_ajustador(), obtener_ajustador() (+4 more)

### Community 49 - "Get Perfil Cliente"
Cohesion: 0.16
Nodes (14): GetPerfilCliente, ClienteRepositoryPort, Devuelve el perfil de cliente (`perfiles_clientes`) del usuario autenticado., actualizar_perfil(), get_perfil(), _perfil_completo(), §4 · Perfil del cliente (numero_poliza, vigencia_poliza, consentimientos)., §4 · Actualiza datos personales del cliente (nombre, email, teléfono). (+6 more)

### Community 50 - "Router Principal"
Cohesion: 0.17
Nodes (11): Router canónico `/api/v1` con prefijos por rol., aplicar_bloqueo_arco(), aplicar_desbloqueo_arco(), Request, client_ip(), get_audit_logger(), Any, Request (+3 more)

### Community 51 - "Admin Purge"
Cohesion: 0.20
Nodes (7): AdminPurgeRepository, Session, _to_domain(), ImagenSiniestroTable, Base, PerfilTallerUsuariosTable, Base

### Community 52 - "Taller DTO"
Cohesion: 0.29
Nodes (13): OperadorTallerRequestDTO, BaseModel, TallerCreateDTO, TallerResponseDTO, TallerUpdateDTO, actualizar_taller(), crear_operador_taller(), crear_taller() (+5 more)

### Community 53 - "Consentimiento"
Cohesion: 0.14
Nodes (13): ConfirmConsent, ClienteRepositoryPort, ConsentRequestDTO, actualizar_consentimientos(), ocr_extraction(), Request, UploadFile, §4 · Reporte preliminar → estatus = Reportado_Preliminar. (+5 more)

### Community 54 - "Recovery Code"
Cohesion: 0.18
Nodes (6): datetime, datetime, RecoveryCode, _to_domain(), Base, RecoveryCodeTable

### Community 55 - "Ajustador Repo"
Cohesion: 0.25
Nodes (7): _format_wkt(), _parse_wkt(), _to_domain(), AjustadorTable, Base, decrypt_fields(), Toma un dict con campos cifrados (nombre_completo_cifrado, telefono_cifrado)

### Community 56 - "Perfil Taller Repo"
Cohesion: 0.30
Nodes (12): PerfilTallerRepository, Session, actualizar_perfil_taller_service(), concluir_trabajo_service(), crear_cotizacion_service(), editar_cotizacion_service(), get_orden_service(), get_perfil_taller_service() (+4 more)

### Community 57 - "Eliminar Ajustador"
Cohesion: 0.20
Nodes (6): AjustadorAdapter, create_ajustador_service(), delete_ajustador_service(), get_ajustador_service(), list_ajustadores_service(), update_ajustador_service()

### Community 58 - "Vehículo SQL Repo"
Cohesion: 0.31
Nodes (5): Session, _to_domain(), VehiculoRepository, Base, VehiculoTable

### Community 59 - "OCR Service"
Cohesion: 0.23
Nodes (5): ClienteOcrStructuredService, OcrStructuredService, Any, Response, ia_ocr_structured_service()

### Community 60 - "Usuario SQL Repo"
Cohesion: 0.26
Nodes (6): Session, UUID, UsuarioRepository, bloqueo_arco_service(), desbloqueo_arco_service(), usuario_repo()

### Community 61 - "Tests Perfil Ajustador"
Cohesion: 0.18
Nodes (3): Pruebas de perfil del ajustador (GET + PUT /api/v1/ajustador/perfil)., test_perfil_rol_no_ajustador_rechazado(), FakeAjustadorRepo

### Community 62 - "PDF Storage Port"
Cohesion: 0.20
Nodes (6): PdfStoragePort, Protocol, Sube PDFs a Supabase Storage usando HTTP directo (httpx).     No depende de stor, SupabasePdfStorage, get_pdf_storage(), subir_pdf_service()

### Community 63 - "Cotización Repo"
Cohesion: 0.33
Nodes (5): CotizacionRepository, Session, _to_domain(), CotizacionTallerTable, Base

### Community 64 - "Desincorporar Aseguradora"
Cohesion: 0.22
Nodes (5): DesincorporarAseguradoraUseCase, AdminPurgeRepositoryPort, DesincorporacionJobPort, Protocol, DesincorporacionJobService

### Community 66 - "Auth Dependencies"
Cohesion: 0.28
Nodes (7): HTTPAuthorizationCredentials, get_current_user(), Dependencia para obtener el usuario autenticado.     Lanza UnauthorizedError si, client(), make_user(), NoopAudit, Bootstrap de pruebas. No requiere base de datos ni servicios externos: se inyect

### Community 67 - "Security Crypto"
Cohesion: 0.36
Nodes (7): decrypt_aes256_legacy(), decrypt_xsalsa20(), encrypt_xsalsa20(), _get_xsalsa20_key(), Cifra un texto utilizando XSalsa20-Poly1305 (NaCl). Retorna string base64., Descifra un texto cifrado con XSalsa20-Poly1305 desde string base64., Descifra datos legacy cifrados con AES-256-GCM (fallback).

### Community 68 - "Taller Cotización DTO"
Cohesion: 0.39
Nodes (8): CotizacionTallerDTO, DanoAjustadoDTO, ExpedienteTecnicoResponseDTO, GuardarPresupuestoRequestDTO, MessageResponseDTO, PeritajeAjustadorTecnicoDTO, BaseModel, SiniestroTecnicoDTO

### Community 69 - "HTTP Responses"
Cohesion: 0.29
Nodes (8): JSONResponse, accepted_response(), created_response(), Any, 201 Created - Respuesta al crear un recurso. Se puede incluir Location., 202 Accepted - El trabajo fue aceptado para procesamiento asíncrono., 200 OK - Respuesta genérica con payload JSON., success_response()

### Community 70 - "Usuario Port"
Cohesion: 0.25
Nodes (3): Any, Protocol, UsuarioRepositoryPort

### Community 71 - "Transcripción Audio"
Cohesion: 0.29
Nodes (4): Any, TranscribeAudio, transcribir_service(), transcribe_status()

### Community 73 - "Delete Usuario"
Cohesion: 0.38
Nodes (3): DeleteUsuario, Session, delete_usuario_service()

### Community 74 - "INE Data Extraction"
Cohesion: 0.29
Nodes (5): ExtractIneData, Any, OcrStructuredPort, extract_ine_service(), extract_ine()

### Community 75 - "Text Extraction"
Cohesion: 0.33
Nodes (3): ExtractText, Any, OcrPort

### Community 76 - "Damage Prediction"
Cohesion: 0.33
Nodes (3): PredictDamage, Any, PredictPort

### Community 78 - "No Content Response"
Cohesion: 0.67
Nodes (3): no_content_response(), Response, 204 No Content - Respuesta sin cuerpo (p. ej. DELETE exitoso).

## Knowledge Gaps
- **2 isolated node(s):** `Config`, `TokenResult`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuthenticatedUser` connect `Auditoría` to `Daños y Siniestros`, `CRUD Clientes`, `Auth y Passwords`, `Inicializar Siniestro`, `Admin Aseguradora Routes`, `Casos de Uso Admin`, `Ajustador Module`, `Errores de Negocio`, `Vehículos y Perfil Cliente`, `Peritajes y Daños`, `Errores 403/404`, `Recuperación Contraseña`, `Tests Ajustador`, `Tests Aseguradora CRUD`, `Perfil Aseguradora`, `Auth Routes`, `Auth Repos`, `OCR y Datos Póliza`, `Análisis de Texto`, `Vehículo desde Póliza`, `DB Session`, `Crear Ajustador`, `Get Perfil Cliente`, `Router Principal`, `Taller DTO`, `Consentimiento`, `Tests Perfil Ajustador`, `Auth Dependencies`, `Security Crypto`, `Transcripción Audio`, `INE Data Extraction`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `NotFoundError` connect `NotFound Error` to `Daños y Siniestros`, `CRUD Clientes`, `Admin Aseguradora Routes`, `Casos de Uso Admin`, `Ajustador Module`, `Errores de Negocio`, `Vehículos y Perfil Cliente`, `CRUD Talleres Admin`, `Peritajes y Daños`, `Errores 403/404`, `Asignaciones Ajustador`, `Aseguradora Use Cases`, `Cotizaciones Taller`, `Excepciones FastAPI`, `Config`, `Admin Operaciones`, `Disponibilidad Ajustador`, `Admin User Repo`, `Perfil Aseguradora`, `Supabase Cliente`, `Taller Admin CRUD`, `Dashboard`, `Errores HTTP Base`, `Perfil Cliente`, `Vehículo Repo`, `Siniestros Asignados`, `CRUD Usuarios`, `Perfil Ajustador`, `Vehículo desde Póliza`, `DB Session`, `Get Perfil Cliente`, `Consentimiento`, `Ajustador Repo`, `Eliminar Ajustador`, `Vehículo SQL Repo`, `Desincorporar Aseguradora`, `Delete Usuario`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `BusinessRuleError` connect `Errores de Negocio` to `Daños y Siniestros`, `CRUD Clientes`, `Inicializar Siniestro`, `Admin Aseguradora Routes`, `Casos de Uso Admin`, `Ajustador Module`, `Vehículos y Perfil Cliente`, `CRUD Talleres Admin`, `Peritajes y Daños`, `Errores 403/404`, `Asignaciones Ajustador`, `Aseguradora Use Cases`, `Cotizaciones Taller`, `Excepciones FastAPI`, `Admin Operaciones`, `NotFound Error`, `Disponibilidad Ajustador`, `Admin User Repo`, `Errores HTTP Base`, `Vehículo Repo`, `CRUD Usuarios`, `Vehículo desde Póliza`, `DB Session`, `Consentimiento`, `Eliminar Ajustador`, `Delete Usuario`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 55 inferred relationships involving `NotFoundError` (e.g. with `ActualizarAseguradoraUseCase` and `ActualizarSuscripcionUseCase`) actually correct?**
  _`NotFoundError` has 55 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `BusinessRuleError` (e.g. with `ActualizarAseguradoraUseCase` and `AplicarBloqueoArcoUseCase`) actually correct?**
  _`BusinessRuleError` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `SiniestroRepositoryPort` (e.g. with `GetMiSiniestro` and `ListMisAsignaciones`) actually correct?**
  _`SiniestroRepositoryPort` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `SiniestroModel` (e.g. with `GetMiSiniestro` and `ListMisAsignaciones`) actually correct?**
  _`SiniestroModel` has 26 INFERRED edges - model-reasoned connections that need verification._