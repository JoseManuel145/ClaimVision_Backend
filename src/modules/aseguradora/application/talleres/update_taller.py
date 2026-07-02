from src.modules.taller.domain.ports.taller_module_port import TallerModulePort
from src.modules.aseguradora.domain.models.taller_model import TallerModel


class UpdateTaller:
    def __init__(self, taller_module: TallerModulePort):
        self.taller_module = taller_module

    def execute(
        self,
        id: str,
        nombre_comercial: str | None,
        direccion_tecnica: str | None,
        telefono_contacto: str | None,
    ) -> TallerModel:
        return self.taller_module.actualizar(id, nombre_comercial, direccion_tecnica, telefono_contacto)
