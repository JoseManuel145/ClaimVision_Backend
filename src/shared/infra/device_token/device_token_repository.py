from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.shared.domain.models_device_token import DeviceToken
from src.shared.domain.ports.device_token_port import DeviceTokenPort
from src.shared.infra.device_token.device_token_table import DeviceTokenTable


def _to_domain(row: DeviceTokenTable) -> DeviceToken:
    return DeviceToken(
        id=row.id,
        user_id=row.user_id,
        token=row.token,
        created_at=row.created_at,
    )


class DeviceTokenRepository(DeviceTokenPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user_id: str, token: str) -> None:
        stmt = select(DeviceTokenTable).where(DeviceTokenTable.token == token)
        existing = self.db.execute(stmt).scalars().first()
        if existing:
            return
        new_token = DeviceTokenTable(
            user_id=user_id,
            token=token,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(new_token)
        self.db.commit()

    def get_by_user(self, user_id: str) -> list[DeviceToken]:
        stmt = select(DeviceTokenTable).where(DeviceTokenTable.user_id == user_id)
        rows = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in rows]

    def get_all(self) -> list[DeviceToken]:
        stmt = select(DeviceTokenTable)
        rows = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in rows]

    def delete(self, token: str) -> None:
        stmt = select(DeviceTokenTable).where(DeviceTokenTable.token == token)
        row = self.db.execute(stmt).scalars().first()
        if not row:
            return
        self.db.delete(row)
        self.db.commit()
