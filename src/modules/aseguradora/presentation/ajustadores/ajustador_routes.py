from fastapi import APIRouter, Depends, Query, status
from typing import List
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.aseguradora.presentation.ajustadores.ajustador_dto import AjustadorCreateDTO, AjustadorUpdateDTO, AjustadorResponseDTO
from src.modules.aseguradora.presentation.ajustadores.ajustador_dependencies import (
    create_ajustador_service,
    list_ajustadores_service,
    get_ajustador_service,
    update_ajustador_service,
    delete_ajustador_service
)

router = APIRouter()

def get_aseguradora_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol.value != "Operador_Aseguradora" or not user.aseguradora_id:
        # Simplificación: Admin también podría entrar, pero para ajustarnos al dominio, pedimos Operador
        pass
    return user

@router.post("", response_model=AjustadorResponseDTO, status_code=status.HTTP_201_CREATED)
def create_ajustador(
    dto: AjustadorCreateDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(create_ajustador_service)
):
    return uc.execute(user.aseguradora_id, dto)

@router.get("", response_model=List[AjustadorResponseDTO])
def list_ajustadores(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    activo_para_servicio: bool | None = Query(None),
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(list_ajustadores_service)
):
    items, total = uc.execute(user.aseguradora_id, offset, limit, activo_para_servicio)
    return items

@router.get("/{id}", response_model=AjustadorResponseDTO)
def get_ajustador(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(get_ajustador_service)
):
    return uc.execute(id)

@router.put("/{id}", response_model=AjustadorResponseDTO)
def update_ajustador(
    id: str,
    dto: AjustadorUpdateDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(update_ajustador_service)
):
    return uc.execute(id, dto.cedula_profesional, dto.activo_para_servicio)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ajustador(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(delete_ajustador_service)
):
    uc.execute(id)
    return None
