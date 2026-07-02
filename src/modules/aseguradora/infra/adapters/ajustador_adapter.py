from datetime import datetime, timezone
import uuid
from typing import List, Tuple

from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.modules.auth.domain.ports import AuthPort
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.auth.domain.models import User
from src.shared.domain.models import Rol, EstadoUsuario
from src.core.exceptions import NotFoundError, BusinessRuleError


class AjustadorAdapter(AjustadorModulePort):
    def __init__(
        self,
        auth_repo: AuthPort,
        ajustador_repo: AjustadorRepositoryPort,
        password_service: PasswordService,
    ):
        self.auth_repo = auth_repo
        self.repo = ajustador_repo
        self.password_service = password_service

    def crear(
        self,
        aseguradora_id: str,
        nombre: str,
        email: str,
        telefono: str,
        password_temporal: str,
        cedula_profesional: str,
    ) -> AjustadorModel:
        if self.auth_repo.get_by_email(email):
            raise BusinessRuleError("El correo electrónico ya está registrado.")

        hashed_password = self.password_service.hash(password_temporal)

        user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=nombre,
            email=email,
            telefono=telefono,
            rol=Rol.AJUSTADOR.value,
            aseguradora_id=aseguradora_id,
            password=hashed_password,
            estado=EstadoUsuario.ACTIVO.value,
            fecha_creacion=datetime.now(timezone.utc),
        )
        saved_user = self.auth_repo.create(user)

        model = AjustadorModel(
            id=str(uuid.uuid4()),
            usuario_id=saved_user.usuario_id,
            cedula_profesional=cedula_profesional,
            geolocalizacion_actual=None,
            activo_para_servicio=True,
            version=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return self.repo.save(model)

    def obtener(self, ajustador_id: str) -> AjustadorModel:
        ajustador = self.repo.get_by_id(ajustador_id)
        if not ajustador:
            raise NotFoundError("Ajustador no encontrado")
        return ajustador

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        activo_para_servicio: bool | None = None,
    ) -> Tuple[List[AjustadorModel], int]:
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit, activo_para_servicio)

    def actualizar(
        self,
        ajustador_id: str,
        cedula_profesional: str | None,
        activo_para_servicio: bool | None,
    ) -> AjustadorModel:
        ajustador = self.repo.get_by_id(ajustador_id)
        if not ajustador:
            raise NotFoundError("Ajustador no encontrado")

        if cedula_profesional is not None:
            ajustador.cedula_profesional = cedula_profesional
        if activo_para_servicio is not None:
            ajustador.activo_para_servicio = activo_para_servicio
        ajustador.updated_at = datetime.now()
        return self.repo.update(ajustador)

    def eliminar(self, ajustador_id: str) -> None:
        ajustador = self.repo.get_by_id(ajustador_id)
        if not ajustador:
            raise NotFoundError("Ajustador no encontrado")
        self.repo.delete(ajustador_id)
