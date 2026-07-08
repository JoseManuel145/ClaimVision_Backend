from datetime import datetime, timezone
from src.modules.admin.presentation.schemas import UpdateUsuarioRequestDTO
from src.modules.admin.domain.ports import AdminUserRepositoryPort, AuditLogRepositoryPort
from src.modules.auth.domain.ports import AuthPort, PasswordPort
from src.modules.admin.domain.models import AuditLog
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.modules.auth.infra.db.tables.user_table import UserTable

FIELD_MAP = {
    "nombre": "nombre_completo_cifrado",
    "telefono": "telefono_cifrado",
    "rol": "rol",
    "aseguradora_id": "aseguradora_id",
    "email": "email",
}

class UpdateUsuario:
    def __init__(
        self,
        user_repo: AdminUserRepositoryPort,
        audit_repo: AuditLogRepositoryPort,
        auth_repo: AuthPort,
        password_port: PasswordPort,
    ):
        self.user_repo = user_repo
        self.audit_repo = audit_repo
        self.auth_repo = auth_repo
        self.password_port = password_port

    def execute(self, admin_id: str, usuario_id: str, data: UpdateUsuarioRequestDTO) -> dict:
        existing = self.user_repo.get_by_id(usuario_id)
        if not existing:
            raise NotFoundError("Usuario no encontrado.")

        update_data = {}
        if data.nombre is not None:
            update_data["nombre_completo_cifrado"] = data.nombre
        if data.telefono is not None:
            update_data["telefono_cifrado"] = data.telefono
        if data.rol is not None:
            update_data["rol"] = data.rol
        if data.aseguradora_id is not None:
            update_data["aseguradora_id"] = data.aseguradora_id
        if data.email is not None:
            existing_email = self.auth_repo.get_by_email(data.email)
            if existing_email and existing_email.usuario_id != usuario_id:
                raise BusinessRuleError("El correo electrónico ya está en uso por otro usuario.")
            update_data["email"] = data.email
        if data.password is not None:
            update_data["password_hash"] = self.password_port.hash(data.password)

        if not update_data:
            return self.user_repo.get_by_id(usuario_id)

        updated = self.user_repo.update_user(usuario_id, update_data)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=existing.get("aseguradora_id"),
            accion_realizada="ACTUALIZAR_USUARIO",
            evento_modulo="USUARIOS",
            metadata_context={"usuario_id": usuario_id, "campos": list(update_data.keys())},
            direccion_ip="[IP_ADDRESS]",
            user_agent=admin_id,
            created_at=datetime.now(),
        ))

        return updated
