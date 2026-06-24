from fastapi import Depends
from src.core.database import get_session
from src.modules.admin.infra.db.repositories.aseguradora_repository import AseguradoraRepository
from src.modules.admin.infra.db.repositories.audit_log_repository import AuditLogRepository
from src.modules.admin.infra.db.repositories.admin_user_repository import AdminUserRepository
from src.modules.admin.infra.services.desincorporacion_job_service import DesincorporacionJobService

from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.aplicar_bloqueo_arco import AplicarBloqueoArcoUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.consultar_auditoria import ConsultarAuditoriaUseCase

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
