from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.modules.aseguradora.infra.db.tables.taller_table import TallerTable
from src.modules.aseguradora.infra.db.tables.convenio_table import ConvenioAseguradoraTallerTable
from datetime import datetime, timezone
import uuid

def _to_domain(obj: TallerTable) -> TallerModel:
    return TallerModel(
        id=str(obj.id),
        nombre_comercial=obj.nombre_comercial,
        rfc=obj.rfc,
        direccion_tecnica=obj.direccion_tecnica,
        telefono_contacto=obj.telefono_contacto,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at
    )

class TallerRepository(TallerRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, taller: TallerModel) -> TallerModel:
        model = TallerTable(
            id=uuid.UUID(taller.id) if taller.id else uuid.uuid4(),
            nombre_comercial=taller.nombre_comercial,
            rfc=taller.rfc,
            direccion_tecnica=taller.direccion_tecnica,
            telefono_contacto=taller.telefono_contacto,
            version=taller.version,
            created_at=taller.created_at,
            updated_at=taller.updated_at,
            deleted_at=taller.deleted_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, id: str) -> TallerModel | None:
        stmt = select(TallerTable).where(TallerTable.id == id, TallerTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def list_by_aseguradora(self, aseguradora_id: str, offset: int = 0, limit: int = 20) -> Tuple[List[TallerModel], int]:
        if not aseguradora_id:
            return [], 0
        aseg_uuid = uuid.UUID(aseguradora_id)
        base = select(TallerTable).join(ConvenioAseguradoraTallerTable, TallerTable.id == ConvenioAseguradoraTallerTable.taller_id)\
            .where(ConvenioAseguradoraTallerTable.aseguradora_id == aseg_uuid, TallerTable.deleted_at.is_(None), ConvenioAseguradoraTallerTable.deleted_at.is_(None))
        
        count_stmt = select(func.count()).select_from(TallerTable).join(ConvenioAseguradoraTallerTable, TallerTable.id == ConvenioAseguradoraTallerTable.taller_id)\
            .where(ConvenioAseguradoraTallerTable.aseguradora_id == aseg_uuid, TallerTable.deleted_at.is_(None), ConvenioAseguradoraTallerTable.deleted_at.is_(None))
        
        total = self.db.execute(count_stmt).scalar() or 0
        
        stmt = base.order_by(TallerTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def update(self, taller: TallerModel) -> TallerModel:
        stmt = update(TallerTable).where(TallerTable.id == taller.id).values(
            nombre_comercial=taller.nombre_comercial,
            rfc=taller.rfc,
            direccion_tecnica=taller.direccion_tecnica,
            telefono_contacto=taller.telefono_contacto,
            version=taller.version,
            updated_at=taller.updated_at
        )
        self.db.execute(stmt)
        self.db.commit()
        return self.get_by_id(taller.id)

    def delete(self, id: str) -> None:
        stmt = update(TallerTable).where(TallerTable.id == id).values(
            deleted_at=func.now()
        )
        self.db.execute(stmt)
        self.db.commit()

    def vincular_taller_aseguradora(self, taller_id: str, aseguradora_id: str) -> None:
        if not taller_id or not aseguradora_id:
            raise ValueError("taller_id y aseguradora_id son requeridos")
        model = ConvenioAseguradoraTallerTable(
            aseguradora_id=uuid.UUID(aseguradora_id),
            taller_id=uuid.UUID(taller_id),
            fecha_convenio=datetime.now(timezone.utc).date()
        )
        self.db.add(model)
        self.db.commit()

    def desvincular_taller_aseguradora(self, taller_id: str, aseguradora_id: str) -> None:
        stmt = update(ConvenioAseguradoraTallerTable).where(
            ConvenioAseguradoraTallerTable.taller_id == taller_id,
            ConvenioAseguradoraTallerTable.aseguradora_id == aseguradora_id
        ).values(deleted_at=func.now())
        self.db.execute(stmt)
        self.db.commit()
