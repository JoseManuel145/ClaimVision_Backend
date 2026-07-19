from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.domain.transitions import construir_timeline
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger
from src.modules.cliente.application.actualizar_perfil_cliente import ActualizarPerfilCliente

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroInicializarDTO,
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.auth.presentation.schemas import ConsentRequestDTO
from src.modules.cliente.presentation.cliente_v1_schemas import (
    ConsentimientosRequest,
    PerfilClienteUpdateRequest,
    PerfilClienteResponse,
    SiniestroDetalleClienteDTO,
)
from src.modules.cliente.presentation.cliente_v1_dependencies import (
    reportar_siniestro_service,
    list_siniestros_cliente_service,
    get_siniestro_cliente_service,
    subir_imagen_siniestro_service,
    get_perfil_cliente_service,
    confirm_consent_service,
    actualizar_perfil_cliente_service,
    get_auth_repo_for_enrichment,
    list_vehiculos_cliente_service,
    create_vehicle_from_poliza_service,
)
from src.modules.cliente.presentation.schemas import ConfirmDataRequestDTO
from src.modules.cliente.application.process_ocr import ProcessOcr
from src.modules.cliente.application.confirm_data import ConfirmData
from src.modules.cliente.application.create_vehicle_from_poliza import CreateVehicleFromPoliza
from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros_cliente import ListSiniestrosCliente
from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente
from src.modules.siniestro.application.siniestros.subir_imagen_siniestro import SubirImagenSiniestro
from src.modules.cliente.application.get_perfil_cliente import GetPerfilCliente
from src.modules.aseguradora.application.vehiculos.list_vehiculos_cliente import ListVehiculosCliente
from src.modules.aseguradora.presentation.vehiculos.vehiculo_dto import VehiculoResponseDTO
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.cliente.presentation.dependencies import (
    process_ocr_service,
    confirm_data_service,
)
from src.shared.infra.storage.url_resolver import resolve_storage_url
from src.core.supabase import get_supabase_client

router = APIRouter()

get_cliente = require_roles("Cliente")
EVENTO = "cliente.siniestros"


# ── Onboarding ──────────────────────────────────────────────────────────

@router.post("/onboarding/ocr")
async def ocr_extraction(
    cedula: UploadFile = File(...),
    poliza: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente),
    uc: ProcessOcr = Depends(process_ocr_service),
):
    """§1 · Extraer y validar datos de póliza e INE (extracción estructurada + validación cruzada)."""
    try:
        poliza_bytes = await poliza.read()
        cedula_bytes = await cedula.read()
        return await uc.execute(
            poliza_bytes=poliza_bytes,
            poliza_filename=poliza.filename or "poliza.pdf",
            ine_bytes=cedula_bytes,
            ine_filename=cedula.filename or "ine.jpg",
            ine_content_type=cedula.content_type or "image/jpeg",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/onboarding/confirmar-datos")
async def confirmar_datos(
    data: ConfirmDataRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: ConfirmData = Depends(confirm_data_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§1 · Confirmar datos del onboarding: guardar perfil + registrar vehículo."""
    try:
        result = uc.execute(
            usuario_id=user.usuario_id,
            aseguradora_id=user.aseguradora_id,
            data=data,
        )
        audit.record(
            evento_modulo="cliente.onboarding", accion="confirmar_datos",
            usuario=user, request=request,
            metadata={"vehiculo_id": result.get("vehiculo_id")},
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/siniestros", response_model=SiniestroResponseDTO, status_code=status.HTTP_201_CREATED)
def reportar_siniestro(
    dto: SiniestroInicializarDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: InicializarSiniestro = Depends(reportar_siniestro_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§4 · Reporte preliminar → estatus = Reportado_Preliminar."""
    siniestro = uc.execute(cliente_id=user.usuario_id, aseguradora_id=user.aseguradora_id, dto=dto)
    audit.record(
        evento_modulo=EVENTO, accion="reportar_siniestro", usuario=user,
        request=request, metadata={"siniestro_id": siniestro.id},
    )
    return siniestro


@router.get("/siniestros", response_model=Page[SiniestroResponseDTO])
def listar_mis_siniestros(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_cliente),
    uc: ListSiniestrosCliente = Depends(list_siniestros_cliente_service),
):
    """§4 · Mis siniestros (paginado)."""
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size, estatus)
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleClienteDTO)
def detalle_siniestro(
    id: str,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: GetSiniestroCliente = Depends(get_siniestro_cliente_service),
    client=Depends(get_supabase_client),
):
    """§4 · Seguimiento (detalle + imágenes + timeline de estatus)."""
    siniestro, imagenes = uc.execute(user.usuario_id, id)
    base = SiniestroResponseDTO.model_validate(siniestro)
    return SiniestroDetalleClienteDTO(
        **base.model_dump(),
        imagenes=[
            ImagenSiniestroResponseDTO.model_validate(i)
            .model_copy(update={"imagen_url": resolve_storage_url(client, i.imagen_url)})
            for i in imagenes
        ],
        timeline=construir_timeline(siniestro.estatus),
    )


