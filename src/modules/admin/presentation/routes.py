from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.security import get_current_user
from src.modules.admin.presentation.schemas import AseguradoraRequestDTO, AseguradoraResponseDTO, UpdateSuscripcionDTO

from src.modules.admin.presentation.dependencies import (
    registrar_aseguradora_service,
    list_aseguradoras_service,
    actualizar_suscripcion_service,
    get_aseguradora_by_id_service,
    desincorporar_aseguradora_service,
    aplicar_bloqueo_arco_service,
    verificar_aseguradora_service,
    consultar_auditoria_service
)

from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.aplicar_bloqueo_arco import AplicarBloqueoArcoUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.consultar_auditoria import ConsultarAuditoriaUseCase

router = APIRouter()

def get_admin_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol != "Administrador_Global":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requiere rol de Administrador Global")
    return user

@router.post("/aseguradoras", response_model=AseguradoraResponseDTO, status_code=status.HTTP_201_CREATED)
async def registrar_aseguradora(
    data: AseguradoraRequestDTO,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: RegistrarAseguradoraUseCase = Depends(registrar_aseguradora_service)
):
    try:
        return usecase.execute(user.usuario_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/aseguradoras", response_model=List[AseguradoraResponseDTO])
async def list_aseguradoras(
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ListAseguradoras = Depends(list_aseguradoras_service)
):
    return usecase.execute()

@router.get("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
async def get_aseguradora_by_id(
    aseguradora_id: str,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: GetAseguradoraById = Depends(get_aseguradora_by_id_service)
):
    try:
        return usecase.execute(user.usuario_id, aseguradora_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/aseguradoras/{aseguradora_id}/verificar", response_model=AseguradoraResponseDTO, status_code=status.HTTP_200_OK)
async def verificar_aseguradora(
    aseguradora_id: str,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: VerificarAseguradoraUseCase = Depends(verificar_aseguradora_service)
):
    try:
        return usecase.execute(user.usuario_id, aseguradora_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/aseguradoras/{aseguradora_id}/suscripcion", response_model=AseguradoraResponseDTO, status_code=status.HTTP_200_OK)
async def actualizar_suscripcion(
    aseguradora_id: str,
    data: UpdateSuscripcionDTO,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ActualizarSuscripcionUseCase = Depends(actualizar_suscripcion_service)
):
    try:
        return usecase.execute(user.usuario_id, aseguradora_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO, status_code=status.HTTP_200_OK)
async def desincorporar_aseguradora(
    aseguradora_id: str,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: DesincorporarAseguradoraUseCase = Depends(desincorporar_aseguradora_service)
):
    try:
        return usecase.execute(user.usuario_id, aseguradora_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/usuarios/{usuario_id}/bloqueo-arco", status_code=status.HTTP_200_OK)
async def aplicar_bloqueo_arco(
    usuario_id: str,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: AplicarBloqueoArcoUseCase = Depends(aplicar_bloqueo_arco_service)
):
    try:
        usecase.execute(user.usuario_id, usuario_id)
        return {"message": "Usuario bloqueado y datos cifrados exitosamente por derechos ARCO."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/auditoria/logs", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def consultar_auditoria(
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ConsultarAuditoriaUseCase = Depends(consultar_auditoria_service)
):
    try:
        logs = usecase.execute(user.usuario_id)
        return [{"id": log.id, "accion": log.accion, "entidad_afectada": log.entidad_afectada, "fecha_evento": log.fecha_evento} for log in logs]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
