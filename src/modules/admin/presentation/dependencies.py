from fastapi import Depends
from src.core.database import get_session
from src.modules.admin.infra.db.repositories.aseguradora_repository import AseguradoraRepository
from src.modules.admin.infra.db.repositories.audit_log_repository import AuditLogRepository
from src.modules.admin.infra.db.repositories.admin_user_repository import AdminUserRepository
from src.modules.admin.infra.services.desincorporacion_job_service import DesincorporacionJobService

from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.actualizar_aseguradora import ActualizarAseguradoraUseCase
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.crear_operador_aseguradora import CrearOperadorAseguradoraUseCase

from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.aplicar_bloqueo_arco import AplicarBloqueoArcoUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.consultar_auditoria import ConsultarAuditoriaUseCase

# ── Nuevos use cases ──────────────────────────────────────────────────
from src.modules.admin.application.list_usuarios import ListUsuarios
from src.modules.admin.application.get_usuario import GetUsuario
from src.modules.admin.application.create_usuario import CreateUsuario
from src.modules.admin.application.update_usuario import UpdateUsuario
from src.modules.admin.application.delete_usuario import DeleteUsuario
from src.modules.admin.application.list_talleres_admin import ListTalleresAdmin
from src.modules.admin.application.get_taller_admin import GetTallerAdmin
from src.modules.admin.application.get_dashboard_resumen import GetDashboardResumen
# taller repo (reused from aseguradora module)
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository


def registrar_aseguradora_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    audit_repo = AuditLogRepository(session)
    return RegistrarAseguradoraUseCase(repo, audit_repo)

def list_aseguradoras_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    return ListAseguradoras(repo)

def actualizar_suscripcion_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    audit_repo = AuditLogRepository(session)
    return ActualizarSuscripcionUseCase(repo, audit_repo)

def actualizar_aseguradora_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    audit_repo = AuditLogRepository(session)
    return ActualizarAseguradoraUseCase(repo, audit_repo)

def get_aseguradora_by_id_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    return GetAseguradoraById(repo)

def desincorporar_aseguradora_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    audit_repo = AuditLogRepository(session)
    job_port = DesincorporacionJobService()
    user_repo = AdminUserRepository(session)
    return DesincorporarAseguradoraUseCase(repo, audit_repo, job_port, user_repo)

def aplicar_bloqueo_arco_service(session=Depends(get_session)):
    user_repo = AdminUserRepository(session)
    audit_repo = AuditLogRepository(session)
    return AplicarBloqueoArcoUseCase(user_repo, audit_repo)

def verificar_aseguradora_service(session=Depends(get_session)):
    repo = AseguradoraRepository(session)
    audit_repo = AuditLogRepository(session)
    return VerificarAseguradoraUseCase(repo, audit_repo)

def consultar_auditoria_service(session=Depends(get_session)):
    audit_repo = AuditLogRepository(session)
    return ConsultarAuditoriaUseCase(audit_repo)

def crear_operador_aseguradora_service(session=Depends(get_session)):
    aseguradora_repo = AseguradoraRepository(session)
    audit_repo = AuditLogRepository(session)
    auth_repo = AuthRepository(session)
    password_port = PasswordService()
    return CrearOperadorAseguradoraUseCase(aseguradora_repo, audit_repo, auth_repo, password_port)

# ── Nuevos servicios ──────────────────────────────────────────────────

def list_usuarios_service(session=Depends(get_session)):
    return ListUsuarios(AdminUserRepository(session))

def get_usuario_service(session=Depends(get_session)):
    return GetUsuario(AdminUserRepository(session))

def create_usuario_service(session=Depends(get_session)):
    return CreateUsuario(
        AdminUserRepository(session),
        AuditLogRepository(session),
        AuthRepository(session),
        PasswordService(),
    )

def update_usuario_service(session=Depends(get_session)):
    return UpdateUsuario(
        AdminUserRepository(session),
        AuditLogRepository(session),
        AuthRepository(session),
        PasswordService(),
    )

def delete_usuario_service(session=Depends(get_session)):
    return DeleteUsuario(
        AdminUserRepository(session),
        AuditLogRepository(session),
        session,
    )

def list_talleres_admin_service(session=Depends(get_session)):
    return ListTalleresAdmin(TallerRepository(session))

def get_taller_admin_service(session=Depends(get_session)):
    return GetTallerAdmin(TallerRepository(session))

def get_dashboard_resumen_service(session=Depends(get_session)):
    return GetDashboardResumen(session)

