from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.database import get_session
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    SiniestroUpdateDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.taller_v1_schemas import CotizacionV1DTO
from src.modules.aseguradora.presentation.siniestros.siniestro_dto import (
    AsignarAjustadorDTO,
    EnviarTallerDTO,
    RechazarCotizacionRequest,
    SiniestroDetalleAseguradoraDTO,
)
from src.modules.aseguradora.application.siniestros.list_siniestros_aseguradora import ListSiniestrosAseguradora
from src.modules.aseguradora.application.siniestros.get_siniestro_aseguradora import GetSiniestroAseguradora
from src.modules.aseguradora.application.siniestros.autorizar_entrega_v1 import AutorizarEntregaV1
from src.modules.aseguradora.application.cotizaciones.aprobar_cotizacion import AprobarCotizacion
from src.modules.aseguradora.application.cotizaciones.rechazar_cotizacion import RechazarCotizacion
from src.modules.aseguradora.presentation.siniestros import siniestro_dependencies as deps
from src.modules.siniestro.application.siniestros.asignar_ajustador import AsignarAjustador
from src.modules.siniestro.application.siniestros.editar_siniestro import EditarSiniestro
from src.modules.siniestro.application.siniestros.enviar_taller import EnviarTaller
from src.modules.siniestro.presentation.siniestros.siniestro_dependencies import (
    asignar_ajustador_service,
    editar_siniestro_service,
    enviar_taller_service,
)
from src.shared.infra.storage.url_resolver import resolve_storage_url
from src.shared.infra.events.sse_manager import sse_manager
from src.core.supabase import get_supabase_client
from src.shared.domain.models import AccionAudit

router = APIRouter()


get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora"


@router.get("/siniestros", response_model=Page[SiniestroResponseDTO])
def listar_siniestros(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    ajustador_id: str | None = Query(None),
    taller_id: str | None = Query(None),
    q: str | None = Query(None, description="Búsqueda por placas/marca/modelo"),
    user: AuthenticatedUser = Depends(get_operador),
    uc: ListSiniestrosAseguradora = Depends(deps.list_siniestros_service),
):
    items, total = uc.execute(
        user.aseguradora_id, offset_from_page(page, page_size), page_size,
        estatus, ajustador_id, taller_id, q,
    )
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleAseguradoraDTO)
def detalle_siniestro(
    id: UUID,
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetSiniestroAseguradora = Depends(deps.get_siniestro_service),
    db: Session = Depends(get_session),
    client=Depends(get_supabase_client),
):
    siniestro, imagenes, peritaje, cotizacion = uc.execute(str(id), user.aseguradora_id)

    from src.modules.aseguradora.infra.db.repositories.cliente_repository import ClienteRepository
    from src.modules.aseguradora.infra.db.repositories.ajustador_repository import AjustadorRepository
    from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository

    def _resolver_nombre(repo, entity_id, attr="nombre"):
        try:
            entity = repo.get_by_id(entity_id)
            return getattr(entity, attr, None) if entity else None
        except Exception:
            return None

    cliente_nombre = _resolver_nombre(ClienteRepository(db), siniestro.cliente_id) if siniestro.cliente_id else None
    ajustador_nombre = _resolver_nombre(AjustadorRepository(db), siniestro.ajustador_id) if siniestro.ajustador_id else None
    taller_nombre = (
        _resolver_nombre(TallerRepository(db), siniestro.taller_id, "nombre_comercial")
        if siniestro.taller_id else None
    )

    base = SiniestroResponseDTO.model_validate(siniestro)

    imagenes_dtos = [
        ImagenSiniestroResponseDTO.model_validate(i)
        .model_copy(update={"imagen_url": resolve_storage_url(client, i.imagen_url)})
        for i in imagenes
    ]

    cotizacion_dto = None
    if cotizacion:
        cotizacion_dto = CotizacionV1DTO.model_validate(cotizacion)
        cotizacion_dto = cotizacion_dto.model_copy(
            update={"desglose_pdf_url": resolve_storage_url(client, cotizacion.desglose_pdf_url)}
        )

    return SiniestroDetalleAseguradoraDTO(
        **base.model_dump(),
        imagenes=imagenes_dtos,
        peritaje=PeritajeResponseDTO.model_validate(peritaje) if peritaje else None,
        cotizacion=cotizacion_dto,
        peritaje_ia=None,
        cliente_nombre=cliente_nombre,
        ajustador_nombre=ajustador_nombre,
        taller_nombre=taller_nombre,
    )


