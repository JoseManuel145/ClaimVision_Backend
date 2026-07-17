from dataclasses import dataclass
from datetime import datetime


@dataclass
class DeviceToken:
    id: int | None
    user_id: str
    token: str
    created_at: datetime
