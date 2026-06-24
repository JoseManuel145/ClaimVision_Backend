from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.core.database import Base


class ProductoTable(Base):
    __tablename__ = "producto"

    producto_id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio = Column(Integer, nullable=False)
    esta_activo = Column(Boolean, default=True)
    esta_destacado = Column(Boolean, default=False)
    stock = Column(Integer, default=0)
    fecha_creacion = Column(DateTime, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.categoria_id"), nullable=True)

    imagenes = relationship("ImagenTable", secondary="producto_imagen")
    tallas = relationship("TallaTable", "producto_talla", viewonly=True)
    colores = relationship("ColorTable", "producto_color", viewonly=True)
