import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class VehiculoTable(Base):
    __tablename__ = "vehiculos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aseguradora_id = Column(UUID(as_uuid=True), ForeignKey("aseguradoras.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("perfiles_clientes.id"), nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    placas = Column(String, nullable=False)
    vin = Column(String, nullable=True)
    color = Column(String, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
