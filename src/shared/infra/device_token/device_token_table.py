from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from src.core.database import Base


class DeviceTokenTable(Base):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    token = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
