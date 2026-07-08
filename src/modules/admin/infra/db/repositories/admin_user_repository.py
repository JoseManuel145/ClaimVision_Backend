from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update, or_
from datetime import datetime, timezone
from src.modules.admin.domain.ports import AdminUserRepositoryPort
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.shared.domain.models import EstadoUsuario

def _user_to_dict(user) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "nombre_completo_cifrado": user.nombre_completo_cifrado,
        "telefono_cifrado": user.telefono_cifrado,
        "rol": user.rol.value if hasattr(user.rol, 'value') else user.rol,
        "estatus_arco": user.estatus_arco.value if hasattr(user.estatus_arco, 'value') else user.estatus_arco,
        "aseguradora_id": str(user.aseguradora_id) if user.aseguradora_id else None,
        "created_at": user.fecha_creacion,
        "deleted_at": user.fecha_eliminacion,
    }

class AdminUserRepository(AdminUserRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, usuario_id: str) -> dict | None:
        user = self.session.query(UserTable).filter(UserTable.id == usuario_id).first()
        if not user:
            return None
        return _user_to_dict(user)

    def bloquear_por_arco(self, usuario_id: str) -> None:
        user = self.session.query(UserTable).filter(UserTable.id == usuario_id).first()
        if user:
            user.estatus_arco = EstadoUsuario.BLOQUEADO_ARCO
            self.session.commit()

    def block_all_users_from_tenant(self, tenant_id: str) -> None:
        self.session.query(UserTable).filter(UserTable.aseguradora_id == tenant_id).update(
            {"estatus_arco": EstadoUsuario.INACTIVO}
        )
        self.session.commit()

    def list_all(
        self,
        offset: int = 0,
        limit: int = 20,
        rol: Optional[str] = None,
        estatus: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[dict], int]:
        base = select(UserTable)
        count_stmt = select(func.count()).select_from(UserTable)

        if rol:
            base = base.where(UserTable.rol == rol)
            count_stmt = count_stmt.where(UserTable.rol == rol)
        if estatus:
            base = base.where(UserTable.estatus_arco == estatus)
            count_stmt = count_stmt.where(UserTable.estatus_arco == estatus)
        if search:
            pattern = f"%{search}%"
            base = base.where(or_(UserTable.email.ilike(pattern), UserTable.nombre_completo_cifrado.ilike(pattern)))
            count_stmt = count_stmt.where(or_(UserTable.email.ilike(pattern), UserTable.nombre_completo_cifrado.ilike(pattern)))

        total = self.session.execute(count_stmt).scalar() or 0
        stmt = base.order_by(UserTable.fecha_creacion.desc()).offset(offset).limit(limit)
        results = self.session.execute(stmt).scalars().all()
        return [_user_to_dict(r) for r in results], total

    def update_user(self, usuario_id: str, data: dict) -> dict | None:
        user = self.session.query(UserTable).filter(UserTable.id == usuario_id).first()
        if not user:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return _user_to_dict(user)

    def soft_delete(self, usuario_id: str) -> bool:
        user = self.session.query(UserTable).filter(UserTable.id == usuario_id).first()
        if not user:
            return False
        user.fecha_eliminacion = datetime.now(timezone.utc)
        user.estatus_arco = EstadoUsuario.INACTIVO
        user.email = f"eliminado_{usuario_id}@anon.claimvision"  # liberar email único
        user.nombre_completo_cifrado = "[ELIMINADO]"
        user.telefono_cifrado = "[ELIMINADO]"
        self.session.commit()
        return True
