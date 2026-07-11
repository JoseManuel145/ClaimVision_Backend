import uuid
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.core.database import Base
from src.shared.domain.models import TipoDano, SeveridadDano

class PeritajeAjustadorTable(Base):
    __tablename__ = "peritajes_ajustador"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    siniestro_id = Column(UUID(as_uuid=True), ForeignKey("siniestros.id"), unique=True, nullable=False)
    ajustador_id = Column(UUID(as_uuid=True), ForeignKey("ajustadores.id"), nullable=False)
    costo_definitivo_ajustador = Column(Float, nullable=False)
    firma_digital_ajustador = Column(String, nullable=False)
    observaciones_campo = Column(String, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __mapper_args__ = {"version_id_col": version}

    danos = relationship("DanosAjustadosManualTable", back_populates="peritaje", cascade="all, delete-orphan")

class DanosAjustadosManualTable(Base):
    __tablename__ = "danos_ajustados_manual"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    peritaje_ajustador_id = Column(UUID(as_uuid=True), ForeignKey("peritajes_ajustador.id"), nullable=False)
    zona_vehiculo = Column(String, nullable=False)
    tipo = Column(SQLEnum(TipoDano, name="tipo_dano", values_callable=lambda x: [e.value for e in x]), nullable=False)
    severidad = Column(SQLEnum(SeveridadDano, name="severidad_dano", values_callable=lambda x: [e.value for e in x]), nullable=False)
    costo_real_reparacion = Column(Float, nullable=False)
    origen_cambio = Column(String, nullable=False, default='AJUSTADOR')
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __mapper_args__ = {"version_id_col": version}

    peritaje = relationship("PeritajeAjustadorTable", back_populates="danos")
