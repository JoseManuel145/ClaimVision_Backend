from src.shared.domain.models import Rol
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.auth.domain.models import User
from src.modules.auth.domain.ports import AuthPort
from src.core.exceptions import NotFoundError
from src.shared.domain.models import EstadoUsuario
from src.shared.domain.services.encryption_service import encrypt_fields, decrypt_fields
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy import update

def _to_domain(obj: UserTable) -> User:
    decrypted = decrypt_fields({
        "nombre_completo_cifrado": obj.nombre_completo_cifrado,
        "telefono_cifrado": obj.telefono_cifrado or "",
    })
    return User(
        usuario_id=str(obj.id) if obj.id is not None else None,
        nombre=decrypted.get("nombre_completo", ""),
        email=obj.email,
        password=obj.password_hash,
        telefono=decrypted.get("telefono", ""),
        rol=obj.rol.value if hasattr(obj.rol, 'value') else obj.rol,
        estado=obj.estatus_arco.value if hasattr(obj.estatus_arco, 'value') else obj.estatus_arco,
        aseguradora_id=str(obj.aseguradora_id) if obj.aseguradora_id is not None else None,
        primer_cambio_password=obj.primer_cambio_password,
        fecha_creacion=obj.fecha_creacion,
        is_authenticated=False,
        fecha_eliminacion=obj.fecha_eliminacion
    )

class AuthRepository(AuthPort):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        encrypted = encrypt_fields({
            "nombre_completo": user.nombre,
            "telefono": user.telefono or "",
            "email": user.email,
            "password_hash": user.password,
            "rol": user.rol if user.rol else Rol.CLIENTE.value,
            "estatus_arco": user.estado if user.estado else EstadoUsuario.ACTIVO.value,
            "aseguradora_id": user.aseguradora_id,
            "fecha_creacion": user.fecha_creacion,
            "fecha_eliminacion": user.fecha_eliminacion,
        })
        model = UserTable(
            id=user.usuario_id,
            nombre_completo_cifrado=encrypted["nombre_completo_cifrado"],
            email=encrypted["email"],
            password_hash=encrypted["password_hash"],
            telefono_cifrado=encrypted.get("telefono_cifrado", ""),
            rol=encrypted["rol"],
            estatus_arco=encrypted["estatus_arco"],
            aseguradora_id=encrypted["aseguradora_id"],
            primer_cambio_password=True,
            fecha_creacion=encrypted["fecha_creacion"],
            fecha_eliminacion=encrypted["fecha_eliminacion"],
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, usuario_id: str) -> User | None:
        stmt = select(UserTable).where(UserTable.id == usuario_id)
        r = self.db.execute(stmt).scalar()
        if r is None:
            return None
        return _to_domain(r)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserTable).where(UserTable.email == email)
        r = self.db.execute(stmt).scalar_one_or_none()
        if r is None:
            return None
        return _to_domain(r)

    def update_password(self, usuario_id: str, password_hash: str) -> None:
        stmt = (
            update(UserTable)
            .where(UserTable.id == usuario_id)
            .values(password_hash=password_hash)
        )

        result = self.db.execute(stmt)

        if result.rowcount == 0:
            raise NotFoundError("User not found")

        self.db.commit()

    def update_password_with_flag(self, usuario_id: str, password_hash: str, primer_cambio: bool = False) -> None:
        stmt = (
            update(UserTable)
            .where(UserTable.id == usuario_id)
            .values(password_hash=password_hash, primer_cambio_password=primer_cambio)
        )

        result = self.db.execute(stmt)

        if result.rowcount == 0:
            raise NotFoundError("User not found")

        self.db.commit()

    def update_user_profile(self, usuario_id: str, nombre: str | None = None, email: str | None = None, telefono: str | None = None) -> None:
        vals = {}
        if nombre is not None:
            vals["nombre_completo"] = nombre
        if email is not None:
            vals["email"] = email
        if telefono is not None:
            vals["telefono"] = telefono
        if not vals:
            return
        encrypted = encrypt_fields(vals)
        col_map = {}
        if "nombre_completo_cifrado" in encrypted:
            col_map["nombre_completo_cifrado"] = encrypted["nombre_completo_cifrado"]
        if "telefono_cifrado" in encrypted:
            col_map["telefono_cifrado"] = encrypted["telefono_cifrado"]
        if "email" in encrypted:
            col_map["email"] = encrypted["email"]
        stmt = update(UserTable).where(UserTable.id == usuario_id).values(**col_map)
        self.db.execute(stmt)
        self.db.commit()

    def verify_user(self, usuario_id: str) -> None:
        stmt = select(UserTable).where(UserTable.id == usuario_id)
        r = self.db.execute(stmt).scalar()
        if r is None:
            raise NotFoundError("User not found")
