"""
Aprobación/rechazo de cotizaciones por el operador de la aseguradora (§3).
Valida pertenencia multi-tenant (`aseguradora_id`) y la transición de
`estatus_cotizacion` (solo desde Pendiente_Aprobacion).
"""
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.shared.domain.models import EstatusCotizacion
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


class _CotizacionDecisionBase:
    def __init__(self, cotizacion_repo: CotizacionRepositoryPort, siniestro_repo: SiniestroRepositoryPort):
        self.cotizacion_repo = cotizacion_repo
        self.siniestro_repo = siniestro_repo

    def _cargar_pendiente(self, cotizacion_id: str, aseguradora_id: str | None) -> CotizacionTallerModel:
        cotizacion = self.cotizacion_repo.get_by_id(cotizacion_id)
        if not cotizacion:
            raise NotFoundError("Cotización no encontrada")
        siniestro = self.siniestro_repo.get_by_id(cotizacion.siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro asociado no encontrado")
        # Multi-tenant: el Administrador_Global pasa con aseguradora_id None.
        if aseguradora_id is not None and siniestro.aseguradora_id != aseguradora_id:
            raise ForbiddenError("La cotización no pertenece a tu aseguradora.")
        if cotizacion.estatus != EstatusCotizacion.PENDIENTE_APROBACION.value:
            raise BusinessRuleError(
                f"Solo se puede decidir una cotización en 'Pendiente_Aprobacion' (actual: '{cotizacion.estatus}')."
            )
        return cotizacion


class AprobarCotizacion(_CotizacionDecisionBase):
    def execute(self, cotizacion_id: str, aseguradora_id: str | None) -> CotizacionTallerModel:
        self._cargar_pendiente(cotizacion_id, aseguradora_id)
        return self.cotizacion_repo.update_estatus(cotizacion_id, EstatusCotizacion.APROBADA.value)


class RechazarCotizacion(_CotizacionDecisionBase):
    def execute(self, cotizacion_id: str, aseguradora_id: str | None, motivo: str | None = None) -> CotizacionTallerModel:
        # `motivo` no tiene columna en `cotizaciones_taller`; se persiste solo en
        # la auditoría (logs_auditoria) desde la capa de presentación.
        self._cargar_pendiente(cotizacion_id, aseguradora_id)
        return self.cotizacion_repo.update_estatus(cotizacion_id, EstatusCotizacion.RECHAZADA.value)
