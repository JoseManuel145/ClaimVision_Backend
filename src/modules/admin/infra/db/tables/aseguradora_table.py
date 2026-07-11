from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from src.core.database import Base
from src.shared.domain.models import EstatusComercialAseguradora

class AseguradoraTable(Base):
    __tablename__ = "aseguradoras"
    __mapper_args__ = {"version_id_col": "version"}

    id = Column(UUID(as_uuid=True), primary_key=True)
    nombre = Column(String, nullable=False)
    rfc = Column(String, unique=True, nullable=False)
    dominio_correo = Column(String, unique=True, nullable=False)
    plan_suscripcion = Column(String, nullable=False)
    limite_peritajes_mes = Column(Integer, nullable=False)
    peritajes_consumidos_mes = Column(Integer, nullable=False, default=0)
    estatus_comercial = Column(Enum(EstatusComercialAseguradora, name='estatus_comercial_aseguradora', values_callable=lambda x: [e.value for e in x]), nullable=False, default=EstatusComercialAseguradora.ACTIVO.value)
    contacto_legal_email = Column(String, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
