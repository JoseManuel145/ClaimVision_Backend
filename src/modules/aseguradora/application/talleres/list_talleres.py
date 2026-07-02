from typing import List, Tuple
from src.modules.taller.domain.ports.taller_module_port import TallerModulePort
from src.modules.aseguradora.domain.models.taller_model import TallerModel


class ListTalleres:
    def __init__(self, taller_module: TallerModulePort):
        self.taller_module = taller_module

    def execute(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[TallerModel], int]:
        return self.taller_module.listar(aseguradora_id, offset, limit)
