from sqlalchemy import Column, Integer, String
from src.core.database import Base


class SeccionTable(Base):
    __tablename__ = "seccion"

    seccion_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
