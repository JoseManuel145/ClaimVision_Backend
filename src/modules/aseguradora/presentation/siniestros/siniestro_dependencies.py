from fastapi import Depends
from src.core.database import get_session
from src.modules.aseguradora.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.aseguradora.infra.db.repositories.ajustador_repository import AjustadorRepository
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.aseguradora.application.siniestros.list_siniestros import ListSiniestros
from src.modules.aseguradora.application.siniestros.asignar_ajustador import AsignarAjustador
from src.modules.aseguradora.application.siniestros.enviar_taller import EnviarTaller
from src.modules.aseguradora.application.siniestros.autorizar_entrega import AutorizarEntrega

def siniestro_repo(session=Depends(get_session)) -> SiniestroRepository:
    return SiniestroRepository(session)

def ajustador_repo(session=Depends(get_session)) -> AjustadorRepository:
    return AjustadorRepository(session)

def taller_repo(session=Depends(get_session)) -> TallerRepository:
    return TallerRepository(session)

def list_siniestros_service(repo: SiniestroRepository = Depends(siniestro_repo)) -> ListSiniestros:
    return ListSiniestros(repo)

def asignar_ajustador_service(
    repo: SiniestroRepository = Depends(siniestro_repo),
    aj_repo: AjustadorRepository = Depends(ajustador_repo)
) -> AsignarAjustador:
    return AsignarAjustador(repo, aj_repo)

def enviar_taller_service(
    repo: SiniestroRepository = Depends(siniestro_repo),
    tl_repo: TallerRepository = Depends(taller_repo)
) -> EnviarTaller:
    return EnviarTaller(repo, tl_repo)

def autorizar_entrega_service(repo: SiniestroRepository = Depends(siniestro_repo)) -> AutorizarEntrega:
    return AutorizarEntrega(repo)