@router.put("/siniestros/{id}", response_model=SiniestroResponseDTO)
def editar_siniestro(
    id: UUID,
    dto: SiniestroUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: EditarSiniestro = Depends(editar_siniestro_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(siniestro_id=str(id), usuario_id=user.usuario_id, rol=user.rol, dto=dto)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.EDITAR_SINIESTRO, usuario=user, request=request,
                 metadata={"siniestro_id": str(id)})
    sse_manager.publish_event_sync(
        event="siniestro_updated",
        data={"entity": "siniestro", "action": "UPDATE", "siniestro_id": str(id)},
        target_aseguradora_id=user.aseguradora_id,
    )
    return siniestro


@router.post("/siniestros/{id}/asignar-ajustador", response_model=SiniestroResponseDTO)
def asignar_ajustador(
    id: UUID,
    dto: AsignarAjustadorDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: AsignarAjustador = Depends(asignar_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(str(id), dto.ajustador_id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.ASIGNAR_AJUSTADOR, usuario=user, request=request,
                 metadata={"siniestro_id": str(id), "ajustador_id": dto.ajustador_id})
    sse_manager.publish_event_sync(
        event="siniestro_updated",
        data={"entity": "siniestro", "action": "ASIGNAR_AJUSTADOR", "siniestro_id": str(id), "ajustador_id": dto.ajustador_id},
        target_aseguradora_id=user.aseguradora_id,
    )
    return siniestro


@router.post("/siniestros/{id}/enviar-taller", response_model=SiniestroResponseDTO)
def enviar_taller(
    id: UUID,
    dto: EnviarTallerDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: EnviarTaller = Depends(enviar_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(str(id), dto.taller_id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.ENVIAR_TALLER, usuario=user, request=request,
                 metadata={"siniestro_id": str(id), "taller_id": dto.taller_id})
    sse_manager.publish_event_sync(
        event="siniestro_updated",
        data={"entity": "siniestro", "action": "ENVIAR_TALLER", "siniestro_id": str(id), "taller_id": dto.taller_id},
        target_aseguradora_id=user.aseguradora_id,
    )
    return siniestro


@router.post("/siniestros/{id}/autorizar-entrega", response_model=SiniestroResponseDTO)
def autorizar_entrega(
    id: UUID,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: AutorizarEntregaV1 = Depends(deps.autorizar_entrega_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(str(id), user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.AUTORIZAR_ENTREGA, usuario=user, request=request,
                 metadata={"siniestro_id": str(id)})
    sse_manager.publish_event_sync(
        event="siniestro_updated",
        data={"entity": "siniestro", "action": "AUTORIZAR_ENTREGA", "siniestro_id": str(id)},
        target_aseguradora_id=user.aseguradora_id,
    )
    return siniestro


@router.post("/cotizaciones/{id}/aprobar", response_model=CotizacionV1DTO)
def aprobar_cotizacion(
    id: UUID,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: AprobarCotizacion = Depends(deps.aprobar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
    client=Depends(get_supabase_client),
):
    cot = uc.execute(str(id), user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.APROBAR_COTIZACION, usuario=user, request=request,
                 metadata={"cotizacion_id": str(id)})
    sse_manager.publish_event_sync(
        event="cotizacion_updated",
        data={"entity": "cotizacion", "action": "APROBAR", "cotizacion_id": str(id)},
        target_aseguradora_id=user.aseguradora_id,
    )
    dto = CotizacionV1DTO.model_validate(cot)
    dto = dto.model_copy(update={"desglose_pdf_url": resolve_storage_url(client, cot.desglose_pdf_url)})
    return dto


@router.post("/cotizaciones/{id}/rechazar", response_model=CotizacionV1DTO)
def rechazar_cotizacion(
    id: UUID,
    dto: RechazarCotizacionRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: RechazarCotizacion = Depends(deps.rechazar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
    client=Depends(get_supabase_client),
):
    cot = uc.execute(str(id), user.aseguradora_id, dto.motivo)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.RECHAZAR_COTIZACION, usuario=user, request=request,
                 metadata={"cotizacion_id": str(id), "motivo": dto.motivo})
    sse_manager.publish_event_sync(
        event="cotizacion_updated",
        data={"entity": "cotizacion", "action": "RECHAZAR", "cotizacion_id": str(id)},
        target_aseguradora_id=user.aseguradora_id,
    )
    dto_resp = CotizacionV1DTO.model_validate(cot)
    dto_resp = dto_resp.model_copy(update={"desglose_pdf_url": resolve_storage_url(client, cot.desglose_pdf_url)})
    return dto_resp

