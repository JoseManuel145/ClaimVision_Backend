from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from src.modules.catalogo.domain.models import CategoriaModel
from src.modules.catalogo.domain.ports.categoria_port import CategoriaPort
from src.modules.catalogo.infra.category.category_table import CategoriaTable
from src.modules.catalogo.infra.sections.seccion_table import SeccionTable


def to_domain(r: CategoriaTable) -> CategoriaModel:
    return CategoriaModel(
        categoria_id=r.categoria_id,
        nombre=r.nombre,
        seccion_id=r.seccion_id,
        nombre_seccion=r.seccion.nombre if r.seccion else None
    )


class CategoriaRepository(CategoriaPort):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, categoria_id: int) -> CategoriaModel | None:
        stmt = select(CategoriaTable).options(joinedload(CategoriaTable.seccion)).filter_by(categoria_id=categoria_id)
        r = self.db.execute(stmt).scalars().first()
        return to_domain(r) if r else None

    def get_all(self) -> list[CategoriaModel]:
        stmt = select(CategoriaTable).options(joinedload(CategoriaTable.seccion)).order_by(CategoriaTable.nombre)
        results = self.db.execute(stmt).scalars().all()
        return [to_domain(r) for r in results]

    def get_all_by_seccion(self, seccion: int) -> list[CategoriaModel]:
        stmt = select(CategoriaTable).options(joinedload(CategoriaTable.seccion)).filter_by(seccion_id=seccion)
        results = self.db.execute(stmt).scalars().all()
        return [to_domain(r) for r in results]

    def create(self, categoria: CategoriaModel) -> CategoriaModel:
        nueva_categoria = CategoriaTable(
            nombre=categoria.nombre,
            seccion_id=categoria.seccion_id
        )
        self.db.add(nueva_categoria)
        self.db.commit()
        self.db.refresh(nueva_categoria)
        # Re-fetch to get the section name
        return self.get_by_id(nueva_categoria.categoria_id)  # type: ignore[return-value]

    def update(self, categoria_id: int, categoria: CategoriaModel) -> CategoriaModel | None:
        categoria_db = self.db.get(CategoriaTable, categoria_id)
        if not categoria_db:
            return None

        categoria_db.nombre = categoria.nombre
        categoria_db.seccion_id = categoria.seccion_id

        self.db.commit()
        self.db.refresh(categoria_db)
        return self.get_by_id(categoria_id)

    def delete(self, categoria_id: int) -> None:
        categoria_db = self.db.query(CategoriaTable).filter_by(categoria_id=categoria_id).first()
        if categoria_db:
            self.db.delete(categoria_db)
            self.db.commit()
