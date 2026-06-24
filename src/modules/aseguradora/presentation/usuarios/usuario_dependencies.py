from fastapi import Depends
from src.core.database import get_session
from src.modules.aseguradora.infra.db.repositories.usuario_repository import UsuarioRepository
from src.modules.aseguradora.application.usuarios.bloqueo_arco import BloqueoArcoAseguradora
from src.modules.aseguradora.application.usuarios.desbloqueo_arco import DesbloqueoArcoAseguradora

def usuario_repo(session=Depends(get_session)) -> UsuarioRepository:
    return UsuarioRepository(session)

def bloqueo_arco_service(repo: UsuarioRepository = Depends(usuario_repo)) -> BloqueoArcoAseguradora:
    return BloqueoArcoAseguradora(repo)

def desbloqueo_arco_service(repo: UsuarioRepository = Depends(usuario_repo)) -> DesbloqueoArcoAseguradora:
    return DesbloqueoArcoAseguradora(repo)
