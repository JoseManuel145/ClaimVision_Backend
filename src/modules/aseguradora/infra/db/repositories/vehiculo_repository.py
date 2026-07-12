from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel
from src.modules.aseguradora.domain.ports.vehiculo_repository_port import VehiculoRepositoryPort
from src.modules.aseguradora.infra.db.tables.vehiculo_table import VehiculoTable
from src.core.exceptions import NotFoundError
import uuid

def _to_domain(obj: VehiculoTable) -> VehiculoModel:
    return VehiculoModel(
        id=str(obj.id),
        aseguradora_id=str(obj.aseguradora_id),
        cliente_id=str(obj.cliente_id),
        marca=obj.marca,
        modelo=obj.modelo,
        anio=obj.anio,
        placas=obj.placas,
        vin=obj.vin,
        color=obj.color,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at,
    )

class VehiculoRepository(VehiculoRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, vehiculo: VehiculoModel) -> VehiculoModel:
        model = VehiculoTable(
            id=uuid.UUID(vehiculo.id) if vehiculo.id else uuid.uuid4(),
            aseguradora_id=uuid.UUID(vehiculo.aseguradora_id) if vehiculo.aseguradora_id else None,
            cliente_id=uuid.UUID(vehiculo.cliente_id) if vehiculo.cliente_id else None,
            marca=vehiculo.marca,
            modelo=vehiculo.modelo,
            anio=vehiculo.anio,
            placas=vehiculo.placas,
            vin=vehiculo.vin,
            color=vehiculo.color,
            version=vehiculo.version,
            created_at=vehiculo.created_at,
            updated_at=vehiculo.updated_at,
            deleted_at=vehiculo.deleted_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, id: str) -> VehiculoModel | None:
        stmt = select(VehiculoTable).where(VehiculoTable.id == id, VehiculoTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def list_by_aseguradora(self, aseguradora_id: str, offset: int = 0, limit: int = 20, cliente_id: str | None = None) -> Tuple[List[VehiculoModel], int]:
        if not aseguradora_id:
            return [], 0
        aseg_uuid = uuid.UUID(aseguradora_id)
        base_filter = [VehiculoTable.aseguradora_id == aseg_uuid, VehiculoTable.deleted_at.is_(None)]
        if cliente_id:
            base_filter.append(VehiculoTable.cliente_id == uuid.UUID(cliente_id))

        count_stmt = select(func.count()).select_from(VehiculoTable).where(*base_filter)
        total = self.db.execute(count_stmt).scalar() or 0

        stmt = select(VehiculoTable).where(*base_filter).order_by(VehiculoTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def list_by_cliente(self, cliente_id: str, offset: int = 0, limit: int = 20) -> Tuple[List[VehiculoModel], int]:
        if not cliente_id:
            return [], 0
        cliente_uuid = uuid.UUID(cliente_id)
        base_filter = [VehiculoTable.cliente_id == cliente_uuid, VehiculoTable.deleted_at.is_(None)]

        count_stmt = select(func.count()).select_from(VehiculoTable).where(*base_filter)
        total = self.db.execute(count_stmt).scalar() or 0

        stmt = select(VehiculoTable).where(*base_filter).order_by(VehiculoTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def update(self, vehiculo: VehiculoModel) -> VehiculoModel:
        obj = self.db.get(VehiculoTable, uuid.UUID(vehiculo.id))
        if not obj:
            raise NotFoundError("Vehiculo no encontrado")

        obj.marca = vehiculo.marca
        obj.modelo = vehiculo.modelo
        obj.anio = vehiculo.anio
        obj.placas = vehiculo.placas
        obj.vin = vehiculo.vin
        obj.color = vehiculo.color
        obj.updated_at = vehiculo.updated_at

        self.db.commit()
        self.db.refresh(obj)
        return _to_domain(obj)

    def delete(self, id: str) -> None:
        stmt = update(VehiculoTable).where(VehiculoTable.id == id).values(
            deleted_at=func.now(),
        )
        self.db.execute(stmt)
        self.db.commit()
