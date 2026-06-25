from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort

@dataclass
class ExpedienteTecnicoResult:
    siniestro: SiniestroModel
    peritaje_ajustador: Optional[PeritajeAjustadorModel]
    cotizacion: Optional[CotizacionTallerModel]

class GetExpedienteTallerUseCase:
    def __init__(
        self,
        siniestro_repo: SiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
        cotizacion_repo: CotizacionRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort
    ):
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo
        self.cotizacion_repo = cotizacion_repo
        self.perfil_taller_repo = perfil_taller_repo

    def execute(self, siniestro_id: str, usuario_id: str) -> ExpedienteTecnicoResult:
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise HTTPException(status_code=403, detail="El usuario no tiene un perfil de taller asignado.")
        
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise HTTPException(status_code=404, detail="Siniestro no encontrado.")
            
        if siniestro.taller_id != taller_id:
            raise HTTPException(status_code=403, detail="Este expediente no está asignado a tu taller.")
            
        peritaje = self.peritaje_repo.get_by_siniestro(siniestro_id)
        cotizacion = self.cotizacion_repo.get_by_siniestro(siniestro_id)
        
        return ExpedienteTecnicoResult(
            siniestro=siniestro,
            peritaje_ajustador=peritaje,
            cotizacion=cotizacion
        )
