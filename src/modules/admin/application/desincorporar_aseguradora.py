import uuid
from datetime import datetime, timezone
from src.modules.admin.domain.models import AseguradoraTenant, AuditLog
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort, DesincorporacionJobPort, AdminUserRepositoryPort
from src.core.exceptions import NotFoundError

class DesincorporarAseguradoraUseCase:
    def __init__(self, repo: AseguradoraRepositoryPort, audit_repo: AuditLogRepositoryPort, job_port: DesincorporacionJobPort, user_repo: AdminUserRepositoryPort):
        self.repo = repo
        self.audit_repo = audit_repo
        self.job_port = job_port
        self.user_repo = user_repo

    def execute(self, admin_id: str, aseguradora_id: str) -> AseguradoraTenant:
        tenant = self.repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")
        
        old_estatus = tenant.estatus_comercial
        tenant.estatus_comercial = "Cancelado"
        tenant.deleted_at = datetime.now(timezone.utc)
        
        updated = self.repo.update(tenant)

        # Bloqueo inmediato de autenticación de todos sus usuarios asociados
        self.user_repo.block_all_users_from_tenant(aseguradora_id)

        # Disparar background job de compresión ZIP + cifrado
        self.job_port.trigger_desincorporacion(aseguradora_id)
        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            metadata_context={
                "old_estatus": old_estatus, 
                "new_estatus": "Cancelado", 
                "job_triggered": True
            },
            direccion_ip='[IP_ADDRESS]', 
            user_agent=admin_id,
            evento_modulo="ASEGURADORAS",
            accion_realizada="DESINCORPORACION_TECNICA",
            created_at=datetime.now(),
        ))
        return updated
