import uuid
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel, DanoAjustadoManualModel
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.siniestro.infra.db.tables.peritaje_table import PeritajeAjustadorTable, DanosAjustadosManualTable

def _dano_to_domain(r: DanosAjustadosManualTable) -> DanoAjustadoManualModel:
    return DanoAjustadoManualModel(
        id=str(r.id),
        peritaje_ajustador_id=str(r.peritaje_ajustador_id),
        zona_vehiculo=r.zona_vehiculo,
        tipo=r.tipo.value if r.tipo else None,
        severidad=r.severidad.value if r.severidad else None,
        costo_real_reparacion=r.costo_real_reparacion,
        origen_cambio=r.origen_cambio,
        version=r.version,
        created_at=r.created_at,
        updated_at=r.updated_at,
        deleted_at=r.deleted_at
    )

def _peritaje_to_domain(r: PeritajeAjustadorTable) -> PeritajeAjustadorModel:
    return PeritajeAjustadorModel(
        id=str(r.id),
        siniestro_id=str(r.siniestro_id),
        ajustador_id=str(r.ajustador_id),
        costo_definitivo_ajustador=r.costo_definitivo_ajustador,
        firma_digital_ajustador=r.firma_digital_ajustador,
        observaciones_campo=r.observaciones_campo,
        danos=[_dano_to_domain(d) for d in r.danos] if r.danos else [],
        version=r.version,
        created_at=r.created_at,
        updated_at=r.updated_at,
        deleted_at=r.deleted_at
    )

class PeritajeAjustadorRepository(PeritajeAjustadorRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def guardar_peritaje(self, peritaje: PeritajeAjustadorModel) -> PeritajeAjustadorModel:
        if not peritaje.siniestro_id:
            raise ValueError("siniestro_id es requerido para guardar el peritaje")

        siniestro_uuid = uuid.UUID(peritaje.siniestro_id)
        stmt = select(PeritajeAjustadorTable).where(PeritajeAjustadorTable.siniestro_id == siniestro_uuid)
        existing = self.db.execute(stmt).scalars().first()

        if existing:
            existing.ajustador_id = uuid.UUID(peritaje.ajustador_id) if peritaje.ajustador_id else None
            existing.costo_definitivo_ajustador = peritaje.costo_definitivo_ajustador
            existing.firma_digital_ajustador = peritaje.firma_digital_ajustador
            existing.observaciones_campo = peritaje.observaciones_campo
            existing.version += 1
            
            # Clear existing danos and replace
            for d in existing.danos:
                self.db.delete(d)
            existing.danos = []
            self.db.flush()
            
            for d in peritaje.danos:
                new_dano = DanosAjustadosManualTable(
                    peritaje_ajustador_id=existing.id,
                    zona_vehiculo=d.zona_vehiculo,
                    tipo=d.tipo,
                    severidad=d.severidad,
                    costo_real_reparacion=d.costo_real_reparacion,
                    origen_cambio=d.origen_cambio
                )
                existing.danos.append(new_dano)
            
            self.db.commit()
            self.db.refresh(existing)
            return _peritaje_to_domain(existing)
        else:
            new_peritaje = PeritajeAjustadorTable(
                siniestro_id=uuid.UUID(peritaje.siniestro_id) if peritaje.siniestro_id else None,
                ajustador_id=uuid.UUID(peritaje.ajustador_id) if peritaje.ajustador_id else None,
                costo_definitivo_ajustador=peritaje.costo_definitivo_ajustador,
                firma_digital_ajustador=peritaje.firma_digital_ajustador,
                observaciones_campo=peritaje.observaciones_campo
            )
            self.db.add(new_peritaje)
            self.db.flush()
            
            for d in peritaje.danos:
                new_dano = DanosAjustadosManualTable(
                    peritaje_ajustador_id=new_peritaje.id,
                    zona_vehiculo=d.zona_vehiculo,
                    tipo=d.tipo,
                    severidad=d.severidad,
                    costo_real_reparacion=d.costo_real_reparacion,
                    origen_cambio=d.origen_cambio
                )
                new_peritaje.danos.append(new_dano)
                
            self.db.commit()
            self.db.refresh(new_peritaje)
            return _peritaje_to_domain(new_peritaje)

    def obtener_peritaje_por_siniestro(self, siniestro_id: str) -> Optional[PeritajeAjustadorModel]:
        if not siniestro_id:
            return None
        stmt = select(PeritajeAjustadorTable).where(
            PeritajeAjustadorTable.siniestro_id == uuid.UUID(siniestro_id),
            PeritajeAjustadorTable.deleted_at.is_(None)
        )
        result = self.db.execute(stmt).scalars().first()
        if not result:
            return None
        return _peritaje_to_domain(result)

    def obtener_por_id(self, peritaje_id: str) -> Optional[PeritajeAjustadorModel]:
        if not peritaje_id:
            return None
        stmt = select(PeritajeAjustadorTable).where(
            PeritajeAjustadorTable.id == uuid.UUID(peritaje_id),
            PeritajeAjustadorTable.deleted_at.is_(None)
        )
        result = self.db.execute(stmt).scalars().first()
        if not result:
            return None
        return _peritaje_to_domain(result)

    def get_by_siniestro(self, siniestro_id: str) -> Optional[PeritajeAjustadorModel]:
        # Alias usado por el módulo taller (get_expediente / presupuesto).
        return self.obtener_peritaje_por_siniestro(siniestro_id)
