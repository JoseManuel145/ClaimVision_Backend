"""
Casos de uso de cotización del taller (contrato §6 del spec): el taller envía
`desglose_pdf_url` (PDF ya subido vía URL prefirmada §8) y los montos. No genera
el PDF en el servidor (eso lo hace el flujo legacy de presupuestos).
"""
import uuid
from datetime import datetime, timezone

from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro, EstatusCotizacion
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


def _taller_id(perfil_repo: PerfilTallerRepositoryPort, usuario_id: str) -> str:
    taller_id = perfil_repo.get_taller_id_by_usuario(usuario_id)
    if not taller_id:
        raise ForbiddenError("El usuario no tiene un perfil de taller asignado.")
    return taller_id


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
        taller_id = _taller_id(self.perfil_taller_repo, usuario_id)
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.taller_id != taller_id:
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
            taller_id=taller_id,
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
        taller_id = _taller_id(self.perfil_taller_repo, usuario_id)
        cotizacion = self.cotizacion_repo.get_by_id(cotizacion_id)
        if not cotizacion:
            raise NotFoundError("Cotización no encontrada")
        if cotizacion.taller_id != taller_id:
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
