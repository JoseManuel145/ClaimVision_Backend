from typing import Any, Dict

from src.modules.ajustador.application._peritaje_base import _PeritajeEditorBase
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel, DanoAjustadoManualModel


def _to_dano(d: Dict[str, Any]) -> DanoAjustadoManualModel:
    import uuid
    return DanoAjustadoManualModel(
        id=str(uuid.uuid4()),
        peritaje_ajustador_id="",
        zona_vehiculo=d["zona_vehiculo"],
        tipo=d["tipo"],
        severidad=d["severidad"],
        costo_real_reparacion=d["costo_real_reparacion"],
        origen_cambio=d.get("origen_cambio", "AJUSTADOR"),
        version=1,
        created_at=None,
        updated_at=None,
        deleted_at=None,
    )


class AgregarDano(_PeritajeEditorBase):
    def execute(self, usuario_id: str, peritaje_id: str, dano_data: Dict[str, Any]) -> PeritajeAjustadorModel:
        peritaje = self._cargar_editable(usuario_id, peritaje_id)
        peritaje.danos.append(_to_dano(dano_data))
        return self.peritaje_repo.guardar_peritaje(peritaje)
