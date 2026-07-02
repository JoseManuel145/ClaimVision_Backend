from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.admin.presentation.schemas import (
    AseguradoraRequestDTO,
    AseguradoraResponseDTO,
    UpdateSuscripcionDTO,
    UpdateAseguradoraDTO,
    AuditResponse,
    OperadorAseguradoraRequestDTO,
)
from src.modules.admin.presentation import dependencies as deps

router = APIRouter()

get_admin = require_roles("Administrador_Global")

EVENTO = "admin"


# ── Aseguradoras CRUD ──────────────────────────────────────────────────

@router.post("/aseguradoras", response_model=AseguradoraResponseDTO, status_code=status.HTTP_201_CREATED)
def registrar_aseguradora(
    data: AseguradoraRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.registrar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Registrar una nueva aseguradora en la plataforma."""
    resultado = uc.execute(user.usuario_id, data)
    audit.record(
        evento_modulo=EVENTO, accion="registrar_aseguradora",
        usuario=user, request=request,
        metadata={"aseguradora_id": resultado.id},
    )
    return resultado


@router.post("/aseguradoras/{aseguradora_id}/operadores", status_code=status.HTTP_201_CREATED)
def crear_operador_aseguradora(
    aseguradora_id: str,
    data: OperadorAseguradoraRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.crear_operador_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Crear un operador para una aseguradora específica."""
    resultado = uc.execute(user.usuario_id, aseguradora_id, data)
    audit.record(
        evento_modulo=EVENTO, accion="crear_operador",
        usuario=user, request=request,
        metadata={"aseguradora_id": aseguradora_id},
    )
    return resultado


@router.get("/aseguradoras", response_model=Page[AseguradoraResponseDTO])
def listar_aseguradoras(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    include_deleted: bool = Query(False, description="Incluir aseguradoras desincorporadas"),
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.list_aseguradoras_service),
):
    """§5 · Listar aseguradoras registradas (paginado, con filtro de baja)."""
    offset = offset_from_page(page, page_size)
    items, total = uc.execute(offset=offset, limit=page_size, include_deleted=include_deleted)
    data = [AseguradoraResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/aseguradoras/desincorporadas", response_model=Page[AseguradoraResponseDTO])
def listar_aseguradoras_desincorporadas(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.list_aseguradoras_service),
):
    """§5 · Listar únicamente aseguradoras desincorporadas (baja lógica)."""
    offset = offset_from_page(page, page_size)
    items, total = uc.execute(offset=offset, limit=page_size, include_deleted=True)
    deleted = [i for i in items if i.deleted_at is not None or i.estatus_comercial == "Cancelado"]
    data = [AseguradoraResponseDTO.model_validate(i) for i in deleted]
    return Page.build(data=data, total=len(deleted), page=page, page_size=page_size)


@router.get("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
def obtener_aseguradora(
    aseguradora_id: str,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.get_aseguradora_by_id_service),
):
    """§5 · Obtener detalle de una aseguradora por ID."""
    try:
        return uc.execute(user.usuario_id, aseguradora_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
def actualizar_aseguradora(
    aseguradora_id: str,
    data: UpdateAseguradoraDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.actualizar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Actualizar datos de una aseguradora existente."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id, data)
        audit.record(
            evento_modulo=EVENTO, accion="actualizar_aseguradora",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/aseguradoras/{aseguradora_id}/verificar", response_model=AseguradoraResponseDTO)
def verificar_aseguradora(
    aseguradora_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.verificar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Marcar aseguradora como verificada."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id)
        audit.record(
            evento_modulo=EVENTO, accion="verificar_aseguradora",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/aseguradoras/{aseguradora_id}/suscripcion", response_model=AseguradoraResponseDTO)
def actualizar_suscripcion(
    aseguradora_id: str,
    data: UpdateSuscripcionDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.actualizar_suscripcion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Actualizar plan de suscripción de una aseguradora."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id, data)
        audit.record(
            evento_modulo=EVENTO, accion="actualizar_suscripcion",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id, "nuevo_plan": data.nuevo_plan},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
def desincorporar_aseguradora(
    aseguradora_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.desincorporar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Desincorporar (baja lógica) una aseguradora de la plataforma."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id)
        audit.record(
            evento_modulo=EVENTO, accion="desincorporar_aseguradora",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── Usuarios (ARCO) ──────────────────────────────────────────────────

@router.post("/usuarios/{usuario_id}/bloqueo-arco")
def aplicar_bloqueo_arco(
    usuario_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.aplicar_bloqueo_arco_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Aplicar bloqueo ARCO a un usuario (cifra sus datos personales)."""
    try:
        uc.execute(user.usuario_id, usuario_id)
        audit.record(
            evento_modulo=EVENTO, accion="bloqueo_arco",
            usuario=user, request=request,
            metadata={"usuario_id": usuario_id},
        )
        return {"message": "Usuario bloqueado y datos cifrados exitosamente por derechos ARCO."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── Auditoría ─────────────────────────────────────────────────────────

@router.get("/auditoria/logs", response_model=Page[AuditResponse])
def consultar_auditoria(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_admin),
    uc=Depends(deps.consultar_auditoria_service),
):
    """§6 · Consultar logs de auditoría (paginado)."""
    try:
        offset = offset_from_page(page, page_size)
        items, total = uc.execute(offset=offset, limit=page_size)
        data = [AuditResponse.model_validate(i) for i in items]
        return Page.build(data=data, total=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
