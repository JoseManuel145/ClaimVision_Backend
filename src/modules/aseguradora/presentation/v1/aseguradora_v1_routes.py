from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.v1.taller_v1_schemas import CotizacionV1DTO
from src.modules.aseguradora.presentation.siniestros.siniestro_dto import (
    AsignarAjustadorDTO,
    EnviarTallerDTO,
)
from src.modules.aseguradora.presentation.v1.aseguradora_v1_schemas import (
    RechazarCotizacionRequest,
    SiniestroDetalleAseguradoraDTO,
)
from src.modules.aseguradora.presentation.v1 import aseguradora_v1_dependencies as deps
from src.modules.siniestro.presentation.siniestros.siniestro_dependencies import (
    asignar_ajustador_service,
    enviar_taller_service,
)
from src.modules.aseguradora.presentation.v1.aseguradora_v1_dependencies import autorizar_entrega_service

router = APIRouter(prefix="/aseguradora", tags=["v1 · Aseguradora"])

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora"


# ── Bandeja de siniestros ──────────────────────────────────────────────
@router.get("/siniestros", response_model=Page[SiniestroResponseDTO])
def listar_siniestros(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    ajustador_id: str | None = Query(None),
    taller_id: str | None = Query(None),
    q: str | None = Query(None, description="Búsqueda por placas/marca/modelo"),
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(deps.list_siniestros_service),
):
    """§3 · Bandeja de siniestros del tenant (filtros + búsqueda + paginación)."""
    items, total = uc.execute(
        user.aseguradora_id, offset_from_page(page, page_size), page_size,
        estatus, ajustador_id, taller_id, q,
    )
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleAseguradoraDTO)
def detalle_siniestro(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(deps.get_siniestro_service),
):
    """§3 · Detalle completo (siniestro + imágenes + peritaje + cotización)."""
    siniestro, imagenes, peritaje, cotizacion = uc.execute(id, user.aseguradora_id)
    base = SiniestroResponseDTO.model_validate(siniestro)
    return SiniestroDetalleAseguradoraDTO(
        **base.model_dump(),
        imagenes=[ImagenSiniestroResponseDTO.model_validate(i) for i in imagenes],
        peritaje=PeritajeResponseDTO.model_validate(peritaje) if peritaje else None,
        cotizacion=CotizacionV1DTO.model_validate(cotizacion) if cotizacion else None,
        peritaje_ia=None,
    )


# ── Acciones de flujo (realineadas a /api/v1) ──────────────────────────
@router.post("/siniestros/{id}/asignar-ajustador", response_model=SiniestroResponseDTO)
def asignar_ajustador(
    id: str,
    dto: AsignarAjustadorDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(asignar_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · → estatus = Asignado_A_Ajustador."""
    siniestro = uc.execute(id, dto.ajustador_id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="asignar_ajustador", usuario=user, request=request,
                 metadata={"siniestro_id": id, "ajustador_id": dto.ajustador_id})
    return siniestro


@router.post("/siniestros/{id}/enviar-taller", response_model=SiniestroResponseDTO)
def enviar_taller(
    id: str,
    dto: EnviarTallerDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(enviar_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · → estatus = Asignado_A_Taller."""
    siniestro = uc.execute(id, dto.taller_id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="enviar_taller", usuario=user, request=request,
                 metadata={"siniestro_id": id, "taller_id": dto.taller_id})
    return siniestro


@router.post("/siniestros/{id}/autorizar-entrega", response_model=SiniestroResponseDTO)
def autorizar_entrega(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(autorizar_entrega_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · → estatus = Entregado."""
    siniestro = uc.execute(id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="autorizar_entrega", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return siniestro


# ── Decisión de cotizaciones ───────────────────────────────────────────
@router.post("/cotizaciones/{id}/aprobar", response_model=CotizacionV1DTO)
def aprobar_cotizacion(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(deps.aprobar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · estatus_cotizacion = Aprobada."""
    cot = uc.execute(id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="aprobar_cotizacion", usuario=user, request=request,
                 metadata={"cotizacion_id": id})
    return cot


@router.post("/cotizaciones/{id}/rechazar", response_model=CotizacionV1DTO)
def rechazar_cotizacion(
    id: str,
    dto: RechazarCotizacionRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc=Depends(deps.rechazar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§3 · estatus_cotizacion = Rechazada (motivo se guarda en auditoría)."""
    cot = uc.execute(id, user.aseguradora_id, dto.motivo)
    audit.record(evento_modulo=EVENTO, accion="rechazar_cotizacion", usuario=user, request=request,
                 metadata={"cotizacion_id": id, "motivo": dto.motivo})
    return cot
