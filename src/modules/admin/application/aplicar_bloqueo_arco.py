import datetime
from uuid import uuid4
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AdminUserRepositoryPort, AuditLogRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError

class AplicarBloqueoArcoUseCase:
    def __init__(self, user_repo: AdminUserRepositoryPort, audit_repo: AuditLogRepositoryPort):
        self.user_repo = user_repo
        self.audit_repo = audit_repo

    def execute(self, admin_id: str, usuario_id: str) -> None:
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado.")

        # Validación de aislamiento multi-tenant (HU-AD-01)
        if not user.get("aseguradora_id"):
            raise BusinessRuleError("El usuario no tiene una aseguradora asociada. No se puede aplicar bloqueo ARCO sin identificador organizacional.")

        # Llama al puerto que ejecutará el aislamiento, revocación de tokens y cifrado AES-256
        self.user_repo.bloquear_por_arco(usuario_id)
        
        self.audit_repo.append(AuditLog(
            id=str(uuid4()),
            usuario_id=admin_id,
            aseguradora_id=user.get("aseguradora_id"),
            accion_realizada="BLOQUEO_ARCO",
            evento_modulo="USUARIOS",
            metadata_context={
                "motivo": "Derechos ARCO",
                "acciones": ["cifrado", "revocacion", "aislamiento"],
                "tenant_id": user.get("aseguradora_id"),
            },
            direccion_ip='[IP_ADDRESS]',
            created_at=datetime.datetime.now(),
            user_agent=admin_id,
        ))