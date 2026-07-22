import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src.modules.cliente.domain.models import ClienteDocumento
from src.modules.cliente.domain.ports import ClienteDocumentoRepositoryPort
from src.modules.cliente.infra.db.tables.cliente_documento_table import ClienteDocumentoTable
from src.core.exceptions import NotFoundError

def _to_domain(obj: ClienteDocumentoTable) -> ClienteDocumento:
    return ClienteDocumento(
        id=str(obj.id),
        usuario_id=str(obj.usuario_id),
        identificacion_url=obj.identificacion_url,
        identificacion_tipo=obj.identificacion_tipo,
        identificacion_subido_en=obj.identificacion_subido_en,
        poliza_url=obj.poliza_url,
        poliza_tipo=obj.poliza_tipo,
        poliza_subido_en=obj.poliza_subido_en,
        created_at=obj.created_at,
        updated_at=obj.updated_at
    )

class ClienteDocumentoRepository(ClienteDocumentoRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def get_by_usuario_id(self, usuario_id: str) -> ClienteDocumento | None:
        usr_id = uuid.UUID(usuario_id) if isinstance(usuario_id, str) else usuario_id
        stmt = select(ClienteDocumentoTable).where(ClienteDocumentoTable.usuario_id == usr_id)
        r = self.db.execute(stmt).scalar_one_or_none()
        if not r:
            return None
        return _to_domain(r)

    def save(self, documento: ClienteDocumento) -> ClienteDocumento:
        doc_id = uuid.UUID(documento.id) if isinstance(documento.id, str) else documento.id
        usr_id = uuid.UUID(documento.usuario_id) if isinstance(documento.usuario_id, str) else documento.usuario_id
        model = ClienteDocumentoTable(
            id=doc_id,
            usuario_id=usr_id,
            identificacion_url=documento.identificacion_url,
            identificacion_tipo=documento.identificacion_tipo,
            identificacion_subido_en=documento.identificacion_subido_en,
            poliza_url=documento.poliza_url,
            poliza_tipo=documento.poliza_tipo,
            poliza_subido_en=documento.poliza_subido_en,
            created_at=documento.created_at or datetime.now(timezone.utc),
            updated_at=documento.updated_at or datetime.now(timezone.utc)
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def update(self, documento: ClienteDocumento) -> ClienteDocumento:
        doc_id = uuid.UUID(documento.id) if isinstance(documento.id, str) else documento.id
        stmt = (
            update(ClienteDocumentoTable)
            .where(ClienteDocumentoTable.id == doc_id)
            .values(
                identificacion_url=documento.identificacion_url,
                identificacion_tipo=documento.identificacion_tipo,
                identificacion_subido_en=documento.identificacion_subido_en,
                poliza_url=documento.poliza_url,
                poliza_tipo=documento.poliza_tipo,
                poliza_subido_en=documento.poliza_subido_en,
                updated_at=datetime.now(timezone.utc)
            )
        )
        result = self.db.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("Documento de cliente no encontrado")
        self.db.commit()
        return self.get_by_usuario_id(documento.usuario_id)
