from src.shared.domain.ports.device_token_port import DeviceTokenPort


class RegisterDeviceToken:
    def __init__(self, token_repo: DeviceTokenPort):
        self.token_repo = token_repo

    def execute(self, user_id: str, token: str) -> None:
        self.token_repo.save(user_id, token)
