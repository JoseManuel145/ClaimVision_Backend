from fastapi import Depends

from src.core.database import get_session
from src.modules.catalogo.app.colors import (
    AsociarColor,
    CreateColor,
    DeleteColor,
    DesasociarColor,
    GetAllColors,
    GetColorById,
    GetColoresByProducto,
    GetPColorById,
    UpdateColor
)
from src.modules.catalogo.infra.colors.color_repository import ColorRepository, ProductoColorRepository


def get_all_colors(session=Depends(get_session)):
    repo = ColorRepository(session)
    return GetAllColors(repo)


def get_color_by_id(session=Depends(get_session)):
    repo = ColorRepository(session)
    return GetColorById(repo)


def get_colores_by_producto(session=Depends(get_session)):
    repo = ProductoColorRepository(session)
    return GetColoresByProducto(repo)


def get_pcolor_by_id(session=Depends(get_session)):
    repo = ProductoColorRepository(session)
    return GetPColorById(repo)


def create_color(session=Depends(get_session)):
    repo = ColorRepository(session)
    return CreateColor(repo)


def update_color(session=Depends(get_session)):
    repo = ColorRepository(session)
    return UpdateColor(repo)


def delete_color(session=Depends(get_session)):
    repo = ColorRepository(session)
    return DeleteColor(repo)


def asociar_color(session=Depends(get_session)):
    repo = ProductoColorRepository(session)
    return AsociarColor(repo)


def desasociar_color(session=Depends(get_session)):
    repo = ProductoColorRepository(session)
    return DesasociarColor(repo)
