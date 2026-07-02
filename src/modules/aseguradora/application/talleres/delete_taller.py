from src.modules.taller.domain.ports.taller_module_port import TallerModulePort


class DeleteTaller:
    def __init__(self, taller_module: TallerModulePort):
        self.taller_module = taller_module

    def execute(self, id: str, aseguradora_id: str) -> None:
        return self.taller_module.eliminar(id, aseguradora_id)
