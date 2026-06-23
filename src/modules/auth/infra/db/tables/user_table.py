from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base
from src.shared.domain.models import Rol, EstadoUsuario

class UserTable(Base):
    __tablename__ = "usuarios"

    usuario_id = Column("id", UUID(as_uuid=True), primary_key=True)
    aseguradora_id = Column(UUID(as_uuid=True), nullable=True)
    rol = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre_completo_cifrado = Column(String, nullable=False)
    telefono_cifrado = Column(String, nullable=True)
    estatus_arco = Column(String, nullable=False, default=EstadoUsuario.ACTIVO.value)
    fecha_creacion = Column("created_at", DateTime, nullable=False)
    fecha_eliminacion = Column("deleted_at", DateTime, nullable=True)
