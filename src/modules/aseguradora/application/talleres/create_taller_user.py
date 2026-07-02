from src.modules.taller.domain.ports.taller_module_port import TallerModulePort
from src.modules.aseguradora.presentation.talleres.taller_dto import OperadorTallerRequestDTO


class CreateOperadorTallerUseCase:
    def __init__(self, taller_module: TallerModulePort):
        self.taller_module = taller_module

    def execute(
        self,
        aseguradora_id: str,
        admin_id: str,
        taller_id: str,
        data: OperadorTallerRequestDTO,
    ) -> dict:
        return self.taller_module.crear_operador(aseguradora_id, admin_id, taller_id, data)
