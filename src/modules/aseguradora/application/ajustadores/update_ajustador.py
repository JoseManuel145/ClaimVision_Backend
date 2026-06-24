from datetime import datetime
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.core.exceptions import NotFoundError

class UpdateAjustador:
    def __init__(self, repo: AjustadorRepositoryPort):
        self.repo = repo

    def execute(self, id: str, cedula_profesional: str | None, activo_para_servicio: bool | None) -> AjustadorModel:
        ajustador = self.repo.get_by_id(id)
        if not ajustador:
            raise NotFoundError("Ajustador no encontrado")
        
        if cedula_profesional is not None:
            ajustador.cedula_profesional = cedula_profesional
        if activo_para_servicio is not None:
            ajustador.activo_para_servicio = activo_para_servicio
            
        ajustador.updated_at = datetime.now()
        return self.repo.update(ajustador)
