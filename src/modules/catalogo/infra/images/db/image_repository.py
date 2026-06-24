from sqlalchemy import select
from sqlalchemy.orm import Session
from src.modules.catalogo.domain.models import ImagenModel
from src.modules.catalogo.domain.ports import ImagePort
from src.modules.catalogo.infra.images.db.image_table import ImagenTable

def _to_domain(r: ImagenTable) -> ImagenModel:
    return ImagenModel(
        imagen_id=r.imagen_id,
        path=r.path,
        orden=r.orden
    )

class ImageRepository(ImagePort):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, imagen: ImagenModel) -> ImagenModel:
        nueva_imagen = ImagenTable(
            path=imagen.path,
            orden=imagen.orden
        )
        self.db_session.add(nueva_imagen)
        self.db_session.commit()
        self.db_session.refresh(nueva_imagen)
        return _to_domain(nueva_imagen)

    def get_by_id(self, imagen_id: int) -> ImagenModel | None:
        stmt = select(ImagenTable).where(ImagenTable.imagen_id == imagen_id)
        r = self.db_session.execute(stmt).scalar_one_or_none()
        if r is None:
            return None
        return _to_domain(r)

    def delete(self, imagen_id: int) -> None:
        stmt = select(ImagenTable).where(ImagenTable.imagen_id == imagen_id)
        r = self.db_session.execute(stmt).scalar_one_or_none()
        if r is None:
            return None
        self.db_session.delete(r)
        self.db_session.commit()
        return None