@router.post(
    "/siniestros/{id}/imagenes",
    response_model=ImagenSiniestroResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
async def registrar_imagen(
    id: str,
    file: UploadFile = File(...),
    request: Request = None,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: SubirImagenSiniestro = Depends(subir_imagen_siniestro_service),
    get_detalle: GetSiniestroCliente = Depends(get_siniestro_cliente_service),
    audit: AuditLogger = Depends(get_audit_logger),
    client=Depends(get_supabase_client),
):
    """§4 · Sube una imagen directamente a Supabase Storage."""
    try:
        get_detalle.execute(user.usuario_id, id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Siniestro no encontrado o no pertenece al cliente.")

    file_bytes = await file.read()
    imagen = uc.execute(id, file_bytes, file.filename or "unknown", file.content_type or "application/octet-stream")
    audit.record(
        evento_modulo=EVENTO, accion="subir_imagen", usuario=user,
        request=request, metadata={"siniestro_id": id, "imagen_id": imagen.id},
    )
    dto = ImagenSiniestroResponseDTO.model_validate(imagen)
    dto = dto.model_copy(update={"imagen_url": resolve_storage_url(client, imagen.imagen_url)})
    return dto


def _perfil_completo(auth_repo, user: AuthenticatedUser, perfil_cliente) -> PerfilClienteResponse:
    data = PerfilClienteResponse.model_validate(perfil_cliente)
    try:
        user_data = auth_repo.get_by_id(user.usuario_id)
        if user_data:
            data.nombre = user_data.nombre
            data.email = user_data.email
            data.telefono = user_data.telefono
    except Exception:
        pass
    return data


@router.get("/perfil", response_model=PerfilClienteResponse)
def get_perfil(
    user: AuthenticatedUser = Depends(get_cliente),
    uc: GetPerfilCliente = Depends(get_perfil_cliente_service),
    auth_repo: AuthRepository = Depends(get_auth_repo_for_enrichment),
):
    """§4 · Perfil del cliente (numero_poliza, vigencia_poliza, consentimientos)."""
    perfil = uc.execute(user.usuario_id)
    return _perfil_completo(auth_repo, user, perfil)


@router.put("/perfil", response_model=PerfilClienteResponse)
def actualizar_perfil(
    dto: PerfilClienteUpdateRequest,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: ActualizarPerfilCliente = Depends(actualizar_perfil_cliente_service),
    getter: GetPerfilCliente = Depends(get_perfil_cliente_service),
    auth_repo: AuthRepository = Depends(get_auth_repo_for_enrichment),
):
    """§4 · Actualiza datos personales del cliente (nombre, email, teléfono)."""
    uc.execute(user.usuario_id, nombre=dto.nombre, email=dto.email, telefono=dto.telefono)
    perfil = getter.execute(user.usuario_id)
    return _perfil_completo(auth_repo, user, perfil)


@router.patch("/consentimientos", status_code=status.HTTP_200_OK)
def actualizar_consentimientos(
    dto: ConsentimientosRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: ConfirmConsent = Depends(confirm_consent_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§4 · Registra consentimientos LFPDPPP → setea fecha_consentimiento."""
    uc.execute(
        usuario_id=user.usuario_id,
        data=ConsentRequestDTO(
            aviso_privacidad=dto.consentimiento_aviso_privacidad,
            biometria=dto.consentimiento_biometria,
            transferencia_talleres=dto.autoriza_transferencia_talleres,
        ),
    )
    audit.record(
        evento_modulo="cliente.consentimientos", accion="actualizar_consentimientos",
        usuario=user, request=request,
    )
    return {"message": "Consentimientos registrados exitosamente."}


@router.get("/vehiculos", response_model=Page[VehiculoResponseDTO])
def listar_mis_vehiculos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_cliente),
    uc: ListVehiculosCliente = Depends(list_vehiculos_cliente_service),
):
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size)
    data = [VehiculoResponseDTO.model_validate(v) for v in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.post("/vehiculos/from-poliza", response_model=VehiculoResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_vehiculo_desde_poliza(
    file: UploadFile = File(...),
    request: Request = None,
    user: AuthenticatedUser = Depends(get_cliente),
    uc: CreateVehicleFromPoliza = Depends(create_vehicle_from_poliza_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """Crea un vehiculo a partir de los datos extraidos de una poliza de seguro via OCR."""
    pdf_bytes = await file.read()
    vehiculo = await uc.execute(
        usuario_id=user.usuario_id,
        aseguradora_id=user.aseguradora_id,
        pdf_bytes=pdf_bytes,
        filename=file.filename or "unknown",
    )
    audit.record(
        evento_modulo="cliente.vehiculos",
        accion="crear_desde_poliza",
        usuario=user,
        request=request,
        metadata={"vehiculo_id": vehiculo.id},
    )
    return vehiculo
