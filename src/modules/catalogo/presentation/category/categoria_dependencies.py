from fastapi import Depends
from src.core.database import get_session

from src.modules.catalogo.app.categories import (
    GetAllCategories,
    GetAllBySection,
    GetCategoryById,
    CreateCategory,
    UpdateCategory,
    DeleteCategory
)
from src.modules.catalogo.infra.category.category_repository import CategoriaRepository


def get_all_by_seccion(session=Depends(get_session)):
    repo = CategoriaRepository(session)
    return GetAllBySection(repo)


def get_all(session=Depends(get_session)):
    repo = CategoriaRepository(session)
    return GetAllCategories(repo)


def get_by_id(session=Depends(get_session)):
    repo = CategoriaRepository(session)
    return GetCategoryById(repo)


def create_categoria(session=Depends(get_session)):
    repo = CategoriaRepository(session)
    return CreateCategory(repo)


def update_categoria(session=Depends(get_session)):
    repo = CategoriaRepository(session)
    return UpdateCategory(repo)


def delete_categoria(session=Depends(get_session)):
    repo = CategoriaRepository(session)
    return DeleteCategory(repo)
