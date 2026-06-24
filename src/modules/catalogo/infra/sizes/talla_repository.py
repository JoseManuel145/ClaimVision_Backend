from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.catalogo.domain.models import TallaModel, ProductoTallaModel
from src.modules.catalogo.domain.ports import TallaPort, ProductoTallaPort
from src.modules.catalogo.infra.sizes.talla_table import TallaTable, ProductoTallaTable


def to_domain_talla(r: TallaTable) -> TallaModel:
    return TallaModel(
        talla_id=r.talla_id,
        nombre=r.nombre
    )


class TallaRepository(TallaPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all(self) -> list[TallaModel]:
        stmt = select(TallaTable)
        rows = self.db.execute(stmt).scalars().all()
        return [to_domain_talla(r) for r in rows]

    def get_by_id(self, talla_id: int) -> TallaModel | None:
        r = self.db.get_one(TallaTable, talla_id)
        return to_domain_talla(r) if r else None  # type: ignore[arg-type]

    def create(self, model: TallaModel) -> TallaModel:
        talla = TallaTable(
            nombre=model.nombre
        )
        self.db.add(talla)
        self.db.commit()
        self.db.refresh(talla)
        return to_domain_talla(talla)

    def update(self, talla_id: int, model: TallaModel) -> TallaModel | None:
        r = self.db.get_one(TallaTable, talla_id)
        if not r:
            return None
        r.nombre = model.nombre
        return to_domain_talla(r)  # type: ignore[arg-type]

    def delete(self, talla_id: int) -> None:
        r = self.db.get(TallaTable, talla_id)
        self.db.delete(r)
        self.db.commit()
        return


def to_domain_p_talla(r: ProductoTallaTable) -> ProductoTallaModel:
    return ProductoTallaModel(
        producto_talla_id=r.producto_talla_id,
        talla_id=r.talla_id,
        producto_id=r.producto_id
    )


class ProductoTallaRepository(ProductoTallaPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_by_producto(self, p_id: str) -> list[TallaModel]:
        stmt = (
            select(TallaTable)
            .join(ProductoTallaTable, TallaTable.talla_id == ProductoTallaTable.talla_id)
            .where(ProductoTallaTable.producto_id == p_id)
        )
        rows = self.db.execute(stmt).scalars().all()

        return [to_domain_talla(r) for r in rows]

    def get_by_id(self, p_talla_id: int) -> ProductoTallaModel:
        r = self.db.get(ProductoTallaTable, p_talla_id)
        return to_domain_p_talla(r) if r else None  # type: ignore[arg-type]

    def assign_to_producto(self, p_talla: ProductoTallaModel) -> ProductoTallaModel:
        assign = ProductoTallaTable(
            producto_id=p_talla.producto_id,
            talla_id=p_talla.talla_id
        )
        self.db.add(assign)
        self.db.commit()
        self.db.refresh(assign)
        return to_domain_p_talla(assign)

    def remove_from_producto(self, producto_id: str, talla_id: int) -> None:
        stmt = (select(ProductoTallaTable)
                .filter(ProductoTallaTable.producto_id == producto_id)
                .filter(ProductoTallaTable.talla_id == talla_id)
                )
        r = self.db.execute(stmt).scalar_one_or_none()
        self.db.delete(r)
        self.db.commit()
        return
