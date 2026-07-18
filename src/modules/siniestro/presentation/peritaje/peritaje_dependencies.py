from fastapi import Depends
from src.core.database import get_session
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.peritaje_repository import PeritajeAjustadorRepository
from src.modules.siniestro.application.peritaje.list_asignados import ListSiniestrosAsignados
from src.modules.siniestro.application.peritaje.guardar_peritaje import GuardarPeritaje
from src.modules.siniestro.application.peritaje.confirmar_peritaje import ConfirmarPeritaje
from src.core.messaging.di import get_siniestro_notifier


def list_asignados_service(session=Depends(get_session)) -> ListSiniestrosAsignados:
    siniestro_repo = SiniestroRepository(session)
    return ListSiniestrosAsignados(siniestro_repo)

def guardar_peritaje_service(session=Depends(get_session)) -> GuardarPeritaje:
    siniestro_repo = SiniestroRepository(session)
    peritaje_repo = PeritajeAjustadorRepository(session)
    return GuardarPeritaje(siniestro_repo, peritaje_repo)

def confirmar_peritaje_service(session=Depends(get_session)) -> ConfirmarPeritaje:
    siniestro_repo = SiniestroRepository(session)
    peritaje_repo = PeritajeAjustadorRepository(session)
    notifier = get_siniestro_notifier(session)
    return ConfirmarPeritaje(siniestro_repo, peritaje_repo, notifier)
