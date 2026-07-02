from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroResponseDTO
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.v1.taller_v1_schemas import (
    CotizacionV1DTO,
    TallerExpedienteDTO,
    CrearCotizacionRequest,
    EditarCotizacionRequest,
)
from src.modules.taller.presentation.v1 import taller_v1_dependencies as deps

router = APIRouter(prefix="/taller", tags=["v1 · Taller"])

get_taller = require_roles("Operador_Taller")
EVENTO = "taller"


@router.get("/ordenes", response_model=Page[SiniestroResponseDTO])
def listar_ordenes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_taller),
    uc=Depends(deps.list_ordenes_service),
):
    """§6 · Órdenes del taller (Asignado_A_Taller / en proceso)."""
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size, estatus)
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=TallerExpedienteDTO)
def detalle_orden(
    id: str,
    user: AuthenticatedUser = Depends(get_taller),
    uc=Depends(deps.get_orden_service),
):
    """§6 · Expediente técnico (siniestro + peritaje validado + cotización)."""
    exp = uc.execute(siniestro_id=id, usuario_id=user.usuario_id)
    base = SiniestroResponseDTO.model_validate(exp.siniestro)
    return TallerExpedienteDTO(
        **base.model_dump(),
        peritaje=PeritajeResponseDTO.model_validate(exp.peritaje_ajustador) if exp.peritaje_ajustador else None,
        cotizacion=CotizacionV1DTO.model_validate(exp.cotizacion) if exp.cotizacion else None,
    )


@router.post("/siniestros/{id}/cotizacion", response_model=CotizacionV1DTO, status_code=status.HTTP_201_CREATED)
def crear_cotizacion(
    id: str,
    dto: CrearCotizacionRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_taller),
    uc=Depends(deps.crear_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Crea cotización → estatus_cotizacion = Pendiente_Aprobacion."""
    cot = uc.execute(
        usuario_id=user.usuario_id, siniestro_id=id,
        monto_mano_obra=dto.monto_mano_obra, monto_refacciones=dto.monto_refacciones,
        desglose_pdf_url=dto.desglose_pdf_url, monto_total=dto.monto_total,
        observaciones_tecnicas=dto.observaciones_tecnicas,
    )
    audit.record(evento_modulo=EVENTO, accion="crear_cotizacion", usuario=user, request=request,
                 metadata={"siniestro_id": id, "cotizacion_id": cot.id})
    return cot


@router.patch("/cotizaciones/{id}", response_model=CotizacionV1DTO)
def editar_cotizacion(
    id: str,
    dto: EditarCotizacionRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_taller),
    uc=Depends(deps.editar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Edita cotización mientras siga Pendiente_Aprobacion."""
    cot = uc.execute(
        usuario_id=user.usuario_id, cotizacion_id=id,
        monto_mano_obra=dto.monto_mano_obra, monto_refacciones=dto.monto_refacciones,
        monto_total=dto.monto_total, desglose_pdf_url=dto.desglose_pdf_url,
        observaciones_tecnicas=dto.observaciones_tecnicas,
    )
    audit.record(evento_modulo=EVENTO, accion="editar_cotizacion", usuario=user, request=request,
                 metadata={"cotizacion_id": id})
    return cot


@router.post("/siniestros/{id}/concluir-trabajo", status_code=status.HTTP_200_OK)
def concluir_trabajo(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_taller),
    uc=Depends(deps.concluir_trabajo_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · → estatus = Trabajo_Concluido (requiere cotización aprobada)."""
    uc.execute(siniestro_id=id, usuario_id=user.usuario_id)
    audit.record(evento_modulo=EVENTO, accion="concluir_trabajo", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return {"message": "Trabajo concluido exitosamente.", "estatus": "Trabajo_Concluido"}


@router.post("/siniestros/{id}/listo-entrega", response_model=SiniestroResponseDTO, status_code=status.HTTP_200_OK)
def listo_entrega(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_taller),
    uc=Depends(deps.listo_entrega_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · → estatus = Listo_Para_Entrega."""
    siniestro = uc.execute(usuario_id=user.usuario_id, siniestro_id=id)
    audit.record(evento_modulo=EVENTO, accion="listo_entrega", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return siniestro
