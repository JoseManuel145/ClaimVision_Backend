from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class TallerTable(Base):
    __tablename__ = "talleres"

    id = Column(UUID(as_uuid=True), primary_key=True)
    nombre_comercial = Column(String, nullable=False)
    rfc = Column(String, unique=True, nullable=False)
    direccion_tecnica = Column(String, nullable=False)
    telefono_contacto = Column(String, nullable=False)
    fecha_creacion = Column("created_at", DateTime, nullable=False)
