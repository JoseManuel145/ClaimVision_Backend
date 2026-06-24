from sqlalchemy import select
from sqlalchemy.orm import Session
from src.modules.catalogo.domain.ports import ProductImagePort
from src.modules.catalogo.domain.models import ProductoImagenModel
from src.modules.catalogo.infra.images.db.image_table import ProductoImagenTable


def _to_domain(r: ProductoImagenTable) -> ProductoImagenModel:
    return ProductoImagenModel(
        producto_imagen_id=r.producto_imagen_id,
        producto_id=r.producto_id,
        imagen_id=r.imagen_id,
        es_principal=r.es_principal
    )

class ProductImageRepository(ProductImagePort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, r: ProductoImagenModel) -> ProductoImagenModel:
        nueva_asociacion = ProductoImagenTable(
            producto_id=r.producto_id,
            imagen_id=r.imagen_id,
            es_principal=r.es_principal
        )
        self.db_session.add(nueva_asociacion)
        self.db_session.commit()
        self.db_session.refresh(nueva_asociacion)
        return _to_domain(nueva_asociacion)

    def delete(self, producto_id: str, imagen_id: int) -> None:
        asociacion = self.db_session.query(ProductoImagenTable).filter_by(
            producto_id=producto_id,
            imagen_id=imagen_id
        ).first()
        if asociacion is None:
            return
        self.db_session.delete(asociacion)
        self.db_session.commit()

    def get_by_producto(self, producto_id: str) -> list[ProductoImagenModel]:
        stmt = select(ProductoImagenTable).filter_by(producto_id=producto_id)
        rows = self.db_session.execute(stmt).scalars()
        return [_to_domain(r) for r in rows]

    def delete_by_producto(self, producto_id: str) -> None:
        stmt = select(ProductoImagenTable).filter_by(producto_id=producto_id)
        rows = self.db_session.execute(stmt).scalars()
        for r in rows:
            self.db_session.delete(r)
        self.db_session.commit()
