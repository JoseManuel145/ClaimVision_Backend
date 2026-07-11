from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.infra.db.tables.siniestro_table import SiniestroTable
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import NotFoundError
import uuid

def _to_domain(obj: SiniestroTable) -> SiniestroModel:
    return SiniestroModel(
        id=str(obj.id),
        aseguradora_id=str(obj.aseguradora_id) if obj.aseguradora_id else None,
        cliente_id=str(obj.cliente_id),
        ajustador_id=str(obj.ajustador_id) if obj.ajustador_id else None,
        taller_id=str(obj.taller_id) if obj.taller_id else None,
        vehiculo_id=str(obj.vehiculo_id) if obj.vehiculo_id else None,
        estatus=obj.estatus.value if hasattr(obj.estatus, 'value') else obj.estatus,
        vehiculo_marca=obj.vehiculo_marca,
        vehiculo_modelo=obj.vehiculo_modelo,
        vehiculo_anio=obj.vehiculo_anio,
        vehiculo_placas=obj.vehiculo_placas,
        vehiculo_vin=obj.vehiculo_vin,
        latitud_siniestro=float(obj.latitud_siniestro),
        longitud_siniestro=float(obj.longitud_siniestro),
        narracion_texto=obj.narracion_texto,
        narracion_audio_url=obj.narracion_audio_url,
        indicaciones_dano_interno=obj.indicaciones_dano_interno,
        fecha_siniestro=obj.fecha_siniestro,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at
    )

