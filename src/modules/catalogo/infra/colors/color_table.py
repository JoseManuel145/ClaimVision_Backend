from sqlalchemy import Column, ForeignKey, Integer, String

from src.core.database import Base


class ColorTable(Base):
    __tablename__ = "color"

    color_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)


class ProductoColorTable(Base):
    __tablename__ = "producto_color"

    producto_color_id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(String, ForeignKey("producto.producto_id"), nullable=False)
    color_id = Column(Integer, ForeignKey("color.color_id"), nullable=False)
