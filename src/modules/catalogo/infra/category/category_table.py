from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base


class CategoriaTable(Base):
    __tablename__ = "categoria"

    categoria_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    seccion_id = Column(Integer, ForeignKey("seccion.seccion_id"), nullable=False)

    seccion = relationship("SeccionTable", backref="categorias")
