from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.presentation.ajustadores.ajustador_dto import (
    AjustadorCreateDTO,
    AjustadorUpdateDTO,
    AjustadorResponseDTO,
)
from src.modules.aseguradora.application.ajustadores.create_ajustador import CreateAjustador
from src.modules.aseguradora.application.ajustadores.list_ajustadores import ListAjustadores
from src.modules.aseguradora.application.ajustadores.get_ajustador import GetAjustador
from src.modules.aseguradora.application.ajustadores.update_ajustador import UpdateAjustador
from src.modules.aseguradora.application.ajustadores.delete_ajustador import DeleteAjustador
from src.modules.aseguradora.presentation.ajustadores import ajustador_dependencies
from src.shared.domain.models import AccionAudit

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"


@router.post("", response_model=AjustadorResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_ajustador(
    dto: AjustadorCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: CreateAjustador = Depends(ajustador_dependencies.create_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(user.aseguradora_id, dto)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.CREAR_AJUSTADOR,
        usuario=user, request=request,
        metadata={"ajustador_id": resultado.id},
    )
    return resultado


@router.get("", response_model=Page[AjustadorResponseDTO])
def listar_ajustadores(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    activo_para_servicio: bool | None = Query(None),
    user: AuthenticatedUser = Depends(get_operador),
    uc: ListAjustadores = Depends(ajustador_dependencies.list_ajustadores_service),
):
    items, total = uc.execute(user.aseguradora_id, offset_from_page(page, page_size), page_size, activo_para_servicio)
    data = [AjustadorResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/{id}", response_model=AjustadorResponseDTO)
def obtener_ajustador(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetAjustador = Depends(ajustador_dependencies.get_ajustador_service),
):
    return uc.execute(id)


@router.put("/{id}", response_model=AjustadorResponseDTO)
def actualizar_ajustador(
    id: str,
    dto: AjustadorUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: UpdateAjustador = Depends(ajustador_dependencies.update_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(id, dto.cedula_profesional, dto.activo_para_servicio)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_AJUSTADOR,
        usuario=user, request=request,
        metadata={"ajustador_id": id},
    )
    return resultado


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ajustador(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: DeleteAjustador = Depends(ajustador_dependencies.delete_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    uc.execute(id)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.ELIMINAR_AJUSTADOR,
        usuario=user, request=request,
        metadata={"ajustador_id": id},
    )
