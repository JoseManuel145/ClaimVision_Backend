from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel


class UpdateVehiculo:
    def __init__(self, vehiculo_module: VehiculoModulePort):
        self.vehiculo_module = vehiculo_module

    def execute(
        self,
        id: str,
        marca: str | None,
        modelo: str | None,
        anio: int | None,
        placas: str | None,
        vin: str | None,
        color: str | None,
    ) -> VehiculoModel:
        return self.vehiculo_module.actualizar(id, marca, modelo, anio, placas, vin, color)
