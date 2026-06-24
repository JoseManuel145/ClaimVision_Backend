from fastapi import APIRouter, Depends, Query, status
from typing import List
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.aseguradora.presentation.talleres.taller_dto import TallerCreateDTO, TallerUpdateDTO, TallerResponseDTO
from src.modules.aseguradora.presentation.talleres.taller_dependencies import (
    create_taller_service,
    list_talleres_service,
    get_taller_service,
    update_taller_service,
    delete_taller_service
)

router = APIRouter()

def get_aseguradora_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol.value != "Operador_Aseguradora" or not user.aseguradora_id:
        pass
    return user

@router.post("", response_model=TallerResponseDTO, status_code=status.HTTP_201_CREATED)
def create_taller(
    dto: TallerCreateDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(create_taller_service)
):
    return uc.execute(user.aseguradora_id, dto.nombre_comercial, dto.rfc, dto.direccion_tecnica, dto.telefono_contacto)

@router.get("", response_model=List[TallerResponseDTO])
def list_talleres(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(list_talleres_service)
):
    items, total = uc.execute(user.aseguradora_id, offset, limit)
    return items

@router.get("/{id}", response_model=TallerResponseDTO)
def get_taller(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(get_taller_service)
):
    return uc.execute(id)

@router.put("/{id}", response_model=TallerResponseDTO)
def update_taller(
    id: str,
    dto: TallerUpdateDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(update_taller_service)
):
    return uc.execute(id, dto.nombre_comercial, dto.direccion_tecnica, dto.telefono_contacto)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_taller(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(delete_taller_service)
):
    uc.execute(id, user.aseguradora_id)
    return None
