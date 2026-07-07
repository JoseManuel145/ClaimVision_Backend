from typing import List, Optional, Tuple

from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.imagen_siniestro_repository_port import ImagenSiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.core.exceptions import NotFoundError, ForbiddenError


class GetSiniestroAseguradora:
    def __init__(
        self,
        siniestro_repo: SiniestroRepositoryPort,
        imagen_repo: ImagenSiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
        cotizacion_repo: CotizacionRepositoryPort,
    ):
        self.siniestro_repo = siniestro_repo
        self.imagen_repo = imagen_repo
        self.peritaje_repo = peritaje_repo
        self.cotizacion_repo = cotizacion_repo

    def execute(
        self, siniestro_id: str, aseguradora_id: str | None
    ) -> Tuple[
        SiniestroModel,
        List[ImagenSiniestroModel],
        Optional[PeritajeAjustadorModel],
        Optional[CotizacionTallerModel],
    ]:
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if aseguradora_id is not None and siniestro.aseguradora_id != aseguradora_id:
            raise ForbiddenError("El siniestro no pertenece a tu aseguradora.")

        imagenes = self.imagen_repo.get_by_siniestro_id(siniestro_id)
        peritaje = self.peritaje_repo.get_by_siniestro(siniestro_id)
        cotizacion = self.cotizacion_repo.get_by_siniestro(siniestro_id)
        return siniestro, imagenes, peritaje, cotizacion
