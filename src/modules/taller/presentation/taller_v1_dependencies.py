from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.peritaje_repository import PeritajeAjustadorRepository
from src.modules.taller.infra.db.repositories.cotizacion_repository import CotizacionRepository
from src.modules.taller.infra.db.repositories.perfil_taller_repository import PerfilTallerRepository

from src.modules.taller.application.expedientes.list_expedientes import ListExpedientesTallerUseCase
from src.modules.taller.application.expedientes.get_expediente import GetExpedienteTallerUseCase
from src.modules.taller.application.expedientes.concluir_expediente import ConcluirExpedienteUseCase
from src.modules.taller.application.expedientes.marcar_listo_entrega import MarcarListoEntrega
from src.modules.taller.application.crear_cotizacion import CrearCotizacion
from src.modules.taller.application.editar_cotizacion import EditarCotizacion


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


def concluir_trabajo_service(session: Session = Depends(get_session)) -> ConcluirExpedienteUseCase:
    return ConcluirExpedienteUseCase(
        SiniestroRepository(session),
        CotizacionRepository(session),
        PerfilTallerRepository(session),
    )


def listo_entrega_service(session: Session = Depends(get_session)) -> MarcarListoEntrega:
    return MarcarListoEntrega(SiniestroRepository(session), PerfilTallerRepository(session))
