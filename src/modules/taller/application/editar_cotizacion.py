from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.shared.domain.models import EstatusCotizacion
from src.modules.taller.application._helpers import taller_id
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


class EditarCotizacion:
    def __init__(
        self,
        cotizacion_repo: CotizacionRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort,
    ):
        self.cotizacion_repo = cotizacion_repo
        self.perfil_taller_repo = perfil_taller_repo

    def execute(
        self,
        usuario_id: str,
        cotizacion_id: str,
        monto_mano_obra: float | None = None,
        monto_refacciones: float | None = None,
        monto_total: float | None = None,
        desglose_pdf_url: str | None = None,
        observaciones_tecnicas: str | None = None,
    ) -> CotizacionTallerModel:
        taller = taller_id(self.perfil_taller_repo, usuario_id)
        cotizacion = self.cotizacion_repo.get_by_id(cotizacion_id)
        if not cotizacion:
            raise NotFoundError("Cotización no encontrada")
        if cotizacion.taller_id != taller:
            raise ForbiddenError("Esta cotización no pertenece a tu taller.")
        if cotizacion.estatus != EstatusCotizacion.PENDIENTE_APROBACION.value:
            raise BusinessRuleError("Solo se puede editar una cotización en estatus 'Pendiente_Aprobacion'.")

        if monto_mano_obra is not None:
            cotizacion.monto_mano_obra = monto_mano_obra
        if monto_refacciones is not None:
            cotizacion.monto_refacciones = monto_refacciones
        if desglose_pdf_url is not None:
            cotizacion.desglose_pdf_url = desglose_pdf_url
        if observaciones_tecnicas is not None:
            cotizacion.observaciones_tecnicas = observaciones_tecnicas
        cotizacion.monto_total = (
            monto_total if monto_total is not None
            else cotizacion.monto_mano_obra + cotizacion.monto_refacciones
        )
        return self.cotizacion_repo.save(cotizacion)
