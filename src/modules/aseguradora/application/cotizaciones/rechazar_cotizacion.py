from src.modules.aseguradora.application.cotizaciones._cotizacion_base import _CotizacionDecisionBase
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.shared.domain.models import EstatusCotizacion


class RechazarCotizacion(_CotizacionDecisionBase):
    def execute(self, cotizacion_id: str, aseguradora_id: str | None, motivo: str | None = None) -> CotizacionTallerModel:
        self._cargar_pendiente(cotizacion_id, aseguradora_id)
        return self.cotizacion_repo.update_estatus(cotizacion_id, EstatusCotizacion.RECHAZADA.value)
