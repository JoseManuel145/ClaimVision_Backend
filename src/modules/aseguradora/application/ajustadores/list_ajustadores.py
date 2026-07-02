from typing import List, Tuple
from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel


class ListAjustadores:
    def __init__(self, ajustador_module: AjustadorModulePort):
        self.ajustador_module = ajustador_module

    def execute(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        activo_para_servicio: bool | None = None,
    ) -> Tuple[List[AjustadorModel], int]:
        return self.ajustador_module.listar(aseguradora_id, offset, limit, activo_para_servicio)
