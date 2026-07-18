from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.shared.infra.messaging.fcm_service import FCMService
from src.shared.infra.messaging.siniestro_notifier import SiniestroNotifier
from src.shared.infra.device_token.device_token_repository import DeviceTokenRepository


def get_siniestro_notifier(session: Session = Depends(get_session)) -> SiniestroNotifier:
    return SiniestroNotifier(
        messaging_service=FCMService(),
        token_repo=DeviceTokenRepository(session),
    )
