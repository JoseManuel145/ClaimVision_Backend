from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, File, Form, status
from uuid import UUID

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.presentation.vehiculos.vehiculo_dto import (
    VehiculoCreateDTO,
    VehiculoUpdateDTO,
    VehiculoResponseDTO,
)
from src.modules.aseguradora.application.vehiculos.create_vehiculo import CreateVehiculo
from src.modules.aseguradora.application.vehiculos.create_vehiculo_from_poliza import CreateVehiculoFromPoliza
from src.modules.aseguradora.application.vehiculos.list_vehiculos import ListVehiculos
from src.modules.aseguradora.application.vehiculos.get_vehiculo import GetVehiculo
from src.modules.aseguradora.application.vehiculos.update_vehiculo import UpdateVehiculo
from src.modules.aseguradora.application.vehiculos.delete_vehiculo import DeleteVehiculo
from src.modules.aseguradora.presentation.vehiculos import vehiculo_dependencies

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"


def _require_aseguradora(user: AuthenticatedUser):
    if not user.aseguradora_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operador no tiene una aseguradora asignada.",
        )
    return user.aseguradora_id


@router.post("", response_model=VehiculoResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_vehiculo(
    dto: VehiculoCreateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: CreateVehiculo = Depends(vehiculo_dependencies.create_vehiculo_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(
        _require_aseguradora(user), dto.cliente_id, dto.marca, dto.modelo,
        dto.anio, dto.placas, dto.vin, dto.color,
    )
    audit.record(
        evento_modulo=EVENTO, accion="crear_vehiculo",
        usuario=user, request=request,
        metadata={"vehiculo_id": resultado.id},
    )
    return resultado


@router.get("", response_model=Page[VehiculoResponseDTO])
def listar_vehiculos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    cliente_id: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_operador),
    uc: ListVehiculos = Depends(vehiculo_dependencies.list_vehiculos_service),
):
    items, total = uc.execute(
        _require_aseguradora(user), offset_from_page(page, page_size), page_size, cliente_id,
    )
    data = [VehiculoResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/{id}", response_model=VehiculoResponseDTO)
def obtener_vehiculo(
    id: UUID,
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetVehiculo = Depends(vehiculo_dependencies.get_vehiculo_service),
):
    return uc.execute(str(id))


@router.put("/{id}", response_model=VehiculoResponseDTO)
def actualizar_vehiculo(
    id: UUID,
    dto: VehiculoUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: UpdateVehiculo = Depends(vehiculo_dependencies.update_vehiculo_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    resultado = uc.execute(
        str(id), dto.marca, dto.modelo, dto.anio, dto.placas, dto.vin, dto.color,
    )
    audit.record(
        evento_modulo=EVENTO, accion="actualizar_vehiculo",
        usuario=user, request=request,
        metadata={"vehiculo_id": str(id)},
    )
    return resultado


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vehiculo(
    id: UUID,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: DeleteVehiculo = Depends(vehiculo_dependencies.delete_vehiculo_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    uc.execute(str(id))
    audit.record(
        evento_modulo=EVENTO, accion="eliminar_vehiculo",
        usuario=user, request=request,
        metadata={"vehiculo_id": str(id)},
    )


@router.post("/from-poliza", response_model=VehiculoResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_vehiculo_desde_poliza(
    cliente_id: str = Form(...),
    file: UploadFile = File(...),
    request: Request = None,
    user: AuthenticatedUser = Depends(get_operador),
    uc: CreateVehiculoFromPoliza = Depends(vehiculo_dependencies.create_vehiculo_from_poliza_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """Crea un vehiculo a partir de los datos extraidos de una poliza de seguro via OCR."""
    pdf_bytes = await file.read()
    vehiculo = await uc.execute(
        aseguradora_id=_require_aseguradora(user),
        cliente_id=cliente_id,
        pdf_bytes=pdf_bytes,
        filename=file.filename or "unknown",
    )
    audit.record(
        evento_modulo=EVENTO,
        accion="crear_vehiculo_desde_poliza",
        usuario=user,
        request=request,
        metadata={"vehiculo_id": vehiculo.id, "cliente_id": cliente_id},
    )
    return vehiculo
