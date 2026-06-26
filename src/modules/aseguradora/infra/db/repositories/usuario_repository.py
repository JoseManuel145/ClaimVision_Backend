from sqlalchemy.orm import Session
from sqlalchemy import update
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.aseguradora.domain.ports.usuario_repository_port import UsuarioRepositoryPort
from src.shared.domain.models import EstadoUsuario
import uuid

class UsuarioRepository(UsuarioRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def _uuid_or_raise(self, id: str) -> uuid.UUID:
        if not id:
            raise ValueError("id es requerido")
        return uuid.UUID(id)

    def get_by_id(self, id: str) -> dict | None:
        user = self.db.query(UserTable).filter(UserTable.id == self._uuid_or_raise(id)).first()
        if not user:
            return None
        return {
            "id": str(user.id),
            "estado": user.estatus_arco.value,
            "aseguradora_id": str(user.aseguradora_id) if user.aseguradora_id else None
        }

    def bloquear_por_arco(self, id: str) -> None:
        stmt = update(UserTable).where(UserTable.id == self._uuid_or_raise(id)).values(
            estatus_arco=EstadoUsuario.BLOQUEADO_ARCO.value,
            nombre_completo_cifrado="[BLOQUEADO_ARCO]",
            telefono_cifrado="[BLOQUEADO_ARCO]"
        )
        self.db.execute(stmt)
        self.db.commit()

    def desbloquear_por_arco(self, id: str) -> None:
        stmt = update(UserTable).where(UserTable.id == self._uuid_or_raise(id)).values(
            estatus_arco=EstadoUsuario.ACTIVO.value,
        )
        self.db.execute(stmt)
        self.db.commit()
