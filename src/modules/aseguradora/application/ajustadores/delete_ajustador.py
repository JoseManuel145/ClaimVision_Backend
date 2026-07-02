from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort


class DeleteAjustador:
    def __init__(self, ajustador_module: AjustadorModulePort):
        self.ajustador_module = ajustador_module

    def execute(self, id: str) -> None:
        return self.ajustador_module.eliminar(id)
