from datetime import datetime
from typing import Tuple
from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort

class CreateTaller:
    def __init__(self, repo: TallerRepositoryPort):
        self.repo = repo

    def execute(self, aseguradora_id: str, nombre_comercial: str, rfc: str, direccion_tecnica: str, telefono_contacto: str) -> TallerModel:
        model = TallerModel(
            id="",
            nombre_comercial=nombre_comercial,
            rfc=rfc,
            direccion_tecnica=direccion_tecnica,
            telefono_contacto=telefono_contacto,
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        taller = self.repo.save(model)
        self.repo.vincular_taller_aseguradora(taller.id, aseguradora_id)
        return taller
