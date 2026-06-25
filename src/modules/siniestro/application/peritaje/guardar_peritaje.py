from typing import List, Dict, Any
import uuid
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel, DanoAjustadoManualModel
from src.shared.domain.models import EstatusSiniestro

class GuardarPeritaje:
    def __init__(self, siniestro_repo: SiniestroRepositoryPort, peritaje_repo: PeritajeAjustadorRepositoryPort):
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo

    async def execute(self, ajustador_id: str, siniestro_id: str, costo_definitivo: float, firma: str, observaciones: str | None, danos_data: List[Dict[str, Any]]) -> PeritajeAjustadorModel:
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise ValueError("Siniestro no encontrado")
        
        if siniestro.ajustador_id != ajustador_id:
            raise PermissionError("No tienes permisos para modificar este siniestro")

        if siniestro.estatus in [EstatusSiniestro.PERITAJE_VALIDADO.value, EstatusSiniestro.ASIGNADO_A_TALLER.value, EstatusSiniestro.TRABAJO_CONCLUIDO.value, EstatusSiniestro.LISTO_PARA_ENTREGA.value, EstatusSiniestro.ENTREGADO.value]:
            raise ValueError("El siniestro ya fue validado y no puede ser modificado")

        danos = []
        for d in danos_data:
            danos.append(DanoAjustadoManualModel(
                id=str(uuid.uuid4()),
                peritaje_ajustador_id="",  # will be set by repo
                zona_vehiculo=d["zona_vehiculo"],
                tipo=d["tipo"],
                severidad=d["severidad"],
                costo_real_reparacion=d["costo_real_reparacion"],
                origen_cambio=d.get("origen_cambio", "AJUSTADOR"),
                version=1,
                created_at=None,
                updated_at=None,
                deleted_at=None
            ))

        peritaje = PeritajeAjustadorModel(
            id=str(uuid.uuid4()),
            siniestro_id=siniestro_id,
            ajustador_id=ajustador_id,
            costo_definitivo_ajustador=costo_definitivo,
            firma_digital_ajustador=firma,
            observaciones_campo=observaciones,
            danos=danos,
            version=1,
            created_at=None,
            updated_at=None,
            deleted_at=None
        )

        return self.peritaje_repo.guardar_peritaje(peritaje)
