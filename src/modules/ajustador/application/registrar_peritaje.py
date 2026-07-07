import uuid
from typing import Any, Dict, List

from src.modules.ajustador.application._helpers import resolver_ajustador_id
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel, DanoAjustadoManualModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.domain.transitions import validar_transicion
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


def _to_dano(d: Dict[str, Any]) -> DanoAjustadoManualModel:
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


class RegistrarPeritaje:
    def __init__(
        self,
        ajustador_repo: AjustadorRepositoryPort,
        siniestro_repo: SiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
    ):
        self.ajustador_repo = ajustador_repo
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo

    def execute(
        self,
        usuario_id: str,
        siniestro_id: str,
        costo_definitivo: float,
        firma: str,
        observaciones: str | None,
        danos_data: List[Dict[str, Any]],
    ) -> PeritajeAjustadorModel:
        ajustador_id = resolver_ajustador_id(self.ajustador_repo, usuario_id)
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.ajustador_id != ajustador_id:
            raise ForbiddenError("Este siniestro no está asignado al ajustador autenticado.")
        if not firma:
            raise BusinessRuleError("El peritaje requiere firma digital del ajustador.")

        validar_transicion(siniestro.estatus, EstatusSiniestro.PERITAJE_VALIDADO.value)

        peritaje = PeritajeAjustadorModel(
            id=str(uuid.uuid4()),
            siniestro_id=siniestro_id,
            ajustador_id=ajustador_id,
            costo_definitivo_ajustador=costo_definitivo,
            firma_digital_ajustador=firma,
            observaciones_campo=observaciones,
            danos=[_to_dano(d) for d in danos_data],
            version=1,
            created_at=None,
            updated_at=None,
            deleted_at=None,
        )
        guardado = self.peritaje_repo.guardar_peritaje(peritaje)
        self.siniestro_repo.update_estatus(siniestro_id, EstatusSiniestro.PERITAJE_VALIDADO.value)
        return guardado
