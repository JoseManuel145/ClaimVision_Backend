"""Casos de uso del ajustador: registrar/editar peritaje y daños manuales."""
import uuid
from datetime import datetime
from typing import Any, Dict, List

from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel, DanoAjustadoManualModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.domain.transitions import validar_transicion
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError

from src.modules.ajustador.application.asignaciones import resolver_ajustador_id

_ESTADOS_BLOQUEADOS = {
    EstatusSiniestro.PERITAJE_VALIDADO.value,
    EstatusSiniestro.ASIGNADO_A_TALLER.value,
    EstatusSiniestro.TRABAJO_CONCLUIDO.value,
    EstatusSiniestro.LISTO_PARA_ENTREGA.value,
    EstatusSiniestro.ENTREGADO.value,
}


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
    """Crea el peritaje del ajustador y valida el siniestro → Peritaje_Validado."""

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

        # Asignado_A_Ajustador → Peritaje_Validado (lanza 409 si no aplica)
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


class _PeritajeEditorBase:
    def __init__(
        self,
        ajustador_repo: AjustadorRepositoryPort,
        siniestro_repo: SiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
    ):
        self.ajustador_repo = ajustador_repo
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo

    def _cargar_editable(self, usuario_id: str, peritaje_id: str) -> PeritajeAjustadorModel:
        ajustador_id = resolver_ajustador_id(self.ajustador_repo, usuario_id)
        peritaje = self.peritaje_repo.obtener_por_id(peritaje_id)
        if not peritaje:
            raise NotFoundError("Peritaje no encontrado")
        if peritaje.ajustador_id != ajustador_id:
            raise ForbiddenError("Este peritaje no pertenece al ajustador autenticado.")
        siniestro = self.siniestro_repo.get_by_id(peritaje.siniestro_id)
        if siniestro and siniestro.estatus in _ESTADOS_BLOQUEADOS:
            raise BusinessRuleError("El peritaje ya fue validado y no puede editarse.")
        return peritaje


class EditarPeritaje(_PeritajeEditorBase):
    """Edita el borrador del peritaje antes de validarlo."""

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


class AgregarDano(_PeritajeEditorBase):
    """Agrega un daño manual al peritaje (origen_cambio = AJUSTADOR)."""

    def execute(self, usuario_id: str, peritaje_id: str, dano_data: Dict[str, Any]) -> PeritajeAjustadorModel:
        peritaje = self._cargar_editable(usuario_id, peritaje_id)
        peritaje.danos.append(_to_dano(dano_data))
        return self.peritaje_repo.guardar_peritaje(peritaje)
