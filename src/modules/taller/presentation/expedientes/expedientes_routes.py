from fastapi import APIRouter, Depends, status
from typing import List, Optional
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.taller.presentation.taller_dto import ExpedienteTecnicoResponseDTO, SiniestroTecnicoDTO, MessageResponseDTO
from src.modules.taller.presentation.taller_dependencies import (
    list_expedientes_taller_service,
    get_expediente_taller_service,
    concluir_expediente_service
)
from src.shared.domain.models import Rol

router = APIRouter(prefix="/expedientes", tags=["Taller - Expedientes"])

def check_operador_taller(user: AuthenticatedUser = Depends(get_current_user)):
    if user.rol != Rol.TALLER.value:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Acceso denegado. Rol requerido: Operador_Taller.")
    return user

@router.get("", response_model=List[SiniestroTecnicoDTO], status_code=status.HTTP_200_OK)
def list_expedientes(
    offset: int = 0,
    limit: int = 20,
    estatus: Optional[str] = None,
    user=Depends(check_operador_taller),
    uc=Depends(list_expedientes_taller_service)
):
    siniestros, _ = uc.execute(usuario_id=user.usuario_id, offset=offset, limit=limit, estatus=estatus)
    return siniestros

@router.get("/{id}", response_model=ExpedienteTecnicoResponseDTO, status_code=status.HTTP_200_OK)
def get_expediente(
    id: str,
    user=Depends(check_operador_taller),
    uc=Depends(get_expediente_taller_service)
):
    return uc.execute(siniestro_id=id, usuario_id=user.usuario_id)

@router.post("/{id}/concluir", response_model=MessageResponseDTO, status_code=status.HTTP_200_OK)
def concluir_expediente(
    id: str,
    user=Depends(check_operador_taller),
    uc=Depends(concluir_expediente_service)
):
    uc.execute(siniestro_id=id, usuario_id=user.usuario_id)
    return MessageResponseDTO(message="Trabajo concluido exitosamente.")
