"""Fakes del módulo Auth."""
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass

from src.shared.domain.models import Rol


@dataclass
class FakeUser:
    """Minimal User domain model para pruebas."""
    usuario_id: str
    nombre: str
    email: str
    password_hash: str
    rol: object
    aseguradora_id: Optional[str] = None
    estado: str = "Activo"
    created_at: datetime = None
    email_verificado: bool = False
    telefono: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.rol, str):
            from src.shared.domain.models import Rol
            self.rol = Rol(self.rol)
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


class FakePasswordService:
    def hash(self, password: str) -> str:
        return f"hashed_{password}"

    def verify(self, plain: str, hashed: str) -> bool:
        return f"hashed_{plain}" == hashed


class FakeTokenService:
    def generate(self, payload):
        from src.modules.auth.domain.models import TokenPayload
        return f"token_{payload.usuario_id}"

    def verify(self, token: str):
        from src.modules.auth.domain.models import TokenPayload
        return TokenPayload(usuario_id="user-1", email="test@x.mx", rol="Cliente", aseguradora_id="aseg-1")

    def create(self, usuario_id: str, email: str, rol: str, aseguradora_id: Optional[str]) -> str:
        return f"token_{usuario_id}"


class FakeAuthRepo:
    def __init__(self):
        self.users: dict[str, FakeUser] = {}

    def create(self, user: FakeUser) -> FakeUser:
        self.users[user.usuario_id] = user
        return user

    def get_by_email(self, email: str) -> FakeUser | None:
        for u in self.users.values():
            if u.email == email:
                return u
        return None

    def get_by_id(self, usuario_id: str) -> FakeUser | None:
        return self.users.get(usuario_id)

    def update_password(self, usuario_id: str, password_hash: str) -> None:
        if usuario_id in self.users:
            self.users[usuario_id].password_hash = password_hash

    def update_user_profile(self, usuario_id: str, nombre: str | None = None, email: str | None = None, telefono: str | None = None) -> None:
        user = self.users.get(usuario_id)
        if user:
            if nombre is not None:
                user.nombre = nombre
            if email is not None:
                user.email = email
            if telefono is not None:
                user.telefono = telefono

    def verify_user(self, usuario_id: str) -> None:
        if usuario_id in self.users:
            self.users[usuario_id].email_verificado = True


class FakeRecoveryRepo:
    def __init__(self):
        self.codes: dict[str, dict] = {}

    def save(self, code) -> None:
        self.codes[code.usuario_id] = {"code": code.code, "expires_at": code.expires_at}

    def get_by_user_id(self, usuario_id: str):
        data = self.codes.get(usuario_id)
        if not data:
            return None
        from src.modules.auth.domain.models import RecoveryCode
        return RecoveryCode(id=None, usuario_id=usuario_id, code=data["code"], expires_at=data["expires_at"])

    def delete_by_user_id(self, usuario_id: str) -> None:
        self.codes.pop(usuario_id, None)


class FakeEmailService:
    sent_codes: dict[str, str] = {}

    def send_code(self, email: str, code: str) -> dict:
        self.sent_codes[email] = code
        return {"email": email, "code": code}

    def send(self, to: str, subject: str, body: str) -> None:
        pass


class FakeRateLimitRepo:
    def __init__(self):
        self._attempts: dict[str, int] = {}
        self._blocked: set[str] = set()

    def record_failed_attempt(self, email: str) -> int:
        self._attempts[email] = self._attempts.get(email, 0) + 1
        if self._attempts[email] >= 5:
            self._blocked.add(email)
        return self._attempts[email]

    def is_blocked(self, email: str) -> bool:
        return email in self._blocked

    def reset_attempts(self, email: str) -> None:
        self._attempts.pop(email, None)
        self._blocked.discard(email)
