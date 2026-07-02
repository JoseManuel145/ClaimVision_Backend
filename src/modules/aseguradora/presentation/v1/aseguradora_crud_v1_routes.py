from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.presentation.ajustadores.ajustador_dto import (
    AjustadorCreateDTO,
    AjustadorUpdateDTO,
    AjustadorResponseDTO,
)
from src.modules.aseguradora.presentation.ajustadores import ajustador_dependencies as ajustadores
from src.modules.aseguradora.presentation.clientes.cliente_dto import (
    ClienteCreateDTO,
    ClienteResponseDTO,
)
from src.modules.aseguradora.presentation.clientes import cliente_dependencies as clientes
from src.modules.aseguradora.presentation.talleres.taller_dto import (
    TallerCreateDTO,
    TallerUpdateDTO,
    TallerResponseDTO,
    OperadorTallerRequestDTO,
)
from src.modules.aseguradora.presentation.talleres import taller_dependencies as talleres
from src.modules.aseguradora.presentation.usuarios import usuario_dependencies as usuarios

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"


# ── Ajustadores ────────────────────────────────────────────────────────

@router.post("/ajustadores", response_model=AjustadorResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_ajustador(
    dto: AjustadorCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(ajustadores.create_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Crear un ajustador en la aseguradora."""
    resultado = uc.execute(user.aseguradora_id, dto)
    audit.record(
        evento_modulo=EVENTO, accion="crear_ajustador",
        usuario=user, request=request,
        metadata={"ajustador_id": resultado.id},
    )
    return resultado


@router.get("/ajustadores", response_model=Page[AjustadorResponseDTO])
def listar_ajustadores(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    activo_para_servicio: bool | None = Query(None),
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(ajustadores.list_ajustadores_service),
):
    """§3 · Listar ajustadores del tenant (paginado)."""
    items, total = uc.execute(user.aseguradora_id, offset_from_page(page, page_size), page_size, activo_para_servicio)
    data = [AjustadorResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/ajustadores/{id}", response_model=AjustadorResponseDTO)
def obtener_ajustador(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(ajustadores.get_ajustador_service),
):
    """§3 · Obtener detalle de un ajustador."""
    return uc.execute(id)


@router.put("/ajustadores/{id}", response_model=AjustadorResponseDTO)
def actualizar_ajustador(
    id: str,
    dto: AjustadorUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(ajustadores.update_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Actualizar datos de un ajustador."""
    resultado = uc.execute(id, dto.cedula_profesional, dto.activo_para_servicio)
    audit.record(
        evento_modulo=EVENTO, accion="actualizar_ajustador",
        usuario=user, request=request,
        metadata={"ajustador_id": id},
    )
    return resultado


@router.delete("/ajustadores/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ajustador(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(ajustadores.delete_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Eliminar un ajustador."""
    uc.execute(id)
    audit.record(
        evento_modulo=EVENTO, accion="eliminar_ajustador",
        usuario=user, request=request,
        metadata={"ajustador_id": id},
    )


# ── Clientes ───────────────────────────────────────────────────────────

@router.post("/clientes", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    dto: ClienteCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(clientes.create_cliente_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Crear un cliente (usuario + perfil) en la aseguradora."""
    cliente = uc.execute(user.aseguradora_id, dto)
    audit.record(
        evento_modulo=EVENTO, accion="crear_cliente",
        usuario=user, request=request,
        metadata={"cliente_id": cliente.id},
    )
    return cliente


@router.get("/clientes", response_model=Page[ClienteResponseDTO])
def listar_clientes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(clientes.list_clientes_service),
):
    """§3 · Listar clientes del tenant (paginado)."""
    items, total = uc.execute(user.aseguradora_id, offset_from_page(page, page_size), page_size)
    data = [ClienteResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/clientes/{id}", response_model=ClienteResponseDTO)
def obtener_cliente(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(clientes.get_cliente_service),
):
    """§3 · Obtener detalle de un cliente."""
    return uc.execute(id)


# ── Talleres ───────────────────────────────────────────────────────────

@router.post("/talleres", response_model=TallerResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_taller(
    dto: TallerCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(talleres.create_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Registrar un taller en la aseguradora."""
    resultado = uc.execute(user.aseguradora_id, dto.nombre_comercial, dto.rfc, dto.direccion_tecnica, dto.telefono_contacto)
    audit.record(
        evento_modulo=EVENTO, accion="crear_taller",
        usuario=user, request=request,
        metadata={"taller_id": resultado.id},
    )
    return resultado


@router.get("/talleres", response_model=Page[TallerResponseDTO])
def listar_talleres(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(talleres.list_talleres_service),
):
    """§3 · Listar talleres del tenant (paginado)."""
    items, total = uc.execute(user.aseguradora_id, offset_from_page(page, page_size), page_size)
    data = [TallerResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/talleres/{id}", response_model=TallerResponseDTO)
def obtener_taller(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(talleres.get_taller_service),
):
    """§3 · Obtener detalle de un taller."""
    return uc.execute(id)


@router.put("/talleres/{id}", response_model=TallerResponseDTO)
def actualizar_taller(
    id: str,
    dto: TallerUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(talleres.update_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Actualizar datos de un taller."""
    resultado = uc.execute(id, dto.nombre_comercial, dto.direccion_tecnica, dto.telefono_contacto)
    audit.record(
        evento_modulo=EVENTO, accion="actualizar_taller",
        usuario=user, request=request,
        metadata={"taller_id": id},
    )
    return resultado


@router.delete("/talleres/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_taller(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(talleres.delete_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Desvincular taller de la aseguradora."""
    uc.execute(id, user.aseguradora_id)
    audit.record(
        evento_modulo=EVENTO, accion="eliminar_taller",
        usuario=user, request=request,
        metadata={"taller_id": id},
    )


@router.post("/talleres/{id}/operadores", status_code=status.HTTP_201_CREATED)
def crear_operador_taller(
    id: str,
    dto: OperadorTallerRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(talleres.crear_operador_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · Crear un operador para un taller."""
    resultado = uc.execute(user.aseguradora_id, user.usuario_id, id, dto)
    audit.record(
        evento_modulo=EVENTO, accion="crear_operador_taller",
        usuario=user, request=request,
        metadata={"taller_id": id},
    )
    return resultado


# ── Usuarios (ARCO) ──────────────────────────────────────────────────

@router.post("/usuarios/{id}/bloqueo-arco")
def aplicar_bloqueo_arco(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(usuarios.bloqueo_arco_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Aplicar bloqueo ARCO a un usuario del tenant."""
    uc.execute(user.aseguradora_id, id)
    audit.record(
        evento_modulo=EVENTO, accion="bloqueo_arco",
        usuario=user, request=request,
        metadata={"usuario_id": id},
    )
    return {"message": "Bloqueo ARCO aplicado exitosamente"}


@router.post("/usuarios/{id}/desbloqueo-arco")
def aplicar_desbloqueo_arco(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(usuarios.desbloqueo_arco_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Desbloquear ARCO de un usuario del tenant."""
    uc.execute(user.aseguradora_id, id)
    audit.record(
        evento_modulo=EVENTO, accion="desbloqueo_arco",
        usuario=user, request=request,
        metadata={"usuario_id": id},
    )
    return {"message": "Desbloqueo ARCO aplicado exitosamente"}
