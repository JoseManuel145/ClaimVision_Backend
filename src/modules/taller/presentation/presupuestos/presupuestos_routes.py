from fastapi import APIRouter, Depends, status
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.taller.presentation.taller_dto import GuardarPresupuestoRequestDTO, CotizacionTallerDTO
from src.modules.taller.presentation.taller_dependencies import guardar_presupuesto_service
from src.shared.domain.models import Rol

router = APIRouter(prefix="/expedientes", tags=["Taller - Presupuestos"])

def check_operador_taller(user: AuthenticatedUser = Depends(get_current_user)):
    if user.rol != Rol.TALLER.value:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Acceso denegado. Rol requerido: Operador_Taller.")
    return user

@router.post("/{id}/presupuesto", response_model=CotizacionTallerDTO, status_code=status.HTTP_201_CREATED)
def guardar_presupuesto(
    id: str,
    dto: GuardarPresupuestoRequestDTO,
    user=Depends(check_operador_taller),
    uc=Depends(guardar_presupuesto_service)
):
    return uc.execute(
        siniestro_id=id,
        usuario_id=user.usuario_id,
        monto_mano_obra=dto.monto_mano_obra,
        monto_refacciones=dto.monto_refacciones,
        observaciones_tecnicas=dto.observaciones_tecnicas
    )
