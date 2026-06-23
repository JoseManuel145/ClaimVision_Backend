from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from src.core.database import Base

class RecoveryCodeTable(Base):
    __tablename__ = "recovery_code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String, ForeignKey("usuario.usuario_id"), nullable=False)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

