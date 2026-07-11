from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort


class DeleteVehiculo:
    def __init__(self, vehiculo_module: VehiculoModulePort):
        self.vehiculo_module = vehiculo_module

    def execute(self, id: str) -> None:
        return self.vehiculo_module.eliminar(id)
