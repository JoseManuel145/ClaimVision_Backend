from datetime import datetime, timezone
import uuid
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.modules.auth.domain.ports import AuthPort
from src.modules.auth.infra.security.password_service import PasswordService
from src.shared.domain.models import Rol, EstadoUsuario
from src.modules.auth.domain.models import User
from src.core.exceptions import BusinessRuleError
from src.modules.aseguradora.presentation.ajustadores.ajustador_dto import AjustadorCreateDTO

class CreateAjustador:
    def __init__(self, auth_repo: AuthPort, repo: AjustadorRepositoryPort, password_service: PasswordService):
        self.auth_repo = auth_repo
        self.repo = repo
        self.password_service = password_service

    def execute(self, aseguradora_id: str, dto: AjustadorCreateDTO) -> AjustadorModel:
        if self.auth_repo.get_by_email(dto.email):
            raise BusinessRuleError("El correo electrónico ya está registrado.")
            
        hashed_password = self.password_service.hash(dto.password_temporal)
        
        user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=dto.nombre,
            email=dto.email,
            telefono=dto.telefono,
            rol=Rol.AJUSTADOR.value,
            aseguradora_id=aseguradora_id,
            password=hashed_password,
            estado=EstadoUsuario.ACTIVO.value,
            fecha_creacion=datetime.now(timezone.utc)
        )
        saved_user = self.auth_repo.create(user)
        
        model = AjustadorModel(
            id=str(uuid.uuid4()),
            usuario_id=saved_user.usuario_id,
            cedula_profesional=dto.cedula_profesional,
            geolocalizacion_actual=None,
            activo_para_servicio=True,
            version=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        return self.repo.save(model)
