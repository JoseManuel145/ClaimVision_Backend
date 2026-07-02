"""
Autorización de entrega por la aseguradora (§3). Corrige la transición respecto
al usecase legacy: el spec define `Listo_Para_Entrega → Entregado` (el paso
`Trabajo_Concluido → Listo_Para_Entrega` lo realiza el taller en §6).
"""
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.domain.transitions import validar_transicion
from src.core.exceptions import NotFoundError, ForbiddenError


class AutorizarEntregaV1:
    def __init__(self, repo: SiniestroRepositoryPort):
        self.repo = repo

    def execute(self, siniestro_id: str, aseguradora_id: str | None) -> SiniestroModel:
        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if aseguradora_id is not None and siniestro.aseguradora_id != aseguradora_id:
            raise ForbiddenError("El siniestro no pertenece a tu aseguradora.")

        validar_transicion(siniestro.estatus, EstatusSiniestro.ENTREGADO.value)
        return self.repo.update_estatus(siniestro_id, EstatusSiniestro.ENTREGADO.value)
