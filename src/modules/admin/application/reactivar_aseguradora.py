import uuid
from datetime import datetime, timezone
from src.modules.admin.domain.models import AseguradoraTenant, AuditLog
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError


class ReactivarAseguradoraUseCase:
    def __init__(self, repo: AseguradoraRepositoryPort, audit_repo: AuditLogRepositoryPort):
        self.repo = repo
        self.audit_repo = audit_repo

    def execute(self, admin_id: str, aseguradora_id: str) -> AseguradoraTenant:
        tenant = self.repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")

        if tenant.estatus_comercial != "Cancelado":
            raise BusinessRuleError("Solo se pueden reactivar aseguradoras con estatus Cancelado.")

        old_estatus = tenant.estatus_comercial
        tenant.estatus_comercial = "Suspendido"
        tenant.deleted_at = None
        tenant.updated_at = datetime.now(timezone.utc)

        updated = self.repo.update(tenant)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            accion_realizada="REACTIVAR_ASEGURADORA",
            evento_modulo="ASEGURADORAS",
            metadata_context={"old_estatus": old_estatus, "new_estatus": "Suspendido"},
            direccion_ip='[IP_ADDRESS]',
            created_at=datetime.now(),
            user_agent=admin_id,
        ))
        return updated
