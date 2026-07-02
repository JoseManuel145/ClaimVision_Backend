from fastapi import Depends
from src.core.database import get_session
from sqlalchemy.orm import Session
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.aseguradora.infra.adapters.taller_adapter import TallerAdapter
from src.modules.aseguradora.application.talleres.create_taller import CreateTaller
from src.modules.aseguradora.application.talleres.list_talleres import ListTalleres
from src.modules.aseguradora.application.talleres.get_taller import GetTaller
from src.modules.aseguradora.application.talleres.update_taller import UpdateTaller
from src.modules.aseguradora.application.talleres.delete_taller import DeleteTaller
from src.modules.aseguradora.application.talleres.create_taller_user import CreateOperadorTallerUseCase
from src.modules.taller.infra.db.repositories.perfil_taller_repository import PerfilTallerRepository
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.security.password_service import PasswordService


def _adapter(session: Session = Depends(get_session)) -> TallerAdapter:
    return TallerAdapter(
        taller_repo=TallerRepository(session),
        perfil_taller_repo=PerfilTallerRepository(session),
        auth_repo=AuthRepository(session),
        password_port=PasswordService(),
    )


def create_taller_service(module: TallerAdapter = Depends(_adapter)) -> CreateTaller:
    return CreateTaller(module)


def list_talleres_service(module: TallerAdapter = Depends(_adapter)) -> ListTalleres:
    return ListTalleres(module)


def get_taller_service(module: TallerAdapter = Depends(_adapter)) -> GetTaller:
    return GetTaller(module)


def update_taller_service(module: TallerAdapter = Depends(_adapter)) -> UpdateTaller:
    return UpdateTaller(module)


def delete_taller_service(module: TallerAdapter = Depends(_adapter)) -> DeleteTaller:
    return DeleteTaller(module)


def crear_operador_taller_service(module: TallerAdapter = Depends(_adapter)) -> CreateOperadorTallerUseCase:
    return CreateOperadorTallerUseCase(module)
