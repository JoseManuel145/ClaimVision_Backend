from fastapi import APIRouter, Depends, Query, status
from typing import List
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.aseguradora.presentation.clientes.cliente_dto import ClienteResponseDTO, ClienteCreateDTO
from src.modules.aseguradora.presentation.clientes.cliente_dependencies import (
    list_clientes_service,
    get_cliente_service,
    create_cliente_service
)

router = APIRouter()

def get_aseguradora_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol != "Operador_Aseguradora" or not user.aseguradora_id:
        pass
    return user

@router.get("", response_model=List[ClienteResponseDTO])
def list_clientes(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(list_clientes_service)
):
    items, total = uc.execute(user.aseguradora_id, offset, limit)
    return items

@router.post("", status_code=status.HTTP_201_CREATED)
def create_cliente(
    dto: ClienteCreateDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(create_cliente_service)
):
    uc.execute(user.aseguradora_id, dto)
    return {"message": "Cliente creado exitosamente"}

@router.get("/{id}", response_model=ClienteResponseDTO)
def get_cliente(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(get_cliente_service)
):
    return uc.execute(id)
