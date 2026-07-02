import uuid
from datetime import datetime, timezone
from typing import List, Tuple

from src.modules.cliente.domain.module_port import ClienteModulePort
from src.modules.cliente.domain.models import ClienteProfile
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel
from src.modules.aseguradora.domain.ports.cliente_repository_port import ClienteRepositoryPort
from src.modules.auth.domain.ports import AuthPort
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.auth.domain.models import User
from src.shared.domain.models import Rol, EstadoUsuario
from src.core.exceptions import NotFoundError, BusinessRuleError


class ClienteAdapter(ClienteModulePort):
    def __init__(
        self,
        auth_repo: AuthPort,
        cliente_repo: ClienteRepositoryPort,
        cliente_module_repo,
        password_service: PasswordService,
    ):
        self.auth_repo = auth_repo
        self.repo = cliente_repo
        self.cliente_module_repo = cliente_module_repo
        self.password_service = password_service

    def crear(
        self,
        aseguradora_id: str,
        nombre: str,
        email: str,
        telefono: str,
        password_temporal: str,
    ) -> ClienteProfile:
        if self.auth_repo.get_by_email(email):
            raise BusinessRuleError("El correo electrónico ya está registrado.")

        hashed_password = self.password_service.hash(password_temporal)

        user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=nombre,
            email=email,
            telefono=telefono,
            rol=Rol.CLIENTE.value,
            aseguradora_id=aseguradora_id,
            password=hashed_password,
            estado=EstadoUsuario.ACTIVO.value,
            fecha_creacion=datetime.now(timezone.utc),
        )
        saved_user = self.auth_repo.create(user)

        profile = ClienteProfile(
            id=str(uuid.uuid4()),
            usuario_id=saved_user.usuario_id,
            numero_poliza="PENDIENTE",
            vigencia_poliza=datetime.now(timezone.utc).date(),
            curp_rfc_cifrado="PENDIENTE",
            consentimiento_aviso_privacidad=False,
            consentimiento_biometria=False,
            autoriza_transferencia_talleres=False,
            fecha_consentimiento=None,
            fecha_creacion=datetime.now(timezone.utc),
        )
        self.cliente_module_repo.save(profile)
        return profile

    def obtener(self, cliente_id: str) -> ClienteModel:
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundError("Cliente no encontrado")
        return cliente

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[ClienteModel], int]:
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit)
