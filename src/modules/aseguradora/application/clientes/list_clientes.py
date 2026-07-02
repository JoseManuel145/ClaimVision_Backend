from typing import List, Tuple
from src.modules.cliente.domain.module_port import ClienteModulePort
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel


class ListClientes:
    def __init__(self, cliente_module: ClienteModulePort):
        self.cliente_module = cliente_module

    def execute(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[ClienteModel], int]:
        return self.cliente_module.listar(aseguradora_id, offset, limit)
