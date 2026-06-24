from fastapi import APIRouter, Depends, status
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.aseguradora.presentation.usuarios.usuario_dependencies import bloqueo_arco_service, desbloqueo_arco_service

router = APIRouter()

def get_aseguradora_user(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
    if user.rol != "Operador_Aseguradora" or not user.aseguradora_id:
        pass
    return user

@router.post("/{id}/bloqueo-arco", status_code=status.HTTP_200_OK)
def aplicar_bloqueo_arco(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(bloqueo_arco_service)
):
    uc.execute(user.aseguradora_id, id)
    return {"message": "Bloqueo ARCO aplicado exitosamente"}

@router.post("/{id}/desbloqueo-arco", status_code=status.HTTP_200_OK)
def aplicar_desbloqueo_arco(
    id: str,
    user: AuthenticatedUser = Depends(get_aseguradora_user),
    uc=Depends(desbloqueo_arco_service)
):
    uc.execute(user.aseguradora_id, id)
    return {"message": "Desbloqueo ARCO aplicado exitosamente"}
