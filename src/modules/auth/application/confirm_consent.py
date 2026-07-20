from datetime import datetime, timezone
from src.modules.auth.presentation.schemas import ConsentRequestDTO
from src.modules.auth.domain.ports import AuthPort
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError

class ConfirmConsent:
    def __init__(self, cliente_repo: ClienteRepositoryPort, auth_repo: AuthPort):
        self.cliente_repo = cliente_repo
        self.auth_repo = auth_repo

    def execute(self, usuario_id: str, data: ConsentRequestDTO) -> None:
        user = self.auth_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        if user.rol not in ("Cliente", "Tester_Global"):
            raise BusinessRuleError("Sólo los clientes pueden dar consentimiento explícito LFPDPPP.")
        
        profile = self.cliente_repo.get_by_usuario_id(usuario_id)
        if not profile:
            from src.modules.cliente.domain.models import ClienteProfile
            from uuid import uuid4
            profile = ClienteProfile(
                id=str(uuid4()),
                usuario_id=usuario_id,
                numero_poliza="",
                vigencia_poliza=datetime.now(timezone.utc).date(),
                curp_rfc_cifrado="",
                consentimiento_aviso_privacidad=data.aviso_privacidad,
                consentimiento_biometria=data.biometria,
                autoriza_transferencia_talleres=data.transferencia_talleres,
                fecha_consentimiento=datetime.now(timezone.utc),
                fecha_creacion=datetime.now(timezone.utc),
            )
            profile = self.cliente_repo.save(profile)


        if not data.aviso_privacidad:
            raise BusinessRuleError("El consentimiento del aviso de privacidad es obligatorio.")

        profile.consentimiento_aviso_privacidad = data.aviso_privacidad
        profile.consentimiento_biometria = data.biometria
        profile.autoriza_transferencia_talleres = data.transferencia_talleres
        profile.fecha_consentimiento = datetime.now(timezone.utc)

        self.cliente_repo.update(profile)
