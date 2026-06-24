from datetime import date
from src.modules.cliente.presentation.schemas import ConfirmDataRequestDTO
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.core.security import encrypt_aes256

class ConfirmData:
    def __init__(self, cliente_repo: ClienteRepositoryPort):
        self.cliente_repo = cliente_repo

    def execute(self, usuario_id: str, data: ConfirmDataRequestDTO) -> None:
        profile = self.cliente_repo.get_by_usuario_id(usuario_id)
        if not profile:
            raise NotFoundError("Perfil de cliente no encontrado.")
        
        if not profile.consentimiento_aviso_privacidad:
            raise BusinessRuleError("No se pueden guardar datos sensibles sin el consentimiento previo del aviso de privacidad.")

        profile.numero_poliza = data.numero_poliza
        profile.vigencia_poliza = data.vigencia_poliza
        profile.curp_rfc_cifrado = encrypt_aes256(data.curp_rfc)

        self.cliente_repo.update(profile)
