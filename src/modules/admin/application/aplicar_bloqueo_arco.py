import datetime
from uuid import uuid4
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AdminUserRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import NotFoundError

class AplicarBloqueoArcoUseCase:
    def __init__(self, user_repo: AdminUserRepositoryPort, audit_repo: AuditLogRepositoryPort):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def execute(self, admin_id: str, usuario_id: str) -> None:
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado.")

        # Llama al puerto que ejecutará el aislamiento, revocación de tokens y cifrado AES-256
        self.user_repo.bloquear_por_arco(usuario_id)
        
        self.audit_repo.append(AuditLog(
            id=str(uuid4()),
            usuario_id=admin_id,
            aseguradora_id=user.aseguradora_id,
            accion_realizada="BLOQUEO_ARCO",
            evento_modulo="usuarios",
            metadata_context={"motivo": "Derechos ARCO", "acciones": ["cifrado", "revocacion", "aislamiento"]},
            direccion_ip='[IP_ADDRESS]', #como consigo la ip? 
            created_at=datetime.now(),
            user_agent=admin_id,
        ))