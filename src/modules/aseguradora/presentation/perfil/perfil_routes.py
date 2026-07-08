from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update as sa_update

from src.core.database import get_session
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.admin.infra.db.repositories.aseguradora_repository import AseguradoraRepository
from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable
from src.modules.aseguradora.presentation.perfil.perfil_dto import (
    PerfilAseguradoraDTO,
    PerfilAseguradoraUpdateDTO,
)
from src.shared.domain.services.encryption_service import encrypt_fields

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


@router.put("", response_model=PerfilAseguradoraDTO)
def actualizar_perfil(
    dto: PerfilAseguradoraUpdateDTO,
    user: AuthenticatedUser = Depends(get_operador),
    db: Session = Depends(get_session),
):
    """Actualiza datos de la aseguradora y del operador autenticado."""

    aseg_update = {}
    if dto.nombre is not None:
        aseg_update["nombre"] = dto.nombre
    if dto.rfc is not None:
        aseg_update["rfc"] = dto.rfc
    if dto.dominio_correo is not None:
        aseg_update["dominio_correo"] = dto.dominio_correo
    if dto.contacto_legal_email is not None:
        aseg_update["contacto_legal_email"] = dto.contacto_legal_email
    if aseg_update:
        db.execute(
            sa_update(AseguradoraTable).where(AseguradoraTable.id == user.aseguradora_id).values(**aseg_update)
        )

    user_update = {}
    if dto.operador_nombre is not None:
        user_update["nombre_completo"] = dto.operador_nombre
    if dto.operador_email is not None:
        user_update["email"] = dto.operador_email
    if dto.operador_telefono is not None:
        user_update["telefono"] = dto.operador_telefono
    if user_update:
        encrypted = encrypt_fields(user_update)
        db.execute(
            sa_update(UserTable).where(UserTable.id == user.usuario_id).values(**encrypted)
        )

    db.commit()

    repo = AseguradoraRepository(db)
    aseguradora = repo.get_by_id(user.aseguradora_id)
    return PerfilAseguradoraDTO.model_validate(aseguradora)
