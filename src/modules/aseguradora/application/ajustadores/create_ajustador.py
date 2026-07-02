from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.presentation.ajustadores.ajustador_dto import AjustadorCreateDTO


class CreateAjustador:
    def __init__(self, ajustador_module: AjustadorModulePort):
        self.ajustador_module = ajustador_module

    def execute(self, aseguradora_id: str, dto: AjustadorCreateDTO) -> AjustadorModel:
        return self.ajustador_module.crear(
            aseguradora_id=aseguradora_id,
            nombre=dto.nombre,
            email=dto.email,
            telefono=dto.telefono,
            password_temporal=dto.password_temporal,
            cedula_profesional=dto.cedula_profesional,
        )
