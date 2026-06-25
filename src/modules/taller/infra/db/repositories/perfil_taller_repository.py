import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.modules.taller.infra.db.tables.perfil_taller_table import PerfilTallerUsuariosTable

class PerfilTallerRepository(PerfilTallerRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def get_taller_id_by_usuario(self, usuario_id: str) -> Optional[str]:
        stmt = select(PerfilTallerUsuariosTable.taller_id).where(
            PerfilTallerUsuariosTable.usuario_id == uuid.UUID(usuario_id),
            PerfilTallerUsuariosTable.deleted_at.is_(None)
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        if not result:
            return None
        return str(result)
