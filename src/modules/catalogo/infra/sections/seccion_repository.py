from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.catalogo.domain.models import SeccionModel
from src.modules.catalogo.domain.ports import SeccionPort
from src.modules.catalogo.infra.sections.seccion_table import SeccionTable


def _to_domain(r: SeccionTable) -> SeccionModel:
    return SeccionModel(
        seccion_id=r.seccion_id,
        nombre=r.nombre,
    )

class SeccionRepository(SeccionPort):
    def __init__(self, session: Session):
        self.db = session

    def get_seccion_by_id(self, seccion_id: int) -> SeccionModel | None:
        r = self.db.get(SeccionTable, seccion_id)
        return _to_domain(r) if r else None # type: ignore[arg-type]

    def get_secciones(self) -> list[SeccionModel]:
        stmt = select(SeccionTable).order_by(SeccionTable.nombre)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results]

    def create_seccion(self, seccion: SeccionModel) -> SeccionModel:
        new_seccion = SeccionTable(nombre=seccion.nombre)
        self.db.add(new_seccion)
        self.db.commit()
        self.db.refresh(new_seccion)
        return _to_domain(new_seccion)

    def update_seccion(self, seccion_id: int, seccion: SeccionModel) -> SeccionModel | None:
        db_seccion = self.db.get(SeccionTable, seccion_id)
        if not db_seccion:
            return None
        db_seccion.nombre = seccion.nombre
        self.db.commit()
        self.db.refresh(db_seccion)
        return _to_domain(db_seccion) # type: ignore[arg-type]

    def delete_seccion(self, seccion_id: int) -> None:
        db_seccion = self.db.get(SeccionTable, seccion_id)

        if db_seccion:
            self.db.delete(db_seccion)
            self.db.commit()
