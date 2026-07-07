from src.modules.ajustador.application._peritaje_base import _PeritajeEditorBase
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel


class EditarPeritaje(_PeritajeEditorBase):
    def execute(
        self,
        usuario_id: str,
        peritaje_id: str,
        costo_definitivo: float | None = None,
        firma: str | None = None,
        observaciones: str | None = None,
    ) -> PeritajeAjustadorModel:
        peritaje = self._cargar_editable(usuario_id, peritaje_id)
        if costo_definitivo is not None:
            peritaje.costo_definitivo_ajustador = costo_definitivo
        if firma is not None:
            peritaje.firma_digital_ajustador = firma
        if observaciones is not None:
            peritaje.observaciones_campo = observaciones
        return self.peritaje_repo.guardar_peritaje(peritaje)
