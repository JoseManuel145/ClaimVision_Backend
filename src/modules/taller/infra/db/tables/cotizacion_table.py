import uuid
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from src.core.database import Base
from src.shared.domain.models import EstatusCotizacion

class CotizacionTallerTable(Base):
    __tablename__ = "cotizaciones_taller"
    __mapper_args__ = {"version_id_col": "version"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    siniestro_id = Column(UUID(as_uuid=True), ForeignKey("siniestros.id"), nullable=False)
    taller_id = Column(UUID(as_uuid=True), ForeignKey("talleres.id"), nullable=False)
    monto_mano_obra = Column(Float, nullable=False)
    monto_refacciones = Column(Float, nullable=False)
    monto_total = Column(Float, nullable=False)
    desglose_pdf_url = Column(String, nullable=False)
    estatus = Column(SQLEnum(EstatusCotizacion, name="estatus_cotizacion"), nullable=False, default=EstatusCotizacion.PENDIENTE_APROBACION)
    observaciones_tecnicas = Column(String, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
