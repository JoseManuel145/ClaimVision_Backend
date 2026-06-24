import uuid
from datetime import datetime
from src.modules.admin.presentation.schemas import UpdateAseguradoraDTO
from src.modules.admin.domain.models import AseguradoraTenant, AuditLog
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError


class ActualizarAseguradoraUseCase:
    def __init__(self, repo: AseguradoraRepositoryPort, audit_repo: AuditLogRepositoryPort):
        self.repo = repo
        self.audit_repo = audit_repo

    def execute(self, admin_id: str, aseguradora_id: str, data: UpdateAseguradoraDTO) -> AseguradoraTenant:
        tenant = self.repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")

        if tenant.estatus_comercial == "Cancelado":
            raise BusinessRuleError("No se pueden modificar los datos de una aseguradora desincorporada.")

        changes: dict = {}

        if data.nombre is not None:
            changes["nombre"] = {"old": tenant.nombre, "new": data.nombre}
            tenant.nombre = data.nombre
        if data.rfc is not None:
            changes["rfc"] = {"old": tenant.rfc, "new": data.rfc}
            tenant.rfc = data.rfc
        if data.dominio_correo is not None:
            changes["dominio_correo"] = {"old": tenant.dominio_correo, "new": data.dominio_correo}
            tenant.dominio_correo = data.dominio_correo
        if data.contacto_legal_email is not None:
            changes["contacto_legal_email"] = {"old": tenant.contacto_legal_email, "new": data.contacto_legal_email}
            tenant.contacto_legal_email = data.contacto_legal_email

        if not changes:
            raise BusinessRuleError("No se proporcionaron campos para actualizar.")

        tenant.updated_at = datetime.now()
        updated = self.repo.update(tenant)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            accion_realizada="ACTUALIZAR_DATOS_COMERCIALES",
            evento_modulo="ASEGURADORAS",
            metadata_context=changes,
            direccion_ip='[IP_ADDRESS]',
            created_at=datetime.now(),
            user_agent=admin_id,
        ))
        return updated
