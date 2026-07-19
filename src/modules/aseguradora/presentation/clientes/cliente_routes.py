from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.presentation.clientes.cliente_dto import (
    ClienteCreateDTO,
    ClienteResponseDTO,
    ClienteUpdateDTO,
)
from src.modules.aseguradora.application.clientes.create_cliente import CreateClienteByAseguradora
from src.modules.aseguradora.application.clientes.list_clientes import ListClientes
from src.modules.aseguradora.application.clientes.get_cliente import GetCliente
from src.modules.aseguradora.application.clientes.update_cliente import UpdateCliente
from src.modules.aseguradora.presentation.clientes import cliente_dependencies
from src.shared.infra.events.sse_manager import sse_manager
from src.shared.domain.models import AccionAudit

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"


@router.post("", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    dto: ClienteCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: CreateClienteByAseguradora = Depends(cliente_dependencies.create_cliente_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    cliente = uc.execute(user.aseguradora_id, dto)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.CREAR_CLIENTE,
        usuario=user, request=request,
        metadata={"cliente_id": cliente.id},
    )
    sse_manager.publish_event_sync(
        event="cliente_created",
        data={"entity": "cliente", "action": "CREATE", "cliente_id": cliente.id},
        target_aseguradora_id=user.aseguradora_id,
    )
    return cliente


@router.get("", response_model=Page[ClienteResponseDTO])
def listar_clientes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_operador),
    uc: ListClientes = Depends(cliente_dependencies.list_clientes_service),
):
    items, total = uc.execute(user.aseguradora_id, offset_from_page(page, page_size), page_size)
    data = [ClienteResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/{id}", response_model=ClienteResponseDTO)
def obtener_cliente(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetCliente = Depends(cliente_dependencies.get_cliente_service),
):
    return uc.execute(id)


@router.put("/{id}", response_model=ClienteResponseDTO)
def actualizar_cliente(
    id: str,
    dto: ClienteUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: UpdateCliente = Depends(cliente_dependencies.update_cliente_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    cliente = uc.execute(id, dto)
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_CLIENTE,
        usuario=user, request=request,
        metadata={"cliente_id": id},
    )
    sse_manager.publish_event_sync(
        event="cliente_updated",
        data={"entity": "cliente", "action": "UPDATE", "cliente_id": id},
        target_aseguradora_id=user.aseguradora_id,
    )
    return cliente

