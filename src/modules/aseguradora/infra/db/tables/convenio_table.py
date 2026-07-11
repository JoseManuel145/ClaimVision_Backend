from sqlalchemy import Column, Integer, DateTime, Date, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class ConvenioAseguradoraTallerTable(Base):
    __tablename__ = "convenio_aseguradora_taller"

    aseguradora_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    taller_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    fecha_convenio = Column(Date, nullable=False, server_default=func.current_date())
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __mapper_args__ = {"version_id_col": version}
