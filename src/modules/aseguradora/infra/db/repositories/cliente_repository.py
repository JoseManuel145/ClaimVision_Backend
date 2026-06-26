from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel
from src.modules.aseguradora.domain.ports.cliente_repository_port import ClienteRepositoryPort
from src.modules.aseguradora.infra.db.tables.perfil_cliente_table import PerfilClienteTable
import uuid

def _to_domain(obj: PerfilClienteTable) -> ClienteModel:
    return ClienteModel(
        id=str(obj.id),
        usuario_id=str(obj.usuario_id),
        numero_poliza=obj.numero_poliza,
        vigencia_poliza=obj.vigencia_poliza,
        curp_rfc_cifrado=obj.curp_rfc_cifrado,
        consentimiento_aviso_privacidad=obj.consentimiento_aviso_privacidad,
        consentimiento_biometria=obj.consentimiento_biometria,
        autoriza_transferencia_talleres=obj.autoriza_transferencia_talleres,
        fecha_consentimiento=obj.fecha_consentimiento,
        version=obj.version,
        created_at=obj.created_at,
        updated_at=obj.updated_at,
        deleted_at=obj.deleted_at
    )

class ClienteRepository(ClienteRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, cliente: ClienteModel) -> ClienteModel:
        model = PerfilClienteTable(
            id=uuid.UUID(cliente.id) if cliente.id else uuid.uuid4(),
            usuario_id=uuid.UUID(cliente.usuario_id) if cliente.usuario_id else None,
            numero_poliza=cliente.numero_poliza,
            vigencia_poliza=cliente.vigencia_poliza,
            curp_rfc_cifrado=cliente.curp_rfc_cifrado,
            consentimiento_aviso_privacidad=cliente.consentimiento_aviso_privacidad,
            consentimiento_biometria=cliente.consentimiento_biometria,
            autoriza_transferencia_talleres=cliente.autoriza_transferencia_talleres,
            fecha_consentimiento=cliente.fecha_consentimiento,
            version=cliente.version,
            created_at=cliente.created_at,
            updated_at=cliente.updated_at,
            deleted_at=cliente.deleted_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_id(self, id: str) -> ClienteModel | None:
        stmt = select(PerfilClienteTable).where(PerfilClienteTable.id == id, PerfilClienteTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def get_by_usuario_id(self, usuario_id: str) -> ClienteModel | None:
        stmt = select(PerfilClienteTable).where(PerfilClienteTable.usuario_id == usuario_id, PerfilClienteTable.deleted_at.is_(None))
        r = self.db.execute(stmt).scalar_one_or_none()
        return _to_domain(r) if r else None

    def list_by_aseguradora(self, aseguradora_id: str, offset: int = 0, limit: int = 20) -> Tuple[List[ClienteModel], int]:
        from src.modules.auth.infra.db.tables.user_table import UserTable
        
        base = select(PerfilClienteTable).join(UserTable, PerfilClienteTable.usuario_id == UserTable.id)\
            .where(UserTable.aseguradora_id == aseguradora_id, PerfilClienteTable.deleted_at.is_(None))
        
        count_stmt = select(func.count()).select_from(PerfilClienteTable).join(UserTable, PerfilClienteTable.usuario_id == UserTable.id)\
            .where(UserTable.aseguradora_id == aseguradora_id, PerfilClienteTable.deleted_at.is_(None))
        
        total = self.db.execute(count_stmt).scalar() or 0
        
        stmt = base.order_by(PerfilClienteTable.created_at.desc()).offset(offset).limit(limit)
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total

    def update(self, cliente: ClienteModel) -> ClienteModel:
        stmt = update(PerfilClienteTable).where(PerfilClienteTable.id == cliente.id).values(
            numero_poliza=cliente.numero_poliza,
            vigencia_poliza=cliente.vigencia_poliza,
            curp_rfc_cifrado=cliente.curp_rfc_cifrado,
            consentimiento_aviso_privacidad=cliente.consentimiento_aviso_privacidad,
            consentimiento_biometria=cliente.consentimiento_biometria,
            autoriza_transferencia_talleres=cliente.autoriza_transferencia_talleres,
            fecha_consentimiento=cliente.fecha_consentimiento,
            version=cliente.version,
            updated_at=cliente.updated_at
        )
        self.db.execute(stmt)
        self.db.commit()
        return self.get_by_id(cliente.id)

    def delete(self, id: str) -> None:
        stmt = update(PerfilClienteTable).where(PerfilClienteTable.id == id).values(
            deleted_at=func.now()
        )
        self.db.execute(stmt)
        self.db.commit()
