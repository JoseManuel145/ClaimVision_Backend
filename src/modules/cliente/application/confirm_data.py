from src.modules.cliente.presentation.schemas import ConfirmDataRequestDTO
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.core.security import encrypt_aes256


class ConfirmData:
    def __init__(self, cliente_repo: ClienteRepositoryPort, vehiculo_module: VehiculoModulePort):
        self.cliente_repo = cliente_repo
        self.vehiculo_module = vehiculo_module

    def execute(self, usuario_id: str, aseguradora_id: str, data: ConfirmDataRequestDTO) -> dict:
        profile = self.cliente_repo.get_by_usuario_id(usuario_id)
        if not profile:
            raise NotFoundError("Perfil de cliente no encontrado.")

        if not profile.consentimiento_aviso_privacidad:
            raise BusinessRuleError(
                "No se pueden guardar datos sensibles sin el consentimiento previo del aviso de privacidad."
            )

        profile.numero_poliza = data.numero_poliza
        profile.vigencia_poliza = data.vigencia_poliza
        profile.curp_rfc_cifrado = encrypt_aes256(data.curp_rfc)
        self.cliente_repo.update(profile)

        vehiculo = self.vehiculo_module.crear(
            aseguradora_id=aseguradora_id,
            cliente_id=profile.id,
            marca=data.vehiculo_marca,
            modelo=data.vehiculo_modelo,
            anio=data.vehiculo_anio,
            placas=data.vehiculo_placas,
            vin=data.vehiculo_vin,
            color=data.vehiculo_color,
        )

        return {"message": "Datos confirmados y vehículo registrado.", "vehiculo_id": vehiculo.id}
