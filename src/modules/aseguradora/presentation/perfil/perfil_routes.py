from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.admin.infra.db.repositories.aseguradora_repository import AseguradoraRepository
from src.modules.aseguradora.presentation.perfil.perfil_dto import PerfilAseguradoraDTO

router = APIRouter()
get_operador = require_roles("Operador_Aseguradora")


@router.get("", response_model=PerfilAseguradoraDTO)
def obtener_perfil(
    user: AuthenticatedUser = Depends(get_operador),
    db: Session = Depends(get_session),
):
    repo = AseguradoraRepository(db)
    aseguradora = repo.get_by_id(user.aseguradora_id)
    return PerfilAseguradoraDTO.model_validate(aseguradora)
