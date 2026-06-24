from fastapi import Depends
from src.core.database import get_session
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.aseguradora.application.talleres.create_taller import CreateTaller
from src.modules.aseguradora.application.talleres.list_talleres import ListTalleres
from src.modules.aseguradora.application.talleres.get_taller import GetTaller
from src.modules.aseguradora.application.talleres.update_taller import UpdateTaller
from src.modules.aseguradora.application.talleres.delete_taller import DeleteTaller

def taller_repo(session=Depends(get_session)) -> TallerRepository:
    return TallerRepository(session)

def create_taller_service(repo: TallerRepository = Depends(taller_repo)) -> CreateTaller:
    return CreateTaller(repo)

def list_talleres_service(repo: TallerRepository = Depends(taller_repo)) -> ListTalleres:
    return ListTalleres(repo)

def get_taller_service(repo: TallerRepository = Depends(taller_repo)) -> GetTaller:
    return GetTaller(repo)

def update_taller_service(repo: TallerRepository = Depends(taller_repo)) -> UpdateTaller:
    return UpdateTaller(repo)

def delete_taller_service(repo: TallerRepository = Depends(taller_repo)) -> DeleteTaller:
    return DeleteTaller(repo)
