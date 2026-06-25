import uuid
from datetime import datetime, timezone
from src.modules.admin.presentation.schemas import OperadorAseguradoraRequestDTO
from src.modules.admin.domain.ports import AseguradoraRepositoryPort, AuditLogRepositoryPort
from src.modules.auth.domain.ports import AuthPort, PasswordPort
from src.modules.auth.domain.models import User
from src.modules.admin.domain.models import AuditLog
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.shared.domain.models import Rol, EstadoUsuario

class CrearOperadorAseguradoraUseCase:
    def __init__(
        self, 
        aseguradora_repo: AseguradoraRepositoryPort, 
        audit_repo: AuditLogRepositoryPort,
        auth_repo: AuthPort,
        password_port: PasswordPort
    ):
        self.aseguradora_repo = aseguradora_repo
        self.audit_repo = audit_repo
        self.auth_repo = auth_repo
        self.password_port = password_port

    def execute(self, admin_id: str, aseguradora_id: str, data: OperadorAseguradoraRequestDTO):
        # 1. Verificar que la aseguradora exista
        tenant = self.aseguradora_repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")
            
        # 2. Verificar que el correo no esté en uso en Auth
        existing_user = self.auth_repo.get_by_email(data.email)
        if existing_user:
            raise BusinessRuleError("El correo electrónico ya está registrado.")
            
        # 3. Hashear contraseña
        hashed_pwd = self.password_port.hash(data.password)
        
        # 4. Crear el usuario en el módulo de Auth vinculado a la aseguradora
        new_user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=data.nombre,
            email=data.email,
            password=hashed_pwd,
            telefono="",
            rol=Rol.ASEGURADORA.value,
            estado=EstadoUsuario.ACTIVO.value,
            aseguradora_id=aseguradora_id,
            fecha_creacion=datetime.now(timezone.utc),
            is_authenticated=False,
            fecha_eliminacion=None
        )
        
        user_created = self.auth_repo.create(new_user)
        
        # 5. Registrar en auditoría
        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            accion_realizada="CREAR_OPERADOR",
            evento_modulo="ASEGURADORAS",
            metadata_context={"operador_email": data.email, "operador_id": user_created.usuario_id},
            direccion_ip='[IP_ADDRESS]',
            user_agent=admin_id,
            created_at=datetime.now(),
        ))
        
        return {
            "usuario_id": user_created.usuario_id,
            "email": user_created.email,
            "rol": user_created.rol,
            "aseguradora_id": user_created.aseguradora_id
        }
