from fastapi import APIRouter, Depends, Query, status
from typing import List
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.siniestro.presentation.schemas import SiniestroResponseDTO
from src.modules.aseguradora.presentation.siniestros.siniestro_dto import AsignarAjustadorDTO, EnviarTallerDTO
from src.modules.siniestro.presentation.dependencies import (
    list_siniestros_service,
    asignar_ajustador_service,
    enviar_taller_service,
    autorizar_entrega_service
)

router = APIRouter()

def get_aseguradora_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol != "Operador_Aseguradora" or not user.aseguradora_id:
        pass
    return user

@router.get("", response_model=List[SiniestroResponseDTO])
def list_siniestros(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None, description="Filtrar por estatus"),
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(list_siniestros_service)
):
    items, total = uc.execute(user.aseguradora_id, offset, limit, estatus)
    return items

# @router.get("/stream")
# async def siniestros_stream(user: AuthenticatedUser = Depends(get_aseguradora_user)):
#     # Placeholder para Server-Sent Events o WebSockets
#     return {"message": "Stream endpoint (SSE/WebSockets) will be implemented here."}

@router.post("/{id}/asignar-ajustador", response_model=SiniestroResponseDTO)
def asignar_ajustador(
    id: str,
    dto: AsignarAjustadorDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(asignar_ajustador_service)
):
    return uc.execute(id, dto.ajustador_id, user.aseguradora_id)

@router.post("/{id}/enviar-taller", response_model=SiniestroResponseDTO)
def enviar_taller(
    id: str,
    dto: EnviarTallerDTO,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(enviar_taller_service)
):
    return uc.execute(id, dto.taller_id, user.aseguradora_id)

@router.post("/{id}/autorizar-entrega", response_model=SiniestroResponseDTO)
def autorizar_entrega(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(autorizar_entrega_service)
):
    return uc.execute(id, user.aseguradora_id)
