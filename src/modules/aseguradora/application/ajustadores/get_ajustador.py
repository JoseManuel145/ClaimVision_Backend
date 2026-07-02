from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel


class GetAjustador:
    def __init__(self, ajustador_module: AjustadorModulePort):
        self.ajustador_module = ajustador_module

    def execute(self, id: str) -> AjustadorModel:
        return self.ajustador_module.obtener(id)
