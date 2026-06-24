import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class AjustadorTable(Base):
    __tablename__ = "ajustadores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    cedula_profesional = Column(String, unique=True, nullable=False)
    geolocalizacion_actual = Column(String, nullable=True) # WKT format 'POINT(lon lat)'
    activo_para_servicio = Column(Boolean, nullable=False, default=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
