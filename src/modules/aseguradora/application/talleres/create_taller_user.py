import uuid
from datetime import datetime, timezone
from src.modules.aseguradora.presentation.talleres.taller_dto import OperadorTallerRequestDTO
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.modules.admin.domain.ports import AuditLogRepositoryPort
from src.modules.auth.domain.ports import AuthPort, PasswordPort
from src.modules.auth.domain.models import User
from src.modules.admin.domain.models import AuditLog
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.shared.domain.models import Rol, EstadoUsuario

class CreateOperadorTallerUseCase:
    def __init__(
        self,
        taller_repo: TallerRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort,
        audit_repo: AuditLogRepositoryPort,
        auth_repo: AuthPort,
        password_port: PasswordPort
    ):
        self.taller_repo = taller_repo
        self.perfil_taller_repo = perfil_taller_repo
        self.audit_repo = audit_repo
        self.auth_repo = auth_repo
        self.password_port = password_port

    def execute(self, aseguradora_id: str, admin_id: str, taller_id: str, data: OperadorTallerRequestDTO):
        # 1. Verificar que el taller exista
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado.")
            
        # 2. Verificar que el correo no esté en uso
        existing_user = self.auth_repo.get_by_email(data.email)
        if existing_user:
            raise BusinessRuleError("El correo electrónico ya está registrado.")
            
        # 3. Hashear contraseña
        hashed_pwd = self.password_port.hash(data.password)
        
        # 4. Crear el usuario en el módulo de Auth (aseguradora_id es None ya que es un usuario de Taller)
        # Nota: El usuario pertenece a un Taller que puede trabajar para N Aseguradoras.
        new_user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=data.nombre,
            email=data.email,
            password=hashed_pwd,
            telefono="",
            rol=Rol.TALLER.value,
            estado=EstadoUsuario.ACTIVO.value,
            aseguradora_id=None,
            fecha_creacion=datetime.now(timezone.utc),
            is_authenticated=False,
            fecha_eliminacion=None
        )
        
        user_created = self.auth_repo.create(new_user)
        
        # 5. Crear el perfil del taller
        self.perfil_taller_repo.add_usuario_a_taller(user_created.usuario_id, taller_id, data.puesto)
        
        # 6. Registrar en auditoría
        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=aseguradora_id,
            accion_realizada="CREAR_OPERADOR_TALLER",
            evento_modulo="TALLERES",
            metadata_context={"operador_email": data.email, "operador_id": user_created.usuario_id, "taller_id": taller_id},
            direccion_ip='[IP_ADDRESS]',
            user_agent=admin_id,
            created_at=datetime.now(),
        ))
        
        return {
            "usuario_id": user_created.usuario_id,
            "email": user_created.email,
            "rol": user_created.rol,
            "taller_id": taller_id,
            "puesto": data.puesto
        }
