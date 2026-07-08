from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.modules.admin.infra.db.repositories.aseguradora_repository import AseguradoraRepository
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.aseguradora.application.perfil.get_perfil_aseguradora import GetPerfilAseguradora
from src.modules.aseguradora.application.perfil.actualizar_perfil_aseguradora import ActualizarPerfilAseguradora


def get_perfil_aseguradora_service(session: Session = Depends(get_session)) -> GetPerfilAseguradora:
    return GetPerfilAseguradora(AseguradoraRepository(session))


def actualizar_perfil_aseguradora_service(session: Session = Depends(get_session)) -> ActualizarPerfilAseguradora:
    return ActualizarPerfilAseguradora(AseguradoraRepository(session), AuthRepository(session))
