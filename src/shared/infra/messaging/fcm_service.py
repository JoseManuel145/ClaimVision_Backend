from typing import Any
from src.shared.domain.ports.messaging_port import MessagingPort
from src.shared.infra.messaging.fcm_client import get_messaging
from src.core.logging import get_logger

logger = get_logger("fcm")


class FCMService(MessagingPort):
    def send(self, token: str, title: str, body: str, data: dict[str, Any] | None = None) -> str:
        messaging = get_messaging()

        message = messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
        )

        return messaging.send(message)
