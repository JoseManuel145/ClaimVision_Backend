from typing import List, Tuple
from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel


class ListVehiculos:
    def __init__(self, vehiculo_module: VehiculoModulePort):
        self.vehiculo_module = vehiculo_module

    def execute(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        cliente_id: str | None = None,
    ) -> Tuple[List[VehiculoModel], int]:
        return self.vehiculo_module.listar(aseguradora_id, offset, limit, cliente_id)
