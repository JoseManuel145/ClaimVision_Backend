from src.shared.domain.models import EstadoUsuario
from src.shared.domain.models import Rol
import uuid
from datetime import datetime, timezone
from src.modules.auth.domain.models import User
from src.modules.auth.domain.ports import AuthPort
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.cliente.domain.models import ClienteProfile
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.core.exceptions import BusinessRuleError
from src.modules.aseguradora.presentation.clientes.cliente_dto import ClienteCreateDTO

class CreateClienteByAseguradora:
    def __init__(self, auth_repo: AuthPort, cliente_repo: ClienteRepositoryPort, password_service: PasswordService):
        self.auth_repo = auth_repo
        self.cliente_repo = cliente_repo
        self.password_service = password_service

    def execute(self, aseguradora_id: str, dto: ClienteCreateDTO) -> ClienteProfile:
        if self.auth_repo.get_by_email(dto.email):
            raise BusinessRuleError("El correo electrónico ya está registrado.")
        
        hashed_password = self.password_service.hash(dto.password_temporal)
        
        user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=dto.nombre,
            email=dto.email,
            telefono=dto.telefono,
            rol=Rol.CLIENTE.value,
            aseguradora_id=aseguradora_id,
            password=hashed_password,
            estado=EstadoUsuario.ACTIVO.value,
            fecha_creacion=datetime.now(timezone.utc)
        )
        saved_user = self.auth_repo.create(user)

        # Inicializamos el perfil de cliente vacío para que posteriormente lo llene el onboarding/OCR
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
            fecha_creacion=datetime.now(timezone.utc)
        )
        self.cliente_repo.save(profile)

        return profile
