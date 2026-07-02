from src.modules.taller.domain.ports.taller_module_port import TallerModulePort
from src.modules.aseguradora.domain.models.taller_model import TallerModel


class GetTaller:
    def __init__(self, taller_module: TallerModulePort):
        self.taller_module = taller_module

    def execute(self, id: str) -> TallerModel:
        return self.taller_module.obtener(id)
