Con el contexto del backend (FastAPI, arquitectura hexagonal por módulos, y el sistema ARCO que ya existe para bloqueo de
  cuentas), aquí está el plan de los endpoints/URL necesarios — sin implementación.

  Endpoints nuevos

  Mismo patrón que recovery/* (código enviado por email), bajo el módulo auth ya existente:

  ┌────────┬───────────────────────────────────────────┬─────────────────────┬────────────────────────────────────────────────┐
  │ Método │                 Endpoint                  │        Auth         │                  Descripción                   │
  ├────────┼───────────────────────────────────────────┼─────────────────────┼────────────────────────────────────────────────┤
  │        │                                           │ JWT                 │ El usuario logueado pide la baja. Genera un    │
  │ POST   │ /api/auth/eliminacion-cuenta/solicitar    │ (get_current_user)  │ código/token de confirmación y dispara el      │
  │        │                                           │                     │ correo.                                        │
  ├────────┼───────────────────────────────────────────┼─────────────────────┼────────────────────────────────────────────────┤
  │ POST   │ /api/auth/eliminacion-cuenta/confirmar    │ Público (token en   │ El usuario confirma con el código recibido por │
  │        │                                           │ body)               │  correo. Aquí se ejecuta la baja real.         │
  ├────────┼───────────────────────────────────────────┼─────────────────────┼────────────────────────────────────────────────┤
  │        │ /api/auth/eliminacion-cuenta/cancelar     │                     │ Permite abortar la solicitud dentro de un      │
  │ POST   │ (opcional)                                │ JWT                 │ plazo de gracia, antes de que se ejecute el    │
  │        │                                           │                     │ borrado definitivo.                            │
  └────────┴───────────────────────────────────────────┴─────────────────────┴────────────────────────────────────────────────┘

  El "enlace"

  - En la app: botón "Eliminar mi cuenta" en la pantalla de perfil/ajustes → llama a solicitar.
  - En el correo de confirmación: un link tipo https://<frontend>/cuenta/eliminar/confirmar?uid={usuario_id}&code={code}, que la
  SPA renderiza y desde ahí hace el POST /confirmar.

  Flujo

  1. Usuario autenticado llama a solicitar → se genera un código igual que en recovery/request (reutilizando el mecanismo de
  GenerateRecoveryCode, pero con un purpose/tipo distinto para que el código no sirva para recuperar contraseña).
  2. EmailService manda un correo nuevo (hoy solo tiene send_code() para recovery; se necesitaría una plantilla nueva) con el link
  de confirmación.
  3. Usuario confirma → confirmar valida el código y ejecuta la baja:
    - deleted_at = ahora, estatus_arco = INACTIVO (mismo criterio que ya dejaste anotado en MODIFICACIONES_BACKEND_NECESARIAS.md
  para el DELETE admin).
    - Revocación de tokens activos (como ya hace bloqueo_arco).
    - Registro en AuditLogRepository (accion="ELIMINACION_CUENTA_SOLICITADA_POR_USUARIO"), igual patrón que
  AplicarBloqueoArcoUseCase.

  Piezas existentes que se reutilizan

  - GenerateRecoveryCode / EmailService (src/modules/auth/infra/messaging/email_service.py) → base para generar y enviar el código.
  - AuditLogger / AuditLogRepository → trazabilidad.
  - EstadoUsuario enum y campos deleted_at/estatus_arco en UserTable → ya soportan el soft-delete, no requieren migración nueva.
  - Patrón de bloqueo_arco como referencia de "cancelación ARCO" ya aceptado en el proyecto.

  Puntos a decidir antes de implementar

  - Retención de datos de siniestros: ¿el borrado de cuenta anonimiza solo credenciales/PII del usuario, o también afecta los
  siniestros asociados? (normalmente esos deben conservarse por obligación regulatoria del seguro, aunque la cuenta se dé de baja).
  - Plazo de gracia: ¿confirmación inmediata o ventana de N días para cancelar antes del borrado definitivo?
  - Requisito de enlace público sin login: algunas políticas (Play Store, LFPDPPP) exigen que el proceso de solicitud de borrado
  esté descrito/accesible sin necesidad de iniciar sesión — si aplica, habría que agregar una página pública informativa además del
  flujo autenticado.
