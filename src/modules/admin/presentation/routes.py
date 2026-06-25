from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.security import get_current_user
from src.modules.admin.presentation.schemas import (
    AseguradoraRequestDTO,
    AseguradoraResponseDTO,
    UpdateSuscripcionDTO,
    UpdateAseguradoraDTO,
    AuditResponse,
    PaginatedResponse,
    MAX_PAGE_SIZE,
    OperadorAseguradoraRequestDTO
)

from src.modules.admin.presentation.dependencies import (
    registrar_aseguradora_service,
    list_aseguradoras_service,
    actualizar_suscripcion_service,
    actualizar_aseguradora_service,
    get_aseguradora_by_id_service,
    desincorporar_aseguradora_service,
    aplicar_bloqueo_arco_service,
    verificar_aseguradora_service,
    consultar_auditoria_service,
    crear_operador_aseguradora_service
)

from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.actualizar_aseguradora import ActualizarAseguradoraUseCase
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.aplicar_bloqueo_arco import AplicarBloqueoArcoUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.consultar_auditoria import ConsultarAuditoriaUseCase
from src.modules.admin.application.crear_operador_aseguradora import CrearOperadorAseguradoraUseCase

router = APIRouter()

def get_admin_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol != "Administrador_Global":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requiere rol de Administrador Global")
    return user

# ── Aseguradoras CRUD ─────────────────────────────────────────────────

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

@router.post("/aseguradoras/{aseguradora_id}/operadores", status_code=status.HTTP_201_CREATED)
async def crear_operador_aseguradora(
    aseguradora_id: str,
    data: OperadorAseguradoraRequestDTO,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: CrearOperadorAseguradoraUseCase = Depends(crear_operador_aseguradora_service)
):
    try:
        return usecase.execute(user.usuario_id, aseguradora_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/aseguradoras", response_model=PaginatedResponse[AseguradoraResponseDTO])
async def list_aseguradoras(
    page: int = Query(1, ge=1, description="Número de página (inicia en 1)"),
    page_size: int = Query(20, ge=1, le=MAX_PAGE_SIZE, description=f"Registros por página (máx. {MAX_PAGE_SIZE})"),
    include_deleted: bool = Query(False, description="Incluir aseguradoras desincorporadas"),
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ListAseguradoras = Depends(list_aseguradoras_service)
):
    offset = (page - 1) * page_size
    items, total = usecase.execute(offset=offset, limit=page_size, include_deleted=include_deleted)
    return PaginatedResponse.build(items=items, total=total, page=page, page_size=page_size)

@router.get("/aseguradoras/desincorporadas", response_model=PaginatedResponse[AseguradoraResponseDTO])
async def list_aseguradoras_desincorporadas(
    page: int = Query(1, ge=1, description="Número de página (inicia en 1)"),
    page_size: int = Query(20, ge=1, le=MAX_PAGE_SIZE, description=f"Registros por página (máx. {MAX_PAGE_SIZE})"),
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ListAseguradoras = Depends(list_aseguradoras_service)
):
    """Lista únicamente las aseguradoras con deleted_at != null (desincorporadas)."""
    offset = (page - 1) * page_size
    # include_deleted=True trae todas, luego filtramos solo las eliminadas
    # Para ser eficiente, se podría agregar un método dedicado al repositorio,
    # pero reutilizamos include_deleted=True y filtramos en memoria por ahora
    items, total = usecase.execute(offset=offset, limit=page_size, include_deleted=True)
    deleted_items = [item for item in items if item.deleted_at is not None or item.estatus_comercial == "Cancelado"]
    return PaginatedResponse.build(items=deleted_items, total=len(deleted_items), page=page, page_size=page_size)

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

@router.put("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO, status_code=status.HTTP_200_OK)
async def actualizar_aseguradora(
    aseguradora_id: str,
    data: UpdateAseguradoraDTO,
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ActualizarAseguradoraUseCase = Depends(actualizar_aseguradora_service)
):
    try:
        return usecase.execute(user.usuario_id, aseguradora_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

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

# ── Usuarios (ARCO) ──────────────────────────────────────────────────

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

# ── Auditoría ─────────────────────────────────────────────────────────

@router.get("/auditoria/logs", response_model=PaginatedResponse[AuditResponse], status_code=status.HTTP_200_OK)
async def consultar_auditoria(
    page: int = Query(1, ge=1, description="Número de página (inicia en 1)"),
    page_size: int = Query(20, ge=1, le=MAX_PAGE_SIZE, description=f"Registros por página (máx. {MAX_PAGE_SIZE})"),
    user: AuthenticatedUser = Depends(get_admin_user),
    usecase: ConsultarAuditoriaUseCase = Depends(consultar_auditoria_service)
):
    try:
        offset = (page - 1) * page_size
        items, total = usecase.execute(offset=offset, limit=page_size)
        return PaginatedResponse.build(items=items, total=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

