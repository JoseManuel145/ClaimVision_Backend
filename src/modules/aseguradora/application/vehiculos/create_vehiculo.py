from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel


class CreateVehiculo:
    def __init__(self, vehiculo_module: VehiculoModulePort):
        self.vehiculo_module = vehiculo_module

    def execute(
        self,
        aseguradora_id: str,
        cliente_id: str,
        marca: str,
        modelo: str,
        anio: int,
        placas: str,
        vin: str | None,
        color: str | None,
    ) -> VehiculoModel:
        return self.vehiculo_module.crear(
            aseguradora_id, cliente_id, marca, modelo, anio, placas, vin, color
        )
