from src.shared.domain.models import Rol
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.auth.domain.models import AuthUser
from src.modules.auth.domain.ports import AuthPort
from src.core.exceptions import NotFoundError
from src.shared.domain.models import EstadoUsuario
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy import update

def _to_domain(obj: UserTable) -> AuthUser:
    return AuthUser(
        usuario_id=str(obj.id) if obj.id is not None else None,
        nombre=obj.nombre_completo_cifrado,
        email=obj.email,
        password=obj.password_hash,
        telefono=obj.telefono_cifrado or "",
        rol=obj.rol,
        estado=obj.estatus_arco,
        aseguradora_id=str(obj.aseguradora_id) if obj.aseguradora_id is not None else None,
        fecha_creacion=obj.fecha_creacion,
        is_authenticated=False,
        fecha_eliminacion=obj.fecha_eliminacion
    )

class AuthRepository(AuthPort):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: AuthUser) -> AuthUser:
        model = UserTable(
            usuario_id=user.usuario_id,
            nombre_completo_cifrado=user.nombre,
            email=user.email,
            password_hash=user.password,
            telefono_cifrado=user.telefono or "",
            rol=user.rol if user.rol else Rol.CLIENTE.value,
            estatus_arco=user.estado if user.estado else EstadoUsuario.ACTIVO.value,
            aseguradora_id=user.aseguradora_id,
            fecha_creacion=user.fecha_creacion,
            fecha_eliminacion=user.fecha_eliminacion
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, usuario_id: str) -> AuthUser | None:
        stmt = select(UserTable).where(UserTable.usuario_id == usuario_id)
        r = self.db.execute(stmt).scalar()
        if r is None:
            return None
        return _to_domain(r)

    def get_by_email(self, email: str) -> AuthUser | None:
        stmt = select(UserTable).where(UserTable.email == email)
        r = self.db.execute(stmt).scalar_one_or_none()
        if r is None:
            return None
        return _to_domain(r)

    def update_password(self, usuario_id: str, password_hash: str) -> None:
        stmt = (
            update(UserTable)
            .where(UserTable.usuario_id == usuario_id)
            .values(password_hash=password_hash)
        )

        result = self.db.execute(stmt)

        if result.rowcount == 0:
            raise NotFoundError("User not found")

        self.db.commit()

    def verify_user(self, usuario_id: str) -> None:
        stmt = select(UserTable).where(UserTable.usuario_id == usuario_id)
        r = self.db.execute(stmt).scalar()
        if r is None:
            raise NotFoundError("User not found")
