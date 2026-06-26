import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.infra.db.tables.cotizacion_table import CotizacionTallerTable

def _to_domain(r: CotizacionTallerTable) -> CotizacionTallerModel:
    return CotizacionTallerModel(
        id=str(r.id),
        siniestro_id=str(r.siniestro_id),
        taller_id=str(r.taller_id),
        monto_mano_obra=r.monto_mano_obra,
        monto_refacciones=r.monto_refacciones,
        monto_total=r.monto_total,
        desglose_pdf_url=r.desglose_pdf_url,
        estatus=r.estatus.value if r.estatus else "Pendiente_Aprobacion",
        observaciones_tecnicas=r.observaciones_tecnicas,
        version=r.version,
        created_at=r.created_at,
        updated_at=r.updated_at,
        deleted_at=r.deleted_at
    )

class CotizacionRepository(CotizacionRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, cotizacion: CotizacionTallerModel) -> CotizacionTallerModel:
        if not cotizacion.siniestro_id:
            raise ValueError("siniestro_id es requerido")

        siniestro_uuid = uuid.UUID(cotizacion.siniestro_id)
        stmt = select(CotizacionTallerTable).where(CotizacionTallerTable.siniestro_id == siniestro_uuid)
        existing = self.db.execute(stmt).scalars().first()

        if existing:
            existing.taller_id = uuid.UUID(cotizacion.taller_id) if cotizacion.taller_id else None
            existing.monto_mano_obra = cotizacion.monto_mano_obra
            existing.monto_refacciones = cotizacion.monto_refacciones
            existing.monto_total = cotizacion.monto_total
            existing.desglose_pdf_url = cotizacion.desglose_pdf_url
            existing.estatus = cotizacion.estatus
            existing.observaciones_tecnicas = cotizacion.observaciones_tecnicas
            existing.version += 1
            self.db.commit()
            self.db.refresh(existing)
            return _to_domain(existing)
        else:
            new_cot = CotizacionTallerTable(
                siniestro_id=uuid.UUID(cotizacion.siniestro_id) if cotizacion.siniestro_id else None,
                taller_id=uuid.UUID(cotizacion.taller_id) if cotizacion.taller_id else None,
                monto_mano_obra=cotizacion.monto_mano_obra,
                monto_refacciones=cotizacion.monto_refacciones,
                monto_total=cotizacion.monto_total,
                desglose_pdf_url=cotizacion.desglose_pdf_url,
                estatus=cotizacion.estatus,
                observaciones_tecnicas=cotizacion.observaciones_tecnicas
            )
            self.db.add(new_cot)
            self.db.commit()
            self.db.refresh(new_cot)
            return _to_domain(new_cot)

    def get_by_siniestro(self, siniestro_id: str) -> Optional[CotizacionTallerModel]:
        if not siniestro_id:
            return None
        stmt = select(CotizacionTallerTable).where(CotizacionTallerTable.siniestro_id == uuid.UUID(siniestro_id), CotizacionTallerTable.deleted_at.is_(None))
        result = self.db.execute(stmt).scalars().first()
        if not result:
            return None
        return _to_domain(result)

    def update_estatus(self, id: str, estatus: str) -> CotizacionTallerModel:
        if not id:
            raise ValueError("id es requerido")
        stmt = update(CotizacionTallerTable).where(CotizacionTallerTable.id == uuid.UUID(id)).values(
            estatus=estatus
        ).returning(CotizacionTallerTable)
        result = self.db.execute(stmt).scalars().first()
        self.db.commit()
        if not result:
            raise ValueError("Cotización no encontrada")
        return _to_domain(result)
