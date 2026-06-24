from fastapi import Depends
from src.core.database import get_session
from src.modules.aseguradora.infra.db.repositories.ajustador_repository import AjustadorRepository
from src.modules.aseguradora.application.ajustadores.create_ajustador import CreateAjustador
from src.modules.aseguradora.application.ajustadores.list_ajustadores import ListAjustadores
from src.modules.aseguradora.application.ajustadores.get_ajustador import GetAjustador
from src.modules.aseguradora.application.ajustadores.update_ajustador import UpdateAjustador
from src.modules.aseguradora.application.ajustadores.delete_ajustador import DeleteAjustador
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.security.password_service import PasswordService

def ajustador_repo(session=Depends(get_session)) -> AjustadorRepository:
    return AjustadorRepository(session)

def create_ajustador_service(session=Depends(get_session), repo: AjustadorRepository = Depends(ajustador_repo)) -> CreateAjustador:
    auth_repo = AuthRepository(session)
    password_service = PasswordService()
    return CreateAjustador(auth_repo, repo, password_service)

def list_ajustadores_service(repo: AjustadorRepository = Depends(ajustador_repo)) -> ListAjustadores:
    return ListAjustadores(repo)

def get_ajustador_service(repo: AjustadorRepository = Depends(ajustador_repo)) -> GetAjustador:
    return GetAjustador(repo)

def update_ajustador_service(repo: AjustadorRepository = Depends(ajustador_repo)) -> UpdateAjustador:
    return UpdateAjustador(repo)

def delete_ajustador_service(repo: AjustadorRepository = Depends(ajustador_repo)) -> DeleteAjustador:
    return DeleteAjustador(repo)
