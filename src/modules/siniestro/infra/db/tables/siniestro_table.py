import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Numeric, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base
from src.shared.domain.models import EstatusSiniestro

class SiniestroTable(Base):
    __tablename__ = "siniestros"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aseguradora_id = Column(UUID(as_uuid=True), nullable=True)
    cliente_id = Column(UUID(as_uuid=True), nullable=False)
    ajustador_id = Column(UUID(as_uuid=True), nullable=True)
    taller_id = Column(UUID(as_uuid=True), nullable=True)
    vehiculo_id = Column(UUID(as_uuid=True), nullable=True)
    estatus = Column(Enum(EstatusSiniestro, name="estatus_siniestro", values_callable=lambda x: [e.value for e in x]), nullable=False, default=EstatusSiniestro.REPORTADO_PRELIMINAR.value)
    vehiculo_marca = Column(String, nullable=False)
    vehiculo_modelo = Column(String, nullable=False)
    vehiculo_anio = Column(Integer, nullable=False)
    vehiculo_placas = Column(String, nullable=False)
    vehiculo_vin = Column(String, nullable=True)
    latitud_siniestro = Column(Numeric(10, 8), nullable=False)
    longitud_siniestro = Column(Numeric(11, 8), nullable=False)
    narracion_texto = Column(String, nullable=True)
    narracion_audio_url = Column(String, nullable=True)
    indicaciones_dano_interno = Column(Boolean, nullable=False, default=False)
    fecha_siniestro = Column(DateTime(timezone=True), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
