from fastapi import APIRouter, Depends, Query, Request, status, HTTPException
from uuid import UUID

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.presentation.talleres.taller_dto import (
    TallerCreateDTO,
    TallerUpdateDTO,
    TallerResponseDTO,
    OperadorTallerRequestDTO,
)
from src.modules.aseguradora.application.talleres.create_taller import CreateTaller
from src.modules.aseguradora.application.talleres.list_talleres import ListTalleres
from src.modules.aseguradora.application.talleres.get_taller import GetTaller
from src.modules.aseguradora.application.talleres.update_taller import UpdateTaller
from src.modules.aseguradora.application.talleres.delete_taller import DeleteTaller
from src.modules.aseguradora.application.talleres.create_taller_user import CreateOperadorTallerUseCase
from src.modules.aseguradora.presentation.talleres import taller_dependencies
from src.shared.domain.models import AccionAudit

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"

def _require_aseguradora(user: AuthenticatedUser):
    if not user.aseguradora_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operador no tiene una aseguradora asignada.",
        )
    return user.aseguradora_id


@router.post("", response_model=TallerResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_taller(
    dto: TallerCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: CreateTaller = Depends(taller_dependencies.create_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(_require_aseguradora(user), dto.nombre_comercial, dto.rfc, dto.direccion_tecnica, dto.telefono_contacto)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.CREAR_TALLER,
        usuario=user, request=request,
        metadata={"taller_id": resultado.id},
    )
    return resultado


@router.get("", response_model=Page[TallerResponseDTO])
def listar_talleres(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_operador),
    uc: ListTalleres = Depends(taller_dependencies.list_talleres_service),
):
    items, total = uc.execute(_require_aseguradora(user), offset_from_page(page, page_size), page_size)
    data = [TallerResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/{id}", response_model=TallerResponseDTO)
def obtener_taller(
    id: UUID,
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetTaller = Depends(taller_dependencies.get_taller_service),
):
    return uc.execute(str(id))


@router.put("/{id}", response_model=TallerResponseDTO)
def actualizar_taller(
    id: UUID,
    dto: TallerUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: UpdateTaller = Depends(taller_dependencies.update_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(str(id), dto.nombre_comercial, dto.direccion_tecnica, dto.telefono_contacto)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_TALLER,
        usuario=user, request=request,
        metadata={"taller_id": str(id)},
    )
    return resultado


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_taller(
    id: UUID,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: DeleteTaller = Depends(taller_dependencies.delete_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    uc.execute(str(id), _require_aseguradora(user))
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.ELIMINAR_TALLER,
        usuario=user, request=request,
        metadata={"taller_id": str(id)},
    )


@router.post("/{id}/operadores", status_code=status.HTTP_201_CREATED)
def crear_operador_taller(
    id: UUID,
    dto: OperadorTallerRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: CreateOperadorTallerUseCase = Depends(taller_dependencies.crear_operador_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(_require_aseguradora(user), user.usuario_id, str(id), dto)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.CREAR_OPERADOR_TALLER,
        usuario=user, request=request,
        metadata={"taller_id": str(id)},
    )
    return resultado
