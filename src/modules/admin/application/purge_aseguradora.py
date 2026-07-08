import uuid
from datetime import datetime, timezone
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import NotFoundError


class PurgeAseguradoraUseCase:
    def __init__(
        self,
        aseguradora_repo: AseguradoraRepositoryPort,
        audit_repo: AuditLogRepositoryPort,
        purge_repo,
    ):
        self.aseguradora_repo = aseguradora_repo
        self.audit_repo = audit_repo
        self.purge_repo = purge_repo

    def execute(self, admin_id: str, aseguradora_id: str) -> dict:
        tenant = self.aseguradora_repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")
        if tenant.deleted_at is not None:
            raise NotFoundError("La aseguradora ya está desincorporada.")

        deleted = self.purge_repo.purge_aseguradora(aseguradora_id)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            evento_modulo="ASEGURADORAS",
            accion_realizada="PURGA_TOTAL_ASEGURADORA",
            direccion_ip="[SYSTEM]",
            user_agent="[PURGE]",
            metadata_context={
                "aseguradora_id": aseguradora_id,
                "aseguradora_nombre": tenant.nombre,
                "deleted": deleted,
            },
            created_at=datetime.now(timezone.utc),
        ))

        return {
            "purged": True,
            "aseguradora_id": aseguradora_id,
            "aseguradora_nombre": tenant.nombre,
            "deleted": deleted,
        }
