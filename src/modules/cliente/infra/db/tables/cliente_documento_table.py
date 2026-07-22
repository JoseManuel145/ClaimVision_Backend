from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class ClienteDocumentoTable(Base):
    __tablename__ = "cliente_documentos"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    usuario_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    identificacion_url = Column(String, nullable=True)
    identificacion_tipo = Column(String, nullable=True)
    identificacion_subido_en = Column(DateTime(timezone=True), nullable=True)
    poliza_url = Column(String, nullable=True)
    poliza_tipo = Column(String, nullable=True)
    poliza_subido_en = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
