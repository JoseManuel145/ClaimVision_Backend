from fastapi import APIRouter, Depends

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.aseguradora.presentation.perfil.perfil_dto import (
    PerfilAseguradoraDTO,
    PerfilAseguradoraUpdateDTO,
)
from src.modules.aseguradora.presentation.perfil import perfil_dependencies as deps
from src.modules.aseguradora.application.perfil.get_perfil_aseguradora import GetPerfilAseguradora
from src.modules.aseguradora.application.perfil.actualizar_perfil_aseguradora import ActualizarPerfilAseguradora

router = APIRouter()
get_operador = require_roles("Operador_Aseguradora")


@router.get("", response_model=PerfilAseguradoraDTO)
def obtener_perfil(
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetPerfilAseguradora = Depends(deps.get_perfil_aseguradora_service),
):
    aseguradora = uc.execute(user.aseguradora_id)
    return PerfilAseguradoraDTO.model_validate(aseguradora)


@router.put("", response_model=PerfilAseguradoraDTO)
def actualizar_perfil(
    dto: PerfilAseguradoraUpdateDTO,
    user: AuthenticatedUser = Depends(get_operador),
    uc: ActualizarPerfilAseguradora = Depends(deps.actualizar_perfil_aseguradora_service),
):
    """Actualiza datos de la aseguradora y del operador autenticado."""
    aseguradora = uc.execute(
        aseguradora_id=user.aseguradora_id,
        usuario_id=user.usuario_id,
        nombre=dto.nombre,
        rfc=dto.rfc,
        dominio_correo=dto.dominio_correo,
        contacto_legal_email=dto.contacto_legal_email,
        operador_nombre=dto.operador_nombre,
        operador_email=dto.operador_email,
        operador_telefono=dto.operador_telefono,
    )
    return PerfilAseguradoraDTO.model_validate(aseguradora)
