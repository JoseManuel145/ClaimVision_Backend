import uuid
from datetime import datetime
from src.modules.admin.presentation.schemas import UpdateSuscripcionDTO
from src.modules.admin.domain.models import AseguradoraTenant, AuditLog
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import NotFoundError

class ActualizarSuscripcionUseCase:
    def __init__(self, repo: AseguradoraRepositoryPort, audit_repo: AuditLogRepositoryPort):
        self.repo = repo
        self.audit_repo = audit_repo

    def execute(self, admin_id: str, aseguradora_id: str, data: UpdateSuscripcionDTO) -> AseguradoraTenant:
        tenant = self.repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")
        
        old_plan = tenant.plan_suscripcion
        old_limit = tenant.limite_peritajes_mes
        
        tenant.plan_suscripcion = data.nuevo_plan
        tenant.limite_peritajes_mes = data.limite_peritajes_mes
        
        updated = self.repo.update(tenant)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            metadata_context={
                "old_plan": old_plan, 
                "new_plan": data.nuevo_plan,
                "old_limit": old_limit, 
                "new_limit": data.limite_peritajes_mes
            },
            direccion_ip='[IP_ADDRESS]', #como consigo la ip? 
            user_agent=admin_id,
            evento_modulo="ASEGURADORAS",
            accion_realizada="ACTUALIZAR_SUSCRIPCION",
            created_at=datetime.now(),
        ))

        return updated

