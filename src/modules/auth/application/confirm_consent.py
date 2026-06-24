from datetime import datetime, timezone
from src.modules.auth.domain.ports import AuthPort
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError

class ConfirmConsent:
    def __init__(self, cliente_repo: ClienteRepositoryPort, auth_repo: AuthPort):
        self.cliente_repo = cliente_repo
        self.auth_repo = auth_repo

    def execute(self, usuario_id: str, aviso_privacidad: bool, biometria: bool, transferencia_talleres: bool) -> None:
        user = self.auth_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        if user.rol.value != "Cliente":
            raise BusinessRuleError("Sólo los clientes pueden dar consentimiento explícito LFPDPPP.")
        
        profile = self.cliente_repo.get_by_usuario_id(usuario_id)
        if not profile:
            raise NotFoundError("Perfil de cliente no inicializado. Contacte a su Aseguradora.")

        if not aviso_privacidad:
            raise BusinessRuleError("El consentimiento del aviso de privacidad es obligatorio.")

        profile.consentimiento_aviso_privacidad = aviso_privacidad
        profile.consentimiento_biometria = biometria
        profile.autoriza_transferencia_talleres = transferencia_talleres
        profile.fecha_consentimiento = datetime.now(timezone.utc)

        self.cliente_repo.update(profile)
