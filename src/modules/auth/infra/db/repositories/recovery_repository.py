import uuid
from src.modules.auth.infra.db.tables.recovery_code import RecoveryCodeTable
from src.modules.auth.domain.ports import RecoveryCodePort
from src.modules.auth.domain.models import RecoveryCode
from sqlalchemy.orm import Session
from sqlalchemy import select



def _to_domain(r: RecoveryCodeTable) -> RecoveryCode:
    return RecoveryCode(
        id=r.id,
        usuario_id=str(r.usuario_id),
        code=r.code,
        expires_at=r.expires_at,
    )


class RecoveryCodeService(RecoveryCodePort):
    def __init__(self, session: Session):
        self.session = session

    def save(self, code: RecoveryCode) -> RecoveryCode:
        code = RecoveryCodeTable(
            id=code.id,
            usuario_id=uuid.UUID(code.usuario_id) if code.usuario_id else None,
            code=code.code,
            expires_at=code.expires_at
        )
        self.session.add(code)
        self.session.commit()
        return _to_domain(code)

    def get_by_user_id(self, user_id: str) -> RecoveryCode | None:
        stmt = select(RecoveryCodeTable).where(RecoveryCodeTable.usuario_id == uuid.UUID(user_id))
        r = self.session.execute(stmt).scalar_one_or_none()
        if not r:
            return None
        return _to_domain(r)

    def delete_by_user_id(self, usuario_id: str):
        stmt = select(RecoveryCodeTable).where(
            RecoveryCodeTable.usuario_id == uuid.UUID(usuario_id)
        )
        r = self.session.execute(stmt).scalar_one_or_none()

        if r is not None:
            self.session.delete(r)
            self.session.commit()
