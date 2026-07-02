from src.modules.taller.domain.ports.taller_module_port import TallerModulePort
from src.modules.aseguradora.domain.models.taller_model import TallerModel


class CreateTaller:
    def __init__(self, taller_module: TallerModulePort):
        self.taller_module = taller_module

    def execute(
        self,
        aseguradora_id: str,
        nombre_comercial: str,
        rfc: str,
        direccion_tecnica: str,
        telefono_contacto: str,
    ) -> TallerModel:
        return self.taller_module.crear(
            aseguradora_id, nombre_comercial, rfc, direccion_tecnica, telefono_contacto
        )
