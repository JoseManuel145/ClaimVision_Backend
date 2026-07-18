from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.logging import get_logger
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.peritaje_repository import PeritajeAjustadorRepository
from src.modules.taller.infra.db.repositories.cotizacion_repository import CotizacionRepository
from src.modules.taller.infra.db.repositories.perfil_taller_repository import PerfilTallerRepository
from src.modules.taller.infra.pdf.supabase_storage_repository import SupabasePdfStorage
from src.core.messaging.di import get_siniestro_notifier

from src.modules.taller.application.expedientes.list_expedientes import ListExpedientesTallerUseCase
from src.modules.taller.application.expedientes.get_expediente import GetExpedienteTallerUseCase
from src.modules.taller.application.expedientes.concluir_expediente import ConcluirExpedienteUseCase
from src.modules.taller.application.expedientes.marcar_listo_entrega import MarcarListoEntrega
from src.modules.taller.application.crear_cotizacion import CrearCotizacion
from src.modules.taller.application.editar_cotizacion import EditarCotizacion
from src.modules.taller.application.get_perfil_taller import GetPerfilTaller
from src.modules.taller.application.actualizar_perfil_taller import ActualizarPerfilTaller
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository

logger = get_logger("deps")


def get_perfil_taller_service(session: Session = Depends(get_session)) -> GetPerfilTaller:
    return GetPerfilTaller(PerfilTallerRepository(session), TallerRepository(session), AuthRepository(session))


def actualizar_perfil_taller_service(session: Session = Depends(get_session)) -> ActualizarPerfilTaller:
    return ActualizarPerfilTaller(PerfilTallerRepository(session), TallerRepository(session), AuthRepository(session))


def list_ordenes_service(session: Session = Depends(get_session)) -> ListExpedientesTallerUseCase:
    return ListExpedientesTallerUseCase(SiniestroRepository(session), PerfilTallerRepository(session))


def get_orden_service(session: Session = Depends(get_session)) -> GetExpedienteTallerUseCase:
    return GetExpedienteTallerUseCase(
        SiniestroRepository(session),
        PeritajeAjustadorRepository(session),
        CotizacionRepository(session),
        PerfilTallerRepository(session),
    )


def crear_cotizacion_service(session: Session = Depends(get_session)) -> CrearCotizacion:
    return CrearCotizacion(
        SiniestroRepository(session),
        CotizacionRepository(session),
        PerfilTallerRepository(session),
        PeritajeAjustadorRepository(session),
    )


def editar_cotizacion_service(session: Session = Depends(get_session)) -> EditarCotizacion:
    return EditarCotizacion(CotizacionRepository(session), PerfilTallerRepository(session))


def _safe_notifier(session: Session):
    try:
        return get_siniestro_notifier(session)
    except Exception as e:
        logger.warning(f"No se pudo inicializar el notificador de siniestros: {e}")
        return None


def concluir_trabajo_service(session: Session = Depends(get_session)) -> ConcluirExpedienteUseCase:
    return ConcluirExpedienteUseCase(
        SiniestroRepository(session),
        CotizacionRepository(session),
        PerfilTallerRepository(session),
        _safe_notifier(session),
    )


def listo_entrega_service(session: Session = Depends(get_session)) -> MarcarListoEntrega:
    return MarcarListoEntrega(
        SiniestroRepository(session),
        PerfilTallerRepository(session),
        _safe_notifier(session),
    )


def subir_pdf_service() -> SupabasePdfStorage:
    return SupabasePdfStorage()
