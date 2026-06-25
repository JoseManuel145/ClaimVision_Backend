import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, func, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from src.core.database import Base

class ImagenSiniestroTable(Base):
    __tablename__ = "imagenes_siniestro"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    siniestro_id = Column(UUID(as_uuid=True), nullable=False)
    imagen_url = Column(String, nullable=False)
    es_calidad_valida = Column(Boolean, nullable=False, default=True)
    metadatos_json = Column(JSONB, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
