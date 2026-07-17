from typing import Protocol, Any


class MessagingPort(Protocol):
    def send(self, token: str, title: str, body: str, data: dict[str, Any] | None = None) -> str: ...
