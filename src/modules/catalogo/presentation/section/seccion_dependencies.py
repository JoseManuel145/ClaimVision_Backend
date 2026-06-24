from fastapi import Depends
from src.core.database import get_session
from src.modules.catalogo.app.sections import GetSecciones, CreateSeccion, UpdateSeccion, DeleteSeccion, GetByIdSeccion
from src.modules.catalogo.infra.sections.seccion_repository import SeccionRepository

def get_all_secciones(session = Depends(get_session)):
    repo = SeccionRepository(session)
    return GetSecciones(repo)

def create_seccion(session = Depends(get_session)):
    repo = SeccionRepository(session)
    return CreateSeccion(repo)

def update_seccion(session = Depends(get_session)):
    repo = SeccionRepository(session)
    return UpdateSeccion(repo)

def delete_seccion(session = Depends(get_session)):
    repo = SeccionRepository(session)
    return DeleteSeccion(repo)

def get_seccion_by_id(session = Depends(get_session)):
    repo = SeccionRepository(session)
    return GetByIdSeccion(repo)