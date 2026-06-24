from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.catalogo.domain.models import ColorModel, ProductoColorModel
from src.modules.catalogo.domain.ports import ColorPort, ProductoColorPort
from src.modules.catalogo.infra.colors.color_table import ColorTable, ProductoColorTable


def to_domain_color(r: ColorTable) -> ColorModel:
    return ColorModel(
        color_id=r.color_id,
        nombre=r.nombre
    )


class ColorRepository(ColorPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> list[ColorModel]:
        stmt = select(ColorTable)
        rows = self.db.execute(stmt).scalars().all()
        return [to_domain_color(r) for r in rows]

    def get_by_id(self, color_id: int) -> ColorModel | None:
        r = self.db.get_one(ColorTable, color_id)
        return to_domain_color(r) if r else None  # type: ignore[arg-type]

    def create(self, model: ColorModel) -> ColorModel:
        color = ColorTable(
            nombre=model.nombre
        )
        self.db.add(color)
        self.db.commit()
        self.db.refresh(color)
        return to_domain_color(color)

    def update(self, color_id: int, model: ColorModel) -> ColorModel | None:
        r = self.db.get_one(ColorTable, color_id)
        if not r:
            return None
        r.nombre = model.nombre
        return to_domain_color(r)  # type: ignore[arg-type]

    def delete(self, color_id: int) -> None:
        r = self.db.get(ColorTable, color_id)
        self.db.delete(r)
        self.db.commit()
        return


def to_domain_p_color(r: ProductoColorTable) -> ProductoColorModel:
    return ProductoColorModel(
        producto_color_id=r.producto_color_id,
        color_id=r.color_id,
        producto_id=r.producto_id
    )


class ProductoColorRepository(ProductoColorPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_by_producto(self, p_id: str) -> list[ColorModel]:
        stmt = (
            select(ColorTable)
            .join(ProductoColorTable, ColorTable.color_id == ProductoColorTable.color_id)
            .where(ProductoColorTable.producto_id == p_id)
        )
        rows = self.db.execute(stmt).scalars().all()

        return [to_domain_color(r) for r in rows]

    def get_by_id(self, p_color_id: int) -> ProductoColorModel:
        r = self.db.get(ProductoColorTable, p_color_id)
        return to_domain_p_color(r) if r else None  # type: ignore[arg-type]

    def assign_to_producto(self, p_color: ProductoColorModel) -> ProductoColorModel:
        assign = ProductoColorTable(
            producto_id=p_color.producto_id,
            color_id=p_color.color_id
        )
        self.db.add(assign)
        self.db.commit()
        self.db.refresh(assign)
        return to_domain_p_color(assign)

    def remove_from_producto(self, producto_id: str, color_id: int) -> None:
        stmt = (select(ProductoColorTable)
                .filter(ProductoColorTable.producto_id == producto_id)
                .filter(ProductoColorTable.color_id == color_id)
                )
        r = self.db.execute(stmt).scalar_one_or_none()
        self.db.delete(r)
        self.db.commit()
        return
