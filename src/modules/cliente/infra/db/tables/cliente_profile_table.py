from sqlalchemy import Column, String, DateTime, Boolean, Date, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base

class ClienteProfileTable(Base):
    __tablename__ = "perfiles_clientes"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True)
    usuario_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    numero_poliza = Column(String, nullable=False)
    vigencia_poliza = Column(Date, nullable=False)
    curp_rfc_cifrado = Column(String, nullable=False)
    consentimiento_aviso_privacidad = Column(Boolean, nullable=False, default=False)
    consentimiento_biometria = Column(Boolean, nullable=False, default=False)
    autoriza_transferencia_talleres = Column(Boolean, nullable=False, default=False)
    fecha_consentimiento = Column(DateTime(timezone=True), nullable=True)
    fecha_creacion = Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now())
    version = Column(Integer, nullable=False, default=1)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
