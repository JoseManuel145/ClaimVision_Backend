from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.modules.aseguradora.infra.db.tables.ajustador_table import AjustadorTable
import uuid

def _parse_wkt(wkt_str: str | None) -> tuple[float, float] | None:
    if not wkt_str or not wkt_str.startswith("POINT("): return None
    try:
        parts = wkt_str.strip("POINT()").split()
        return (float(parts[1]), float(parts[0])) # lon, lat in WKT -> lat, lon in tuple
    except:
        return None

def _format_wkt(coords: tuple[float, float] | None) -> str | None:
    if not coords: return None
    return f"POINT({coords[1]} {coords[0]})"

def _to_domain(obj: AjustadorTable) -> AjustadorModel:
    return AjustadorModel(
        id=str(obj.id),
        usuario_id=str(obj.usuario_id),
        cedula_profesional=obj.cedula_profesional,
        geolocalizacion_actual=_parse_wkt(obj.geolocalizacion_actual),
        activo_para_servicio=obj.activo_para_servicio,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at
    )

class AjustadorRepository(AjustadorRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, ajustador: AjustadorModel) -> AjustadorModel:
        model = AjustadorTable(
            id=uuid.UUID(ajustador.id) if ajustador.id else uuid.uuid4(),
            usuario_id=uuid.UUID(ajustador.usuario_id) if ajustador.usuario_id else None,
            cedula_profesional=ajustador.cedula_profesional,
            geolocalizacion_actual=_format_wkt(ajustador.geolocalizacion_actual),
            activo_para_servicio=ajustador.activo_para_servicio,
            version=ajustador.version,
            created_at=ajustador.created_at,
            updated_at=ajustador.updated_at,
            deleted_at=ajustador.deleted_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, id: str) -> AjustadorModel | None:
        stmt = select(AjustadorTable).where(AjustadorTable.id == id, AjustadorTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def get_by_usuario_id(self, usuario_id: str) -> AjustadorModel | None:
        stmt = select(AjustadorTable).where(AjustadorTable.usuario_id == usuario_id, AjustadorTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def list_by_aseguradora(self, aseguradora_id: str, offset: int = 0, limit: int = 20, activo_para_servicio: bool | None = None) -> Tuple[List[AjustadorModel], int]:
        # Requiere JOIN con la tabla de usuarios para filtrar por aseguradora_id
        from src.modules.auth.infra.db.tables.user_table import UserTable
        
        base_query = select(AjustadorTable).join(UserTable, AjustadorTable.usuario_id == UserTable.id)\
            .where(UserTable.aseguradora_id == aseguradora_id, AjustadorTable.deleted_at.is_(None))
            
        count_query = select(func.count()).select_from(AjustadorTable).join(UserTable, AjustadorTable.usuario_id == UserTable.id)\
            .where(UserTable.aseguradora_id == aseguradora_id, AjustadorTable.deleted_at.is_(None))
            
        if activo_para_servicio is not None:
            base_query = base_query.where(AjustadorTable.activo_para_servicio == activo_para_servicio)
            count_query = count_query.where(AjustadorTable.activo_para_servicio == activo_para_servicio)
        
        total = self.db.execute(count_query).scalar() or 0
        
        stmt = base_query.order_by(AjustadorTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def update(self, ajustador: AjustadorModel) -> AjustadorModel:
        stmt = update(AjustadorTable).where(AjustadorTable.id == ajustador.id).values(
            cedula_profesional=ajustador.cedula_profesional,
            geolocalizacion_actual=_format_wkt(ajustador.geolocalizacion_actual),
            activo_para_servicio=ajustador.activo_para_servicio,
            version=ajustador.version,
            updated_at=ajustador.updated_at
        )
        self.db.execute(stmt)
        self.db.commit()
        return self.get_by_id(ajustador.id)

    def delete(self, id: str) -> None:
        stmt = update(AjustadorTable).where(AjustadorTable.id == id).values(
            deleted_at=func.now()
        )
        self.db.execute(stmt)
        self.db.commit()
