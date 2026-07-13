from datetime import date
from src.modules.ia_bridge.domain.ports import OcrStructuredPort
from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.ports.cliente_repository_port import ClienteRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError


class CreateVehiculoFromPoliza:
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
        self, aseguradora_id: str, cliente_id: str, pdf_bytes: bytes, filename: str
    ):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise NotFoundError(
                "El cliente especificado no existe. Use el campo 'id' del perfil de cliente."
            )

        poliza_data = await self.ocr_port.extract_poliza(pdf_bytes, filename)

        vehiculo = self.vehiculo_module.crear(
            aseguradora_id=aseguradora_id,
            cliente_id=cliente_id,
            marca=poliza_data.get("vehiculo_marca", ""),
            modelo=poliza_data.get("vehiculo_modelo", ""),
            anio=poliza_data.get("vehiculo_anio", 0),
            placas=poliza_data.get("vehiculo_placas", ""),
            vin=poliza_data.get("vehiculo_vin"),
            color=poliza_data.get("vehiculo_color"),
        )

        return vehiculo
