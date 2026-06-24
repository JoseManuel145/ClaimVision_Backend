from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class AjustadorTable(Base):
    __tablename__ = "ajustadores"

    id = Column(UUID(as_uuid=True), primary_key=True)
    usuario_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    cedula_profesional = Column(String, unique=True, nullable=False)
    # geolocalizacion_actual se manejará si postgis está activo, pero por ahora simplificamos.
    activo_para_servicio = Column(Boolean, nullable=False, default=True)
    fecha_creacion = Column("created_at", DateTime, nullable=False)
