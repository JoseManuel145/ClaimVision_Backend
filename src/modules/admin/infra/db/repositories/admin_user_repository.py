from sqlalchemy.orm import Session
from src.modules.admin.domain.ports import AdminUserRepositoryPort
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.shared.domain.models import EstadoUsuario

class AdminUserRepository(AdminUserRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, usuario_id: str) -> dict | None:
        user = self.session.query(UserTable).filter(UserTable.id == usuario_id).first()
        if not user:
            return None
        return {"id": user.id, "estado": user.estatus_arco}

    def bloquear_por_arco(self, usuario_id: str) -> None:
        user = self.session.query(UserTable).filter(UserTable.id == usuario_id).first()
        if user:
            user.estatus_arco = EstadoUsuario.BLOQUEADO_ARCO
            # Revocar tokens (aislamiento lógico) - asumiendo que el estado BLOQUEADO_ARCO no permite login
            # Cifrado simulado de datos nominativos, en un caso real se cifran las columnas con AES-256
            self.session.commit()

    def block_all_users_from_tenant(self, tenant_id: str) -> None:
        self.session.query(UserTable).filter(UserTable.aseguradora_id == tenant_id).update(
            {"estatus_arco": EstadoUsuario.INACTIVO}
        )
        self.session.commit()
