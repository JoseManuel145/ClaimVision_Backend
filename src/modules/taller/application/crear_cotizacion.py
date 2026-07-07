import uuid
from datetime import datetime, timezone

from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro, EstatusCotizacion
from src.modules.taller.application._helpers import taller_id
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


class CrearCotizacion:
    def __init__(
        self,
        siniestro_repo: SiniestroRepositoryPort,
        cotizacion_repo: CotizacionRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
    ):
        self.siniestro_repo = siniestro_repo
        self.cotizacion_repo = cotizacion_repo
        self.perfil_taller_repo = perfil_taller_repo
        self.peritaje_repo = peritaje_repo

    def execute(
        self,
        usuario_id: str,
        siniestro_id: str,
        monto_mano_obra: float,
        monto_refacciones: float,
        desglose_pdf_url: str,
        monto_total: float | None = None,
        observaciones_tecnicas: str | None = None,
    ) -> CotizacionTallerModel:
        taller = taller_id(self.perfil_taller_repo, usuario_id)
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.taller_id != taller:
            raise ForbiddenError("Este expediente no está asignado a tu taller.")
        if siniestro.estatus != EstatusSiniestro.ASIGNADO_A_TALLER.value:
            raise BusinessRuleError(
                f"Solo se puede cotizar un siniestro en estatus 'Asignado_A_Taller' (actual: '{siniestro.estatus}')."
            )
        if not self.peritaje_repo.get_by_siniestro(siniestro_id):
            raise BusinessRuleError("No se puede cotizar sin un peritaje validado del ajustador.")

        total = monto_total if monto_total is not None else monto_mano_obra + monto_refacciones
        now = datetime.now(timezone.utc)
        cotizacion = CotizacionTallerModel(
            id=str(uuid.uuid4()),
            siniestro_id=siniestro_id,
            taller_id=taller,
            monto_mano_obra=monto_mano_obra,
            monto_refacciones=monto_refacciones,
            monto_total=total,
            desglose_pdf_url=desglose_pdf_url,
            estatus=EstatusCotizacion.PENDIENTE_APROBACION.value,
            observaciones_tecnicas=observaciones_tecnicas,
            version=1,
            created_at=now,
            updated_at=now,
        )
        return self.cotizacion_repo.save(cotizacion)
