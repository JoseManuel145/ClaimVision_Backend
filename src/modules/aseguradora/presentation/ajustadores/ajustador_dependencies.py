from fastapi import Depends
from src.core.database import get_session
from sqlalchemy.orm import Session
from src.modules.aseguradora.infra.db.repositories.ajustador_repository import AjustadorRepository
from src.modules.aseguradora.infra.adapters.ajustador_adapter import AjustadorAdapter
from src.modules.aseguradora.application.ajustadores.create_ajustador import CreateAjustador
from src.modules.aseguradora.application.ajustadores.list_ajustadores import ListAjustadores
from src.modules.aseguradora.application.ajustadores.get_ajustador import GetAjustador
from src.modules.aseguradora.application.ajustadores.update_ajustador import UpdateAjustador
from src.modules.aseguradora.application.ajustadores.delete_ajustador import DeleteAjustador
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.security.password_service import PasswordService


def _adapter(session: Session = Depends(get_session)) -> AjustadorAdapter:
    return AjustadorAdapter(
        auth_repo=AuthRepository(session),
        ajustador_repo=AjustadorRepository(session),
        password_service=PasswordService(),
    )


def create_ajustador_service(module: AjustadorAdapter = Depends(_adapter)) -> CreateAjustador:
    return CreateAjustador(module)


def list_ajustadores_service(module: AjustadorAdapter = Depends(_adapter)) -> ListAjustadores:
    return ListAjustadores(module)


def get_ajustador_service(module: AjustadorAdapter = Depends(_adapter)) -> GetAjustador:
    return GetAjustador(module)


def update_ajustador_service(module: AjustadorAdapter = Depends(_adapter)) -> UpdateAjustador:
    return UpdateAjustador(module)


def delete_ajustador_service(module: AjustadorAdapter = Depends(_adapter)) -> DeleteAjustador:
    return DeleteAjustador(module)
