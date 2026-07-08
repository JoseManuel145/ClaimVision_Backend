import uuid
from datetime import datetime, timezone
from src.modules.admin.presentation.schemas import CreateUsuarioRequestDTO
from src.modules.admin.domain.ports import AdminUserRepositoryPort, AuditLogRepositoryPort
from src.modules.auth.domain.ports import AuthPort, PasswordPort
from src.modules.auth.domain.models import User
from src.modules.admin.domain.models import AuditLog
from src.core.exceptions import BusinessRuleError
from src.shared.domain.models import EstadoUsuario

class CreateUsuario:
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

    def execute(self, admin_id: str, data: CreateUsuarioRequestDTO) -> dict:
        existing = self.auth_repo.get_by_email(data.email)
        if existing:
            raise BusinessRuleError("El correo electrónico ya está registrado.")

        hashed_pwd = self.password_port.hash(data.password)

        new_user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=data.nombre,
            email=data.email,
            password=hashed_pwd,
            telefono=data.telefono or "",
            rol=data.rol,
            estado=EstadoUsuario.ACTIVO.value,
            aseguradora_id=data.aseguradora_id,
            fecha_creacion=datetime.now(timezone.utc),
            is_authenticated=False,
            fecha_eliminacion=None,
        )
        created = self.auth_repo.create(new_user)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=data.aseguradora_id,
            accion_realizada="CREAR_USUARIO",
            evento_modulo="USUARIOS",
            metadata_context={"usuario_id": created.usuario_id, "email": created.email, "rol": created.rol},
            direccion_ip="[IP_ADDRESS]",
            user_agent=admin_id,
            created_at=datetime.now(),
        ))

        return self.user_repo.get_by_id(created.usuario_id)
