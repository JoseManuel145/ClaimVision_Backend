from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel


class UpdateAjustador:
    def __init__(self, ajustador_module: AjustadorModulePort):
        self.ajustador_module = ajustador_module

    def execute(
        self,
        id: str,
        cedula_profesional: str | None,
        activo_para_servicio: bool | None,
    ) -> AjustadorModel:
        return self.ajustador_module.actualizar(id, cedula_profesional, activo_para_servicio)
