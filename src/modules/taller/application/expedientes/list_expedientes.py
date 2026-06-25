from typing import List, Tuple
from fastapi import HTTPException
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort

class ListExpedientesTallerUseCase:
    def __init__(
        self,
        siniestro_repo: SiniestroRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort
    ):
        self.siniestro_repo = siniestro_repo
        self.perfil_taller_repo = perfil_taller_repo

    def execute(self, usuario_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None) -> Tuple[List[SiniestroModel], int]:
        # Get the taller_id associated with this user
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise HTTPException(status_code=403, detail="El usuario no tiene un perfil de taller asignado.")
        
        return self.siniestro_repo.list_by_taller(taller_id=taller_id, offset=offset, limit=limit, estatus=estatus)
