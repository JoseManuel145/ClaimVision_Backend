from src.modules.cliente.presentation.schemas import ConfirmDataRequestDTO
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.core.security import encrypt_xsalsa20


class ConfirmData:
    def __init__(self, cliente_repo: ClienteRepositoryPort, vehiculo_module: VehiculoModulePort):
        self.cliente_repo = cliente_repo
        self.vehiculo_module = vehiculo_module

    def execute(self, usuario_id: str, aseguradora_id: str, data: ConfirmDataRequestDTO) -> dict:
        profile = self.cliente_repo.get_by_usuario_id(usuario_id)
        if not profile:
            from src.modules.cliente.domain.models import ClienteProfile
            from uuid import uuid4
            from datetime import datetime, timezone
            profile = ClienteProfile(
                id=str(uuid4()),
                usuario_id=usuario_id,
                numero_poliza=data.numero_poliza,
                vigencia_poliza=data.vigencia_poliza,
                curp_rfc_cifrado=encrypt_xsalsa20(data.curp_rfc),
                consentimiento_aviso_privacidad=True,
                consentimiento_biometria=False,
                autoriza_transferencia_talleres=False,
                fecha_consentimiento=datetime.now(timezone.utc),
                fecha_creacion=datetime.now(timezone.utc),
            )
            profile = self.cliente_repo.save(profile)

        if not profile.consentimiento_aviso_privacidad:
            from datetime import datetime, timezone
            profile.consentimiento_aviso_privacidad = True
            profile.fecha_consentimiento = datetime.now(timezone.utc)

        profile.numero_poliza = data.numero_poliza
        profile.vigencia_poliza = data.vigencia_poliza
        profile.curp_rfc_cifrado = encrypt_xsalsa20(data.curp_rfc)
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
