from fastapi import APIRouter
from fastapi.params import Depends

from src.modules.catalogo.app.sections import GetSecciones, CreateSeccion, UpdateSeccion, DeleteSeccion
from src.modules.catalogo.presentation.section.seccion_dependencies import (
    get_all_secciones,
    create_seccion,
    update_seccion,
    delete_seccion
)
from src.modules.catalogo.presentation.section.seccion_dto import SeccionDto, SeccionCreate, SeccionUpdate

router = APIRouter()


@router.get("", response_model=list[SeccionDto])
def list_secciones(
        uc: GetSecciones = Depends(get_all_secciones)
):
    return uc.execute()


@router.post("", response_model=SeccionDto)
def create(
        dto: SeccionCreate,
        uc: CreateSeccion = Depends(create_seccion)
):
    return uc.execute(dto)


@router.put("/{seccion_id}", response_model=SeccionDto)
def update(
        seccion_id: int,
        dto: SeccionUpdate,
        uc: UpdateSeccion = Depends(update_seccion)
):
    return uc.execute(seccion_id, dto)


@router.delete("/{seccion_id}", status_code=204)
def delete(
        seccion_id: int,
        uc: DeleteSeccion = Depends(delete_seccion)
):
    return uc.execute(seccion_id)
