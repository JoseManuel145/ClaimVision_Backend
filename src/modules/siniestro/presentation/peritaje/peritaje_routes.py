from fastapi import APIRouter, Depends, Query, status, HTTPException
from typing import List
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroResponseDTO
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeUpsertRequestDTO, PeritajeResponseDTO
from src.modules.siniestro.presentation.peritaje.peritaje_dependencies import (
    list_asignados_service,
    guardar_peritaje_service,
    confirmar_peritaje_service
)
from src.modules.siniestro.application.peritaje.list_asignados import ListSiniestrosAsignados
from src.modules.siniestro.application.peritaje.guardar_peritaje import GuardarPeritaje
from src.modules.siniestro.application.peritaje.confirmar_peritaje import ConfirmarPeritaje

router = APIRouter(tags=["Peritaje"])

def get_ajustador_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol != "Ajustador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado. Requiere rol de Ajustador.")
    return user

@router.get("/asignados", response_model=List[SiniestroResponseDTO])
async def list_siniestros_asignados(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_ajustador_user),
    uc: ListSiniestrosAsignados = Depends(list_asignados_service)
):
    try:
        items, total = await uc.execute(user.usuario_id, offset, limit, estatus)
        return items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}/peritaje", response_model=PeritajeResponseDTO)
async def guardar_peritaje(
    id: str,
    dto: PeritajeUpsertRequestDTO,
    user: AuthenticatedUser = Depends(get_ajustador_user),
    uc: GuardarPeritaje = Depends(guardar_peritaje_service)
):
    try:
        danos_data = [d.model_dump() for d in dto.danos]
        peritaje = await uc.execute(
            ajustador_id=user.usuario_id,
            siniestro_id=id,
            costo_definitivo=dto.costo_definitivo_ajustador,
            firma=dto.firma_digital_ajustador,
            observaciones=dto.observaciones_campo,
            danos_data=danos_data
        )
        return peritaje
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.post("/{id}/confirmar", response_model=SiniestroResponseDTO)
async def confirmar_peritaje(
    id: str,
    user: AuthenticatedUser = Depends(get_ajustador_user),
    uc: ConfirmarPeritaje = Depends(confirmar_peritaje_service)
):
    try:
        siniestro = await uc.execute(user.usuario_id, id)
        return siniestro
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
