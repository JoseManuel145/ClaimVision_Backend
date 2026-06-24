from datetime import datetime
import uuid
from typing import Optional
from src.modules.admin.presentation.schemas import AseguradoraRequestDTO
from src.modules.admin.domain.models import AseguradoraTenant, AuditLog
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import BusinessRuleError

class RegistrarAseguradoraUseCase:
    def __init__(self, repo: AseguradoraRepositoryPort, audit_repo: AuditLogRepositoryPort):
        self.repo = repo
        self.audit_repo = audit_repo

    def execute(self, admin_id: str, data: AseguradoraRequestDTO) -> AseguradoraTenant:
        if not data.nombre or not data.rfc:
            raise BusinessRuleError("Nombre y RFC son obligatorios para crear una aseguradora.")
        
        tenant = AseguradoraTenant(
            id=str(uuid.uuid4()),
            nombre=data.nombre,
            rfc=data.rfc,
            dominio_correo=data.dominio_correo,
            plan_suscripcion=data.plan_suscripcion,
            limite_peritajes_mes=0,
            peritajes_consumidos_mes=0,
            estatus_comercial='Suspendido',
            contacto_legal_email=data.contacto_legal_email,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        saved = self.repo.save(tenant)

        # Registrar en Auditoría
        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=saved.id,
            accion_realizada="REGISTRO_ASEGURADORA",
            evento_modulo="ASEGURADORAS",
            metadata_context={"rfc": saved.rfc, "nombre": saved.nombre},
            direccion_ip='[IP_ADDRESS]',
            created_at=datetime.now(),
            user_agent=admin_id,
        ))
        return saved
