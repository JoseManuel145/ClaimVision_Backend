from fastapi import APIRouter, Depends

from src.modules.catalogo.app.categories import GetCategoryById, GetAllCategories, GetAllBySection, CreateCategory, UpdateCategory, DeleteCategory
from src.modules.catalogo.presentation.category.categoria_dependencies import get_all_by_seccion, get_all, get_by_id, create_categoria, update_categoria, delete_categoria
from src.modules.catalogo.presentation.category.categoria_dto import CategoriaDto, CategoriaUpdate, CategoriaCreate

router = APIRouter()

@router.get("", response_model=list[CategoriaDto])
def get_categorias(
        uc: GetAllCategories = Depends(get_all)
):
    return uc.execute()

@router.post("", response_model=CategoriaDto)
def create_categoria(
        dto: CategoriaCreate,
        uc: CreateCategory = Depends(create_categoria)
):
    return uc.execute(dto)

@router.get("/by-seccion/{seccion_id}", response_model=list[CategoriaDto])
def get_categorias_by_seccion(
        seccion_id: int,
        uc: GetAllBySection = Depends(get_all_by_seccion)
):
    return uc.execute(seccion_id)


@router.get("/{categoria_id}", response_model=CategoriaDto)
def get_categoria_by_id(
    categoria_id: int,
    uc: GetCategoryById = Depends(get_by_id)
):
    return uc.execute(categoria_id)

@router.put("/{categoria_id}", response_model=CategoriaDto)
def update_categoria(
    categoria_id: int,
    categoria: CategoriaUpdate,
    uc: UpdateCategory = Depends(update_categoria)
):
    return uc.execute(categoria_id, categoria)

@router.delete("/{categoria_id}", status_code=204)
def delete_categoria(
    categoria_id: int,
    uc: DeleteCategory = Depends(delete_categoria)
):
    uc.execute(categoria_id)
