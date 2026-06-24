import uuid
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from src.modules.admin.domain.models import AseguradoraTenant
from src.modules.admin.domain.ports import AseguradoraRepositoryPort
from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable
from src.core.exceptions import NotFoundError

def _to_domain(obj: AseguradoraTable) -> AseguradoraTenant:
    return AseguradoraTenant(
        id=str(obj.id),
        nombre=obj.nombre,
        rfc=obj.rfc,
        dominio_correo=obj.dominio_correo,
        plan_suscripcion=obj.plan_suscripcion,
        limite_peritajes_mes=obj.limite_peritajes_mes,
        peritajes_consumidos_mes=obj.peritajes_consumidos_mes,
        estatus_comercial=obj.estatus_comercial,
        contacto_legal_email=obj.contacto_legal_email,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at
    )

class AseguradoraRepository(AseguradoraRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, aseguradora: AseguradoraTenant) -> AseguradoraTenant:
        model = AseguradoraTable(
            id=aseguradora.id or uuid.uuid4(),
            nombre=aseguradora.nombre,
            rfc=aseguradora.rfc,
            dominio_correo=aseguradora.dominio_correo,
            plan_suscripcion=aseguradora.plan_suscripcion,
            limite_peritajes_mes=aseguradora.limite_peritajes_mes,
            peritajes_consumidos_mes=aseguradora.peritajes_consumidos_mes,
            estatus_comercial=aseguradora.estatus_comercial,
            contacto_legal_email=aseguradora.contacto_legal_email,
            version=aseguradora.version,
            created_at=aseguradora.created_at,
            updated_at=aseguradora.updated_at,
            deleted_at=aseguradora.deleted_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, id: str) -> AseguradoraTenant | None:
        stmt = select(AseguradoraTable).where(AseguradoraTable.id == id)
        r = self.db.execute(stmt).scalar_one_or_none()
        if not r:
            return None
        return _to_domain(r)

    def list_all(self, offset: int = 0, limit: int = 20, include_deleted: bool = False) -> Tuple[List[AseguradoraTenant], int]:
        base = select(AseguradoraTable)
        count_stmt = select(func.count()).select_from(AseguradoraTable)

        if not include_deleted:
            base = base.where(AseguradoraTable.deleted_at.is_(None))
            count_stmt = count_stmt.where(AseguradoraTable.deleted_at.is_(None))

        total = self.db.execute(count_stmt).scalar() or 0
        stmt = base.order_by(AseguradoraTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def update(self, aseguradora: AseguradoraTenant) -> AseguradoraTenant:
        stmt = (
            update(AseguradoraTable)
            .where(AseguradoraTable.id == aseguradora.id)
            .values(
                nombre=aseguradora.nombre,
                rfc=aseguradora.rfc,
                dominio_correo=aseguradora.dominio_correo,
                plan_suscripcion=aseguradora.plan_suscripcion,
                limite_peritajes_mes=aseguradora.limite_peritajes_mes,
                peritajes_consumidos_mes=aseguradora.peritajes_consumidos_mes,
                estatus_comercial=aseguradora.estatus_comercial,
                contacto_legal_email=aseguradora.contacto_legal_email,
                version=aseguradora.version,
                updated_at=aseguradora.updated_at,
                deleted_at=aseguradora.deleted_at
            )
        )
        result = self.db.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("Aseguradora no encontrada")
        self.db.commit()
        return self.get_by_id(aseguradora.id)
