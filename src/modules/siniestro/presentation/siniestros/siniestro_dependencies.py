from fastapi import Depends
from sqlalchemy.orm import Session
from src.core.database import get_session
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.imagen_siniestro_repository import ImagenSiniestroRepository
from src.modules.siniestro.infra.adapters.ajustador_checker_adapter import AjustadorCheckerAdapter
from src.modules.siniestro.infra.adapters.taller_checker_adapter import TallerCheckerAdapter
from src.modules.aseguradora.infra.db.repositories.ajustador_repository import AjustadorRepository
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.siniestro.infra.storage.supabase_storage import SupabaseStorageAdapter
from src.core.supabase import get_supabase_client

from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.subir_imagen_siniestro import SubirImagenSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros import ListSiniestros
from src.modules.siniestro.application.siniestros.asignar_ajustador import AsignarAjustador
from src.modules.siniestro.application.siniestros.enviar_taller import EnviarTaller
from src.modules.siniestro.application.siniestros.autorizar_entrega import AutorizarEntrega
from src.modules.siniestro.application.siniestros.editar_siniestro import EditarSiniestro

# Repositorios
def get_siniestro_repo(session: Session = Depends(get_session)) -> SiniestroRepository:
    return SiniestroRepository(session)

def get_imagen_siniestro_repo(session: Session = Depends(get_session)) -> ImagenSiniestroRepository:
    return ImagenSiniestroRepository(session)

def get_storage_port(client = Depends(get_supabase_client)) -> SupabaseStorageAdapter:
    return SupabaseStorageAdapter(client)

def get_ajustador_checker(session: Session = Depends(get_session)) -> AjustadorCheckerAdapter:
    # Consume el repo real de aseguradora
    repo = AjustadorRepository(session)
    return AjustadorCheckerAdapter(repo)

def get_taller_checker(session: Session = Depends(get_session)) -> TallerCheckerAdapter:
    # Consume el repo real de aseguradora
    repo = TallerRepository(session)
    return TallerCheckerAdapter(repo)

def get_cliente_checker(session: Session = Depends(get_session)):
    from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository
    from src.modules.siniestro.infra.adapters.cliente_checker_adapter import ClienteCheckerAdapter
    repo = ClienteRepository(session)
    return ClienteCheckerAdapter(repo)

# Casos de Uso
def inicializar_siniestro_service(
    repo: SiniestroRepository = Depends(get_siniestro_repo),
    cliente_checker=Depends(get_cliente_checker)
) -> InicializarSiniestro:
    return InicializarSiniestro(repo, cliente_checker)

def subir_imagen_siniestro_service(
    repo_img: ImagenSiniestroRepository = Depends(get_imagen_siniestro_repo),
    repo_sin: SiniestroRepository = Depends(get_siniestro_repo),
    storage: SupabaseStorageAdapter = Depends(get_storage_port)
) -> SubirImagenSiniestro:
    return SubirImagenSiniestro(repo_img, repo_sin, storage)

def list_siniestros_service(repo: SiniestroRepository = Depends(get_siniestro_repo)) -> ListSiniestros:
    return ListSiniestros(repo)

def asignar_ajustador_service(
    repo: SiniestroRepository = Depends(get_siniestro_repo),
    checker: AjustadorCheckerAdapter = Depends(get_ajustador_checker)
) -> AsignarAjustador:
    return AsignarAjustador(repo, checker)

def enviar_taller_service(
    repo: SiniestroRepository = Depends(get_siniestro_repo),
    checker: TallerCheckerAdapter = Depends(get_taller_checker)
) -> EnviarTaller:
    return EnviarTaller(repo, checker)

def autorizar_entrega_service(repo: SiniestroRepository = Depends(get_siniestro_repo)) -> AutorizarEntrega:
    return AutorizarEntrega(repo)

def editar_siniestro_service(repo: SiniestroRepository = Depends(get_siniestro_repo)) -> EditarSiniestro:
    return EditarSiniestro(repo)
