# Graph Report - .  (2026-07-11)

## Corpus Check
- 256 files · ~54,333 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1790 nodes · 6041 edges · 89 communities (80 shown, 9 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 756 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Siniestro Assignment & Delivery
- Quote Approval Workflow
- Siniestro Lifecycle Core
- Workshop Quote Management
- Workshop Administration
- Admin CRUD Operations
- Insurer Profile Management
- Exception Handling Layer
- Adjuster Field Operations
- Adjuster Test Suite
- Adjuster Domain Ports
- Client Test Suite
- Admin Use Cases
- Auth Verification Flow
- Admin Dashboard & Repos
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 54
- Community 55
- Community 56
- Community 57
- Community 58
- Community 59
- Community 60
- Community 61
- Community 62
- Community 63
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79

## God Nodes (most connected - your core abstractions)
1. `NotFoundError` - 148 edges
2. `AuthenticatedUser` - 127 edges
3. `BusinessRuleError` - 106 edges
4. `SiniestroRepositoryPort` - 95 edges
5. `SiniestroModel` - 89 edges
6. `AuditLog` - 58 edges
7. `AjustadorModel` - 58 edges
8. `AuditLogger` - 54 edges
9. `SiniestroRepository` - 51 edges
10. `PeritajeAjustadorModel` - 49 edges

## Surprising Connections (you probably didn't know these)
- `FakeAjustadorChecker` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py
- `FakeCotizacionRepo` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py
- `FakeImagenRepo` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py
- `FakeSiniestroRepo` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py
- `FakeTallerChecker` --uses--> `BusinessRuleError`  [INFERRED]
  tests/fakes/siniestro.py → src/core/exceptions.py

## Import Cycles
- 1-file cycle: `src/core/supabase.py -> src/core/supabase.py`

## Hyperedges (group relationships)
- **Siniestro Lifecycle Flow** — ia_utils_database_md_estatus_siniestro_enum, ia_utils_database_md_siniestros, endpoints_md_cliente, endpoints_md_aseguradora_siniestros, endpoints_md_ajustador, endpoints_md_taller [EXTRACTED 0.85]
- **Claims Core Domain Tables** — ia_utils_database_md_siniestros, ia_utils_database_md_peritajes_ia, ia_utils_database_md_peritajes_ajustador, ia_utils_database_md_cotizaciones_taller, ia_utils_database_md_ajustadores [EXTRACTED 0.90]
- **Error Registry Driving Architecture Patterns** — ia_utils_error_registry_md_circular_import, ia_utils_error_registry_md_column_mismatch, ia_utils_error_registry_md_enum_casing, ia_utils_error_registry_md_uuid_serialization, ia_utils_error_registry_md_table_redefinition, ia_utils_architecture_md_dependency_inversion, ia_utils_architecture_md_data_mapper, ia_utils_architecture_md_hexagonal_modules [INFERRED 0.75]

## Communities (89 total, 9 thin omitted)

### Community 0 - "Siniestro Assignment & Delivery"
Cohesion: 0.07
Nodes (21): Autorización de entrega por la aseguradora (§3). Corrige la transición respecto, ConfirmarPeritaje, InicializarSiniestro, ListSiniestrosCliente, Lista los siniestros del cliente autenticado (filtrados por su perfil)., ListSiniestros, SiniestroModel, ClienteCheckerPort (+13 more)

### Community 1 - "Quote Approval Workflow"
Cohesion: 0.06
Nodes (29): AprobarCotizacion, _CotizacionDecisionBase, RechazarCotizacion, AutorizarEntregaV1, GetSiniestroAseguradora, ListSiniestrosAseguradora, aprobar_cotizacion_service(), autorizar_entrega_service() (+21 more)

### Community 2 - "Siniestro Lifecycle Core"
Cohesion: 0.06
Nodes (29): BusinessRuleError, 409 Conflict - Conflicto de estado, p. ej. registro duplicado., AsignarAjustador, AutorizarEntrega, EditarSiniestro, EnviarTaller, AjustadorCheckerPort, Protocol (+21 more)

### Community 3 - "Workshop Quote Management"
Cohesion: 0.08
Nodes (20): CrearCotizacion, EditarCotizacion, ConcluirExpedienteUseCase, ExpedienteTecnicoResult, GetExpedienteTallerUseCase, ListExpedientesTallerUseCase, MarcarListoEntrega, §6 · Trabajo_Concluido → Listo_Para_Entrega. (+12 more)

### Community 4 - "Workshop Administration"
Cohesion: 0.08
Nodes (18): ListTalleresAdmin, list_talleres_admin_service(), CreateTaller, GetTaller, ListTalleres, UpdateTaller, TallerModel, Protocol (+10 more)

### Community 5 - "Admin CRUD Operations"
Cohesion: 0.07
Nodes (49): HTTPException, ActualizarAseguradoraUseCase, CreateUsuario, actualizar_aseguradora(), actualizar_suscripcion(), actualizar_usuario(), aplicar_bloqueo_arco(), consultar_auditoria() (+41 more)

### Community 6 - "Insurer Profile Management"
Cohesion: 0.07
Nodes (19): ActualizarPerfilAseguradora, GetPerfilAseguradora, actualizar_perfil_aseguradora_service(), get_perfil_aseguradora_service(), Session, PerfilAseguradoraDTO, PerfilAseguradoraUpdateDTO, BaseModel (+11 more)

### Community 7 - "Exception Handling Layer"
Cohesion: 0.15
Nodes (11): NotFoundError, FastAPI, 404 Not Found - Recurso no encontrado., register_exception_handlers(), GetTallerAdmin, PurgeAseguradoraUseCase, UpdateUsuario, AuditLog (+3 more)

### Community 8 - "Adjuster Field Operations"
Cohesion: 0.13
Nodes (19): ForbiddenError, 403 Forbidden - Usuario autenticado pero sin permisos., Any, _to_dano(), GetMiSiniestro, resolver_ajustador_id(), _PeritajeEditorBase, Any (+11 more)

### Community 9 - "Adjuster Test Suite"
Cohesion: 0.06
Nodes (30): Pruebas de §5 Ajustador (`/api/v1/ajustador/...`)., Paginación con valores límite válidos funciona; inválidos dan 422., Filtrar asignaciones por estatus., Página más allá del total debe devolver lista vacía., UUID que no existe debe devolver 404., Peritaje sin firma digital es rechazado (422 por campo requerido)., Peritaje sobre siniestro que no existe → 404., Dos peticiones en paralelo: solo una crea el peritaje. (+22 more)

### Community 10 - "Adjuster Domain Ports"
Cohesion: 0.13
Nodes (18): AjustadorModulePort, Protocol, CreateAjustador, DeleteAjustador, GetAjustador, ListAjustadores, UpdateAjustador, CreateClienteByAseguradora (+10 more)

### Community 11 - "Client Test Suite"
Cohesion: 0.05
Nodes (26): Pruebas de §4 Cliente (`/api/v1/cliente/...`) — siniestros + onboarding., 422 si faltan campos obligatorios en el reporte., Acepta strings largos, SQL injection, años extremos., Mismo payload dos veces → 201 ambos, IDs distintos., Paginación con valores límite válidos funciona; inválidos dan 422., Filtrar por estatus existente e inexistente., Página más allá del total debe devolver lista vacía., UUID que no existe debe devolver 404. (+18 more)

### Community 12 - "Admin Use Cases"
Cohesion: 0.08
Nodes (13): AplicarBloqueoArcoUseCase, ConsultarAuditoriaUseCase, RegistrarAseguradoraUseCase, VerificarAseguradoraUseCase, §5 · Registrar una nueva aseguradora en la plataforma., registrar_aseguradora(), AseguradoraRequestDTO, FakeAseguradoraTenant (+5 more)

### Community 13 - "Auth Verification Flow"
Cohesion: 0.07
Nodes (13): VerifyRecoveryCode, VerifyUser, verify_code(), verify_recovery_code_service(), Pruebas de Auth v1 (`/api/v1/auth/...`) — registro, login, recovery, consentimie, test_consentimiento(), test_me_autenticado_devuelve_usuario(), test_recovery_verify() (+5 more)

### Community 14 - "Admin Dashboard & Repos"
Cohesion: 0.10
Nodes (25): GetDashboardResumen, Session, AseguradoraRepository, Session, AuditLogRepository, Session, _to_domain(), AuditLogTable (+17 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (16): GetSiniestroCliente, Detalle de un siniestro para el cliente dueño, con sus imágenes. Valida la     p, Registra una imagen ya subida (vía URL prefirmada, §8) en     `imagenes_siniestr, RegistrarImagenSiniestro, SubirImagenSiniestro, ImagenSiniestroModel, ImagenSiniestroRepositoryPort, Protocol (+8 more)

### Community 16 - "Community 16"
Cohesion: 0.13
Nodes (30): DanoRequest, AjustadorPerfilResponse, AjustadorPerfilUpdateRequest, DisponibilidadRequest, EditarPeritajeRequest, GeolocalizacionRequest, BaseModel, SiniestroDetalleAjustadorDTO (+22 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (12): ActualizarSuscripcionUseCase, DesincorporarAseguradoraUseCase, GetAseguradoraById, ListAseguradoras, AseguradoraTenant, AdminPurgeRepositoryPort, AseguradoraRepositoryPort, DesincorporacionJobPort (+4 more)

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (26): get_session(), AsignarAjustadorDTO, EnviarTallerDTO, BaseModel, RechazarCotizacionRequest, SiniestroDetalleAseguradoraDTO, detalle_siniestro(), Session (+18 more)

### Community 19 - "Community 19"
Cohesion: 0.11
Nodes (27): aprobar_cotizacion(), asignar_ajustador(), autorizar_entrega(), editar_siniestro(), enviar_taller(), Request, rechazar_cotizacion(), aplicar_bloqueo_arco() (+19 more)

### Community 20 - "Community 20"
Cohesion: 0.11
Nodes (29): actualizar_consentimientos(), actualizar_perfil(), confirmar_datos(), detalle_siniestro(), get_perfil(), ocr_extraction(), _perfil_completo(), Request (+21 more)

### Community 21 - "Community 21"
Cohesion: 0.09
Nodes (15): Logger, get_logger(), Cada módulo llama esto para obtener su logger con nombre jerárquico.     Ejemplo, Configura el sistema de logging de toda la app., setup_logging(), FastAPI, register_middlewares(), ActualizarPerfilTaller (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (27): listar_aseguradoras(), listar_aseguradoras_desincorporadas(), listar_usuarios(), §5 · Listar aseguradoras registradas (paginado, con filtro de baja)., §5 · Listar únicamente aseguradoras desincorporadas (baja lógica)., Listar usuarios con paginación y filtros., listar_asignaciones(), §5 · Siniestros asignados a mí (paginado). (+19 more)

### Community 23 - "Community 23"
Cohesion: 0.14
Nodes (9): ClienteModel, ClienteRepositoryPort, Protocol, ClienteAdapter, _adapter(), create_cliente_service(), get_cliente_service(), list_clientes_service() (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.07
Nodes (16): BadGatewayError, BadRequestError, ConflictError, InternalServerError, MethodNotAllowedError, 400 Bad Request - Datos inválidos: campos faltantes o formato incorrecto., 401 Unauthorized - Token ausente o inválido., 405 Method Not Allowed - Méthodo no permitido en el endpoint. (+8 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (5): ActualizarDisponibilidad, ActualizarGeolocalizacion, AjustadorModel, AjustadorRepositoryPort, Protocol

### Community 26 - "Community 26"
Cohesion: 0.16
Nodes (5): RegisterUser, TokenResult, User, AuthPort, PasswordPort

### Community 27 - "Community 27"
Cohesion: 0.11
Nodes (8): DeleteUsuario, Session, GetUsuario, ListUsuarios, AdminUserRepositoryPort, Any, get_usuario_service(), list_usuarios_service()

### Community 28 - "Community 28"
Cohesion: 0.11
Nodes (8): ActualizarPerfilAjustador, GetPerfilAjustador, Pruebas de perfil del ajustador (GET + PUT /api/v1/ajustador/perfil)., test_perfil_rol_no_ajustador_rechazado(), wired(), default_ajustador(), FakeAjustadorRepo, Fakes del módulo Ajustador.

### Community 29 - "Community 29"
Cohesion: 0.11
Nodes (8): FakeAjustadorAdapter, test_login_cuenta_arco_bloqueada(), test_recovery_request(), test_recovery_reset_password(), FakeAuthRepo, FakeUser, Fakes del módulo Auth., Minimal User domain model para pruebas.

### Community 30 - "Community 30"
Cohesion: 0.11
Nodes (22): Async/Await Pattern, Clean Architecture, Data Mapper Pattern, Dependency Inversion Pattern, Hexagonal Module Structure, Multi-Tenancy Pattern, ajustadores Table, aseguradoras Table (+14 more)

### Community 31 - "Community 31"
Cohesion: 0.14
Nodes (12): ClienteRepositoryPort, LoginUser, AuthRepository, Session, _to_domain(), PasswordService, confirm_consent_service(), generate_recovery_code_service() (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.19
Nodes (9): ListSiniestrosAsignados, Session, SiniestroRepository, _to_domain(), Base, SiniestroTable, confirmar_peritaje_service(), guardar_peritaje_service() (+1 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (14): ConfirmConsent, ClienteRepositoryPort, ResetPassword, login(), me(), register(), reset_password(), submit_consentimiento() (+6 more)

### Community 34 - "Community 34"
Cohesion: 0.10
Nodes (4): FakeClienteAseguradoraRepo, FakeTallerCrudRepo, FakeUsuarioRepo, Fakes del módulo Aseguradora (CRUD: ajustadores, clientes, talleres, usuarios).

### Community 35 - "Community 35"
Cohesion: 0.16
Nodes (10): 502 Bad Gateway - Error en un servicio de terceros., ThirdPartyServiceError, ProcessOcr, Any, Orquesta la llamada al microservicio externo de OCR.         Retorna los datos e, OcrPort, Any, OcrService (+2 more)

### Community 36 - "Community 36"
Cohesion: 0.23
Nodes (7): Session, TallerRepository, _to_domain(), ConvenioAseguradoraTallerTable, Base, Base, TallerTable

### Community 37 - "Community 37"
Cohesion: 0.15
Nodes (14): GuardarPresupuestoUseCase, PdfGeneratorPort, Any, Protocol, Any, ReportLabPdfGenerator, get_cotizacion_repo(), get_expediente_taller_service() (+6 more)

### Community 38 - "Community 38"
Cohesion: 0.23
Nodes (16): AgregarDano, EditarPeritaje, ListMisAsignaciones, actualizar_perfil_ajustador_service(), agregar_dano_service(), disponibilidad_service(), editar_peritaje_service(), geolocalizacion_service() (+8 more)

### Community 39 - "Community 39"
Cohesion: 0.19
Nodes (8): datetime, RecoveryCode, RecoveryCodePort, Session, RecoveryCodeService, _to_domain(), Base, RecoveryCodeTable

### Community 40 - "Community 40"
Cohesion: 0.21
Nodes (14): ActualizarPerfilCliente, ClienteRepository, ClienteRepositoryPort, Session, actualizar_perfil_cliente_service(), _cliente_checker(), confirm_consent_service(), get_auth_repo_for_enrichment() (+6 more)

### Community 41 - "Community 41"
Cohesion: 0.22
Nodes (13): PerfilTallerRepository, Session, PerfilTallerUsuariosTable, Base, actualizar_perfil_taller_service(), concluir_trabajo_service(), crear_cotizacion_service(), editar_cotizacion_service() (+5 more)

### Community 43 - "Community 43"
Cohesion: 0.14
Nodes (8): BaseSettings, Config, Settings, SendRecoveryCode, EmailPort, Protocol, EmailService, send_recovery_code_service()

### Community 44 - "Community 44"
Cohesion: 0.14
Nodes (10): Tester_Global accede a todos los endpoints de cliente., test_detalle_de_otro_cliente_prohibido(), test_reportar_sin_onboarding_falla(), test_tester_global_bypass_cliente(), wired(), default_cliente_profile(), FakeClienteChecker, FakeClienteRepo (+2 more)

### Community 45 - "Community 45"
Cohesion: 0.15
Nodes (11): AsyncClient, get_supabase_async_client(), get_supabase_client(), Client, Obtiene o crea la instancia global del cliente Supabase asíncrono., Obtiene o crea la instancia global del cliente Supabase., PdfStoragePort, Protocol (+3 more)

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (8): HTTPAuthorizationCredentials, get_current_user(), Dependencia para obtener el usuario autenticado.     Lanza UnauthorizedError si, VerifyToken, TokenPayload, TokenPort, JwtTokenService, verify_token_service()

### Community 47 - "Community 47"
Cohesion: 0.24
Nodes (9): AdminPurgeRepository, Session, _dano_to_domain(), _peritaje_to_domain(), PeritajeAjustadorRepository, Session, DanosAjustadosManualTable, PeritajeAjustadorTable (+1 more)

### Community 48 - "Community 48"
Cohesion: 0.30
Nodes (7): Enum, EstadoUsuario, EstatusComercialAseguradora, PlanSuscripcion, Rol, SeveridadDano, TipoDano

### Community 49 - "Community 49"
Cohesion: 0.24
Nodes (10): Router canónico `/api/v1` con prefijos por rol., AjustadorCreateDTO, AjustadorResponseDTO, AjustadorUpdateDTO, BaseModel, actualizar_ajustador(), crear_ajustador(), eliminar_ajustador() (+2 more)

### Community 50 - "Community 50"
Cohesion: 0.21
Nodes (5): AdminUserRepository, Session, _user_to_dict(), Base, UserTable

### Community 51 - "Community 51"
Cohesion: 0.28
Nodes (11): OperadorTallerRequestDTO, BaseModel, TallerCreateDTO, TallerResponseDTO, TallerUpdateDTO, actualizar_taller(), crear_operador_taller(), crear_taller() (+3 more)

### Community 52 - "Community 52"
Cohesion: 0.28
Nodes (6): ClienteRepository, ClienteRepositoryPort, Session, _to_domain(), PerfilClienteTable, Base

### Community 53 - "Community 53"
Cohesion: 0.25
Nodes (6): ClienteProfile, ClienteRepositoryPort, Protocol, _to_domain(), ClienteProfileTable, Base

### Community 54 - "Community 54"
Cohesion: 0.24
Nodes (10): AESGCM, decrypt_aes256(), encrypt_aes256(), _get_aesgcm(), Cifra un texto utilizando AES-256-GCM. Retorna string base64., Descifra un texto cifrado con AES-256-GCM desde string base64., decrypt_fields(), encrypt_fields() (+2 more)

### Community 55 - "Community 55"
Cohesion: 0.23
Nodes (8): AjustadorAdapter, _adapter(), create_ajustador_service(), delete_ajustador_service(), get_ajustador_service(), list_ajustadores_service(), Session, update_ajustador_service()

### Community 56 - "Community 56"
Cohesion: 0.29
Nodes (5): _format_wkt(), _parse_wkt(), _to_domain(), AjustadorTable, Base

### Community 57 - "Community 57"
Cohesion: 0.20
Nodes (5): BloqueoArcoAseguradora, DesbloqueoArcoAseguradora, Any, Protocol, UsuarioRepositoryPort

### Community 58 - "Community 58"
Cohesion: 0.18
Nodes (3): CreateOperadorTallerUseCase, crear_operador_taller_service(), FakeTallerModuleAdapter

### Community 59 - "Community 59"
Cohesion: 0.29
Nodes (5): Session, UsuarioRepository, bloqueo_arco_service(), desbloqueo_arco_service(), usuario_repo()

### Community 61 - "Community 61"
Cohesion: 0.28
Nodes (6): Factory de dependencia para RBAC. Devuelve una dependencia que valida que el, require_roles(), client(), make_user(), NoopAudit, Bootstrap de pruebas. No requiere base de datos ni servicios externos: se inyect

### Community 62 - "Community 62"
Cohesion: 0.28
Nodes (5): ConfirmData, ClienteRepositoryPort, confirm_data_service(), ConfirmDataRequestDTO, BaseModel

### Community 63 - "Community 63"
Cohesion: 0.39
Nodes (8): CotizacionTallerDTO, DanoAjustadoDTO, ExpedienteTecnicoResponseDTO, GuardarPresupuestoRequestDTO, MessageResponseDTO, PeritajeAjustadorTecnicoDTO, BaseModel, SiniestroTecnicoDTO

### Community 64 - "Community 64"
Cohesion: 0.29
Nodes (8): JSONResponse, accepted_response(), created_response(), Any, 201 Created - Respuesta al crear un recurso. Se puede incluir Location., 202 Accepted - El trabajo fue aceptado para procesamiento asíncrono., 200 OK - Respuesta genérica con payload JSON., success_response()

### Community 66 - "Community 66"
Cohesion: 0.33
Nodes (4): EmailStr, GenerateRecoveryCode, datetime, request_recovery()

### Community 67 - "Community 67"
Cohesion: 0.47
Nodes (4): CrearOperadorAseguradoraUseCase, crear_operador_aseguradora(), §5 · Crear un operador para una aseguradora específica., OperadorAseguradoraRequestDTO

### Community 68 - "Community 68"
Cohesion: 0.47
Nodes (3): ClienteCreateDTO, ClienteResponseDTO, BaseModel

### Community 69 - "Community 69"
Cohesion: 0.33
Nodes (3): GetPerfilCliente, ClienteRepositoryPort, Devuelve el perfil de cliente (`perfiles_clientes`) del usuario autenticado.

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (4): Admin API Module, Auth API Module, Cliente API Module, Account Deletion Plan

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (3): Ajustador API Module, Aseguradora Siniestros API, Taller API Module

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (3): POST /auth/eliminacion-cuenta/confirmar, GenerateRecoveryCode Reuse, POST /auth/eliminacion-cuenta/solicitar

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (3): Response, no_content_response(), 204 No Content - Respuesta sin cuerpo (p. ej. DELETE exitoso).

## Knowledge Gaps
- **18 isolated node(s):** `Config`, `TokenResult`, `Admin API Module`, `Ajustador API Module`, `Taller API Module` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `NotFoundError` connect `Exception Handling Layer` to `Siniestro Assignment & Delivery`, `Quote Approval Workflow`, `Siniestro Lifecycle Core`, `Workshop Quote Management`, `Workshop Administration`, `Admin CRUD Operations`, `Insurer Profile Management`, `Adjuster Field Operations`, `Admin Use Cases`, `Admin Dashboard & Repos`, `Community 15`, `Community 16`, `Community 17`, `Community 18`, `Community 21`, `Community 23`, `Community 24`, `Community 26`, `Community 27`, `Community 28`, `Community 31`, `Community 33`, `Community 40`, `Community 50`, `Community 53`, `Community 54`, `Community 55`, `Community 57`, `Community 62`, `Community 67`, `Community 69`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `AuthenticatedUser` connect `Community 22` to `Quote Approval Workflow`, `Workshop Quote Management`, `Admin CRUD Operations`, `Insurer Profile Management`, `Adjuster Test Suite`, `Adjuster Domain Ports`, `Client Test Suite`, `Admin Use Cases`, `Auth Verification Flow`, `Community 16`, `Community 18`, `Community 19`, `Community 20`, `Community 21`, `Community 26`, `Community 28`, `Community 33`, `Community 38`, `Community 42`, `Community 44`, `Community 46`, `Community 49`, `Community 51`, `Community 61`, `Community 67`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `BusinessRuleError` connect `Siniestro Lifecycle Core` to `Siniestro Assignment & Delivery`, `Quote Approval Workflow`, `Workshop Quote Management`, `Workshop Administration`, `Admin CRUD Operations`, `Exception Handling Layer`, `Adjuster Field Operations`, `Admin Use Cases`, `Community 15`, `Community 23`, `Community 24`, `Community 25`, `Community 26`, `Community 27`, `Community 33`, `Community 55`, `Community 57`, `Community 62`, `Community 67`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 45 inferred relationships involving `NotFoundError` (e.g. with `ActualizarAseguradoraUseCase` and `ActualizarSuscripcionUseCase`) actually correct?**
  _`NotFoundError` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 36 inferred relationships involving `BusinessRuleError` (e.g. with `ActualizarAseguradoraUseCase` and `AplicarBloqueoArcoUseCase`) actually correct?**
  _`BusinessRuleError` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `SiniestroRepositoryPort` (e.g. with `GetMiSiniestro` and `ListMisAsignaciones`) actually correct?**
  _`SiniestroRepositoryPort` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `SiniestroModel` (e.g. with `GetMiSiniestro` and `ListMisAsignaciones`) actually correct?**
  _`SiniestroModel` has 26 INFERRED edges - model-reasoned connections that need verification._