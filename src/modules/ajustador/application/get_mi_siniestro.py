from typing import List, Optional, Tuple

from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.imagen_siniestro_repository_port import ImagenSiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.modules.ajustador.application._helpers import resolver_ajustador_id
from src.core.exceptions import NotFoundError, ForbiddenError


class GetMiSiniestro:
    def __init__(
        self,
        ajustador_repo: AjustadorRepositoryPort,
        siniestro_repo: SiniestroRepositoryPort,
        imagen_repo: ImagenSiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
    ):
        self.ajustador_repo = ajustador_repo
        self.siniestro_repo = siniestro_repo
        self.imagen_repo = imagen_repo
        self.peritaje_repo = peritaje_repo

    def execute(
        self, usuario_id: str, siniestro_id: str
    ) -> Tuple[SiniestroModel, List[ImagenSiniestroModel], Optional[PeritajeAjustadorModel]]:
        ajustador_id = resolver_ajustador_id(self.ajustador_repo, usuario_id)
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.ajustador_id != ajustador_id:
            raise ForbiddenError("Este siniestro no está asignado al ajustador autenticado.")

        imagenes = self.imagen_repo.get_by_siniestro_id(siniestro_id)
        peritaje = self.peritaje_repo.obtener_peritaje_por_siniestro(siniestro_id)
        return siniestro, imagenes, peritaje
