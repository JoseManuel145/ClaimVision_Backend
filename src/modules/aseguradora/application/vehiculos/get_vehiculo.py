from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel


class GetVehiculo:
    def __init__(self, vehiculo_module: VehiculoModulePort):
        self.vehiculo_module = vehiculo_module

    def execute(self, id: str) -> VehiculoModel:
        return self.vehiculo_module.obtener(id)
