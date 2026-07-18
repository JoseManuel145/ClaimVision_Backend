from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile, status
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.logging import get_logger
from src.core.security import require_roles

logger = get_logger("taller.routes")
from src.core.exceptions import NotFoundError, ForbiddenError
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroResponseDTO
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.taller_v1_schemas import (
    CotizacionV1DTO,
    TallerExpedienteDTO,
    TallerPerfilResponse,
    TallerPerfilUpdateRequest,
    CrearCotizacionRequest,
    EditarCotizacionRequest,
)
from src.modules.taller.application.expedientes.list_expedientes import ListExpedientesTallerUseCase
from src.modules.taller.application.expedientes.get_expediente import GetExpedienteTallerUseCase
from src.modules.taller.application.expedientes.concluir_expediente import ConcluirExpedienteUseCase
from src.modules.taller.application.expedientes.marcar_listo_entrega import MarcarListoEntrega
from src.modules.taller.application.crear_cotizacion import CrearCotizacion
from src.modules.taller.application.editar_cotizacion import EditarCotizacion
from src.modules.taller.application.get_perfil_taller import GetPerfilTaller
from src.modules.taller.application.actualizar_perfil_taller import ActualizarPerfilTaller
from src.modules.taller.infra.pdf.supabase_storage_repository import SupabasePdfStorage
from src.modules.taller.presentation import taller_v1_dependencies as deps

router = APIRouter()

get_taller = require_roles("Operador_Taller")
EVENTO = "taller"


@router.get("/perfil", response_model=TallerPerfilResponse)
def get_perfil(
    user: AuthenticatedUser = Depends(get_taller),
    uc: GetPerfilTaller = Depends(deps.get_perfil_taller_service),
):
    """§6 · Perfil del taller (datos del taller + datos del operador)."""
    taller, user_data = uc.execute(user.usuario_id)
    return TallerPerfilResponse(
        id=taller.id,
        nombre_comercial=taller.nombre_comercial,
        rfc=taller.rfc,
        direccion_tecnica=taller.direccion_tecnica,
        telefono_contacto=taller.telefono_contacto,
        nombre=user_data.nombre if user_data else None,
        email=user_data.email if user_data else None,
        telefono=user_data.telefono if user_data else None,
        version=taller.version,
        created_at=taller.created_at,
        updated_at=taller.updated_at,
    )


@router.put("/perfil", response_model=TallerPerfilResponse)
def actualizar_perfil(
    dto: TallerPerfilUpdateRequest,
    user: AuthenticatedUser = Depends(get_taller),
    uc: ActualizarPerfilTaller = Depends(deps.actualizar_perfil_taller_service),
):
    """§6 · Actualiza perfil del taller (datos del taller + datos del operador)."""
    taller, user_data = uc.execute(
        usuario_id=user.usuario_id,
        nombre_comercial=dto.nombre_comercial,
        direccion_tecnica=dto.direccion_tecnica,
        telefono_contacto=dto.telefono_contacto,
        nombre=dto.nombre,
        email=dto.email,
        telefono=dto.telefono,
    )
    return TallerPerfilResponse(
        id=taller.id,
        nombre_comercial=taller.nombre_comercial,
        rfc=taller.rfc,
        direccion_tecnica=taller.direccion_tecnica,
        telefono_contacto=taller.telefono_contacto,
        nombre=user_data.nombre if user_data else None,
        email=user_data.email if user_data else None,
        telefono=user_data.telefono if user_data else None,
        version=taller.version,
        created_at=taller.created_at,
        updated_at=taller.updated_at,
    )


@router.get("/ordenes", response_model=Page[SiniestroResponseDTO])
def listar_ordenes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_taller),
    uc: ListExpedientesTallerUseCase = Depends(deps.list_ordenes_service),
):
    """§6 · Órdenes del taller (Asignado_A_Taller / en proceso)."""
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size, estatus)
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=TallerExpedienteDTO)
def detalle_orden(
    id: str,
    user: AuthenticatedUser = Depends(get_taller),
    uc: GetExpedienteTallerUseCase = Depends(deps.get_orden_service),
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
async def crear_cotizacion(
    id: str,
    monto_mano_obra: float = Form(...),
    monto_refacciones: float = Form(...),
    monto_total: float | None = Form(None),
    observaciones_tecnicas: str | None = Form(None),
    desglose_pdf: UploadFile = File(...),
    request: Request = None,
    user: AuthenticatedUser = Depends(get_taller),
    uc: CrearCotizacion = Depends(deps.crear_cotizacion_service),
    storage: SupabasePdfStorage = Depends(deps.subir_pdf_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Crea cotización → estatus_cotizacion = Pendiente_Aprobacion. Recibe PDF del desglose."""
    logger.info(
        "crear_cotizacion siniestro_id=%s usuario_id=%s filename=%s content_type=%s size=%d",
        id, user.usuario_id, desglose_pdf.filename, desglose_pdf.content_type,
        desglose_pdf.size or 0,
    )
    pdf_bytes = await desglose_pdf.read()
    filename = desglose_pdf.filename or f"cotizacion_{id}.pdf"
    content_type = desglose_pdf.content_type or "application/pdf"
    pdf_url = storage.upload_pdf(pdf_bytes, filename, content_type)
    logger.info("PDF subido exitosamente url=%s", pdf_url)

    cot = uc.execute(
        usuario_id=user.usuario_id, siniestro_id=id,
        monto_mano_obra=monto_mano_obra, monto_refacciones=monto_refacciones,
        desglose_pdf_url=pdf_url, monto_total=monto_total,
        observaciones_tecnicas=observaciones_tecnicas,
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
    uc: EditarCotizacion = Depends(deps.editar_cotizacion_service),
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
    uc: ConcluirExpedienteUseCase = Depends(deps.concluir_trabajo_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · → estatus = Trabajo_Concluido (requiere cotización aprobada)."""
    logger.info("concluir_trabajo siniestro_id=%s usuario_id=%s", id, user.usuario_id)
    uc.execute(siniestro_id=id, usuario_id=user.usuario_id)
    audit.record(evento_modulo=EVENTO, accion="concluir_trabajo", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return {"message": "Trabajo concluido exitosamente.", "estatus": "Trabajo_Concluido"}


@router.post("/siniestros/{id}/listo-entrega", response_model=SiniestroResponseDTO, status_code=status.HTTP_200_OK)
def listo_entrega(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_taller),
    uc: MarcarListoEntrega = Depends(deps.listo_entrega_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · → estatus = Listo_Para_Entrega."""
    siniestro = uc.execute(usuario_id=user.usuario_id, siniestro_id=id)
    audit.record(evento_modulo=EVENTO, accion="listo_entrega", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return siniestro
