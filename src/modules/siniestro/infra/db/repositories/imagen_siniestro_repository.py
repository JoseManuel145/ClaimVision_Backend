from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.ports.imagen_siniestro_repository_port import ImagenSiniestroRepositoryPort
from src.modules.siniestro.infra.db.tables.imagen_siniestro_table import ImagenSiniestroTable
import uuid

def _to_domain(obj: ImagenSiniestroTable) -> ImagenSiniestroModel:
    return ImagenSiniestroModel(
        id=str(obj.id),
        siniestro_id=str(obj.siniestro_id),
        imagen_url=obj.imagen_url,
        es_calidad_valida=obj.es_calidad_valida,
        metadatos_json=obj.metadatos_json,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at
    )

class ImagenSiniestroRepository(ImagenSiniestroRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, imagen: ImagenSiniestroModel) -> ImagenSiniestroModel:
        model = ImagenSiniestroTable(
            id=uuid.UUID(imagen.id) if imagen.id else uuid.uuid4(),
            siniestro_id=uuid.UUID(imagen.siniestro_id) if imagen.siniestro_id else None,
            imagen_url=imagen.imagen_url,
            es_calidad_valida=imagen.es_calidad_valida,
            metadatos_json=imagen.metadatos_json,
            version=imagen.version,
            created_at=imagen.created_at,
            updated_at=imagen.updated_at,
            deleted_at=imagen.deleted_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_siniestro_id(self, siniestro_id: str) -> List[ImagenSiniestroModel]:
        stmt = select(ImagenSiniestroTable).where(
            ImagenSiniestroTable.siniestro_id == siniestro_id, 
            ImagenSiniestroTable.deleted_at.is_(None)
        ).order_by(ImagenSiniestroTable.created_at.desc())
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results]
