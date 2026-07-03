from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.presentation.clientes.cliente_dto import (
    ClienteCreateDTO,
    ClienteResponseDTO,
)
from src.modules.aseguradora.presentation.clientes import cliente_dependencies

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"


@router.post("", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    dto: ClienteCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(cliente_dependencies.create_cliente_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    cliente = uc.execute(user.aseguradora_id, dto)
    audit.record(
        evento_modulo=EVENTO, accion="crear_cliente",
        usuario=user, request=request,
        metadata={"cliente_id": cliente.id},
    )
    return cliente


@router.get("", response_model=Page[ClienteResponseDTO])
def listar_clientes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(cliente_dependencies.list_clientes_service),
):
    items, total = uc.execute(user.aseguradora_id, offset_from_page(page, page_size), page_size)
    data = [ClienteResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/{id}", response_model=ClienteResponseDTO)
def obtener_cliente(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(cliente_dependencies.get_cliente_service),
):
    return uc.execute(id)