class SiniestroRepository(SiniestroRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, siniestro: SiniestroModel) -> SiniestroModel:
        model = SiniestroTable(
            id=uuid.UUID(siniestro.id) if siniestro.id else uuid.uuid4(),
            aseguradora_id=uuid.UUID(siniestro.aseguradora_id) if siniestro.aseguradora_id else None,
            cliente_id=uuid.UUID(siniestro.cliente_id) if siniestro.cliente_id else None,
            ajustador_id=uuid.UUID(siniestro.ajustador_id) if siniestro.ajustador_id else None,
            taller_id=uuid.UUID(siniestro.taller_id) if siniestro.taller_id else None,
            vehiculo_id=uuid.UUID(siniestro.vehiculo_id) if siniestro.vehiculo_id else None,
            estatus=siniestro.estatus,
            vehiculo_marca=siniestro.vehiculo_marca,
            vehiculo_modelo=siniestro.vehiculo_modelo,
            vehiculo_anio=siniestro.vehiculo_anio,
            vehiculo_placas=siniestro.vehiculo_placas,
            vehiculo_vin=siniestro.vehiculo_vin,
            latitud_siniestro=siniestro.latitud_siniestro,
            longitud_siniestro=siniestro.longitud_siniestro,
            narracion_texto=siniestro.narracion_texto,
            narracion_audio_url=siniestro.narracion_audio_url,
            indicaciones_dano_interno=siniestro.indicaciones_dano_interno,
            fecha_siniestro=siniestro.fecha_siniestro,
            version=siniestro.version,
            created_at=siniestro.created_at,
            updated_at=siniestro.updated_at,
            deleted_at=siniestro.deleted_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, id: str) -> SiniestroModel | None:
        stmt = select(SiniestroTable).where(SiniestroTable.id == id, SiniestroTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def list_by_aseguradora(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        estatus: str | None = None,
        ajustador_id: str | None = None,
        taller_id: str | None = None,
        q: str | None = None,
    ) -> Tuple[List[SiniestroModel], int]:
        aseg_uuid = uuid.UUID(aseguradora_id) if aseguradora_id else None
        if not aseg_uuid:
            return [], 0

        filtros = [SiniestroTable.aseguradora_id == aseg_uuid, SiniestroTable.deleted_at.is_(None)]
        if estatus is not None:
            filtros.append(SiniestroTable.estatus == estatus)
        if ajustador_id is not None:
            filtros.append(SiniestroTable.ajustador_id == uuid.UUID(ajustador_id))
        if taller_id is not None:
            filtros.append(SiniestroTable.taller_id == uuid.UUID(taller_id))
        if q:
            patron = f"%{q}%"
            filtros.append(
                SiniestroTable.vehiculo_placas.ilike(patron)
                | SiniestroTable.vehiculo_marca.ilike(patron)
                | SiniestroTable.vehiculo_modelo.ilike(patron)
            )

        base_query = select(SiniestroTable).where(*filtros)
        count_query = select(func.count()).select_from(SiniestroTable).where(*filtros)

        total = self.db.execute(count_query).scalar() or 0

        stmt = base_query.order_by(SiniestroTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def update(self, siniestro: SiniestroModel) -> SiniestroModel:
        obj = self.db.get(SiniestroTable, uuid.UUID(siniestro.id))
        if not obj:
            raise NotFoundError("Siniestro no encontrado")

        obj.ajustador_id = uuid.UUID(siniestro.ajustador_id) if siniestro.ajustador_id else None
        obj.taller_id = uuid.UUID(siniestro.taller_id) if siniestro.taller_id else None
        obj.vehiculo_id = uuid.UUID(siniestro.vehiculo_id) if siniestro.vehiculo_id else None
        obj.estatus = siniestro.estatus
        obj.vehiculo_marca = siniestro.vehiculo_marca
        obj.vehiculo_modelo = siniestro.vehiculo_modelo
        obj.vehiculo_anio = siniestro.vehiculo_anio
        obj.vehiculo_placas = siniestro.vehiculo_placas
        obj.vehiculo_vin = siniestro.vehiculo_vin
        obj.latitud_siniestro = siniestro.latitud_siniestro
        obj.longitud_siniestro = siniestro.longitud_siniestro
        obj.narracion_texto = siniestro.narracion_texto
        obj.narracion_audio_url = siniestro.narracion_audio_url
        obj.indicaciones_dano_interno = siniestro.indicaciones_dano_interno
        obj.updated_at = siniestro.updated_at

        self.db.commit()
        self.db.refresh(obj)
        return _to_domain(obj)

    def update_estatus(self, siniestro_id: str, estatus: str) -> SiniestroModel:
        stmt = update(SiniestroTable).where(SiniestroTable.id == siniestro_id).values(
            estatus=estatus,
            updated_at=func.now()
        )
        self.db.execute(stmt)
        self.db.commit()
        return self.get_by_id(siniestro_id)

    def list_by_cliente(self, cliente_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None) -> Tuple[List[SiniestroModel], int]:
        cliente_uuid = uuid.UUID(cliente_id) if cliente_id else None
        if not cliente_uuid:
            return [], 0
        base_query = select(SiniestroTable).where(SiniestroTable.cliente_id == cliente_uuid, SiniestroTable.deleted_at.is_(None))
        count_query = select(func.count()).select_from(SiniestroTable).where(SiniestroTable.cliente_id == cliente_uuid, SiniestroTable.deleted_at.is_(None))

        if estatus is not None:
            base_query = base_query.where(SiniestroTable.estatus == estatus)
            count_query = count_query.where(SiniestroTable.estatus == estatus)

        total = self.db.execute(count_query).scalar() or 0

        stmt = base_query.order_by(SiniestroTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def list_by_ajustador(self, ajustador_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None) -> Tuple[List[SiniestroModel], int]:
        ajustador_uuid = uuid.UUID(ajustador_id) if ajustador_id else None
        if not ajustador_uuid:
            return [], 0
        base_query = select(SiniestroTable).where(SiniestroTable.ajustador_id == ajustador_uuid, SiniestroTable.deleted_at.is_(None))
        count_query = select(func.count()).select_from(SiniestroTable).where(SiniestroTable.ajustador_id == ajustador_uuid, SiniestroTable.deleted_at.is_(None))
        
        if estatus is not None:
            base_query = base_query.where(SiniestroTable.estatus == estatus)
            count_query = count_query.where(SiniestroTable.estatus == estatus)

        total = self.db.execute(count_query).scalar() or 0
        
        stmt = base_query.order_by(SiniestroTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def list_by_taller(self, taller_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None) -> Tuple[List[SiniestroModel], int]:
        taller_uuid = uuid.UUID(taller_id) if taller_id else None
        if not taller_uuid:
            return [], 0
        base_query = select(SiniestroTable).where(SiniestroTable.taller_id == taller_uuid, SiniestroTable.deleted_at.is_(None))
        count_query = select(func.count()).select_from(SiniestroTable).where(SiniestroTable.taller_id == taller_uuid, SiniestroTable.deleted_at.is_(None))
        
        if estatus is not None:
            base_query = base_query.where(SiniestroTable.estatus == estatus)
            count_query = count_query.where(SiniestroTable.estatus == estatus)

        total = self.db.execute(count_query).scalar() or 0
        
        stmt = base_query.order_by(SiniestroTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total
