from datetime import datetime
from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.core.exceptions import NotFoundError

class UpdateTaller:
    def __init__(self, repo: TallerRepositoryPort):
        self.repo = repo

    def execute(self, id: str, nombre_comercial: str | None, direccion_tecnica: str | None, telefono_contacto: str | None) -> TallerModel:
        taller = self.repo.get_by_id(id)
        if not taller:
            raise NotFoundError("Taller no encontrado")
        
        if nombre_comercial is not None:
            taller.nombre_comercial = nombre_comercial
        if direccion_tecnica is not None:
            taller.direccion_tecnica = direccion_tecnica
        if telefono_contacto is not None:
            taller.telefono_contacto = telefono_contacto
            
        taller.updated_at = datetime.now()
        return self.repo.update(taller)
