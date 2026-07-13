from datetime import date
from src.modules.ia_bridge.domain.ports import OcrStructuredPort
from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError


class CreateVehicleFromPoliza:
    def __init__(
        self,
        ocr_port: OcrStructuredPort,
        vehiculo_module: VehiculoModulePort,
        cliente_repo: ClienteRepositoryPort,
    ):
        self.ocr_port = ocr_port
        self.vehiculo_module = vehiculo_module
        self.cliente_repo = cliente_repo

    async def execute(
        self, usuario_id: str, aseguradora_id: str, pdf_bytes: bytes, filename: str
    ):
        perfil = self.cliente_repo.get_by_usuario_id(usuario_id)
        if not perfil:
            raise NotFoundError("Perfil de cliente no encontrado.")

        if not perfil.consentimiento_aviso_privacidad:
            raise BusinessRuleError(
                "Debe aceptar el aviso de privacidad antes de registrar documentos."
            )

        poliza_data = await self.ocr_port.extract_poliza(pdf_bytes, filename)

        vehiculo = self.vehiculo_module.crear(
            aseguradora_id=aseguradora_id,
            cliente_id=perfil.id,
            marca=poliza_data.get("vehiculo_marca", ""),
            modelo=poliza_data.get("vehiculo_modelo", ""),
            anio=poliza_data.get("vehiculo_anio", 0),
            placas=poliza_data.get("vehiculo_placas", ""),
            vin=poliza_data.get("vehiculo_vin"),
            color=poliza_data.get("vehiculo_color"),
        )

        numero_poliza = poliza_data.get("numero_poliza", "")
        vigencia_fin = poliza_data.get("vigencia_fin", "")

        if numero_poliza and perfil.numero_poliza == "PENDIENTE":
            perfil.numero_poliza = numero_poliza
            if vigencia_fin:
                try:
                    perfil.vigencia_poliza = date.fromisoformat(vigencia_fin)
                except ValueError:
                    pass
            self.cliente_repo.update(perfil)

        return vehiculo
