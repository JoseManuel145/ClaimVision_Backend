from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class AuditLogTable(Base):
    __tablename__ = "logs_auditoria"

    id = Column(UUID(as_uuid=True), primary_key=True)
    created_at = Column("created_at", DateTime(timezone=True), primary_key=True)
    usuario_id = Column(UUID(as_uuid=True), nullable=True)
    aseguradora_id = Column(UUID(as_uuid=True), nullable=True)
    evento_modulo = Column(String, nullable=False)
    accion_realizada = Column(String, nullable=False)
    direccion_ip = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    metadata_context = Column(JSON, nullable=True)
