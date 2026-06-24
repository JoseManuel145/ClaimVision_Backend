from fastapi import Depends

from src.core.database import get_session
from src.modules.catalogo.app.sizes import (
    AsociarTalla,
    CreateTalla,
    DeleteTalla,
    DesasociarTalla,
    GetAllTallas,
    GetTallasByProducto,
    GetPTallaById,
    GetTallaById,
    UpdateTalla
)
from src.modules.catalogo.infra.sizes.talla_repository import TallaRepository, ProductoTallaRepository


def get_all_tallas(session=Depends(get_session)):
    repo = TallaRepository(session)
    return GetAllTallas(repo)


def get_talla_by_id(session=Depends(get_session)):
    repo = TallaRepository(session)
    return GetTallaById(repo)


def get_tallas_by_producto(session=Depends(get_session)):
    repo = ProductoTallaRepository(session)
    return GetTallasByProducto(repo)


def get_ptalla_by_id(session=Depends(get_session)):
    repo = ProductoTallaRepository(session)
    return GetPTallaById(repo)


def create_talla(session=Depends(get_session)):
    repo = TallaRepository(session)
    return CreateTalla(repo)


def update_talla(session=Depends(get_session)):
    repo = TallaRepository(session)
    return UpdateTalla(repo)


def delete_talla(session=Depends(get_session)):
    repo = TallaRepository(session)
    return DeleteTalla(repo)


def asociar_talla(session=Depends(get_session)):
    repo = ProductoTallaRepository(session)
    return AsociarTalla(repo)


def desasociar_talla(session=Depends(get_session)):
    repo = ProductoTallaRepository(session)
    return DesasociarTalla(repo)
