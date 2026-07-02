"""
Bootstrap de pruebas. No requiere base de datos ni servicios externos: se
inyectan variables de entorno dummy antes de importar la app y los casos de uso
se cablean con repositorios en memoria vía `app.dependency_overrides`.
"""
import base64
import os

os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SUPABASE_URL", "http://localhost")
os.environ.setdefault("SUPABASE_KEY", "dummy")
os.environ.setdefault("SUPABASE_BUCKET_IMG", "imagenes")
os.environ.setdefault("SUPABASE_BUCKET_PDF", "pdfs")
os.environ.setdefault("MAIL_USERNAME", "test@claimvision.mx")
os.environ.setdefault("MAIL_PASSWORD", "dummy")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("TIME_MINUTES", "60")
os.environ.setdefault("BCRYPT_ROUNDS", "12")
os.environ.setdefault("ENCRYPTION_KEY", base64.b64encode(b"0" * 32).decode())
os.environ.setdefault("OCR_API_URL", "http://localhost/ocr")
os.environ.setdefault("LOG_LEVEL", "WARNING")
os.environ.setdefault("ORIGINS", '["*"]')
os.environ.setdefault("FIREBASE_CREDENTIALS_PATH", "none")

import pytest
from starlette.testclient import TestClient

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser


class NoopAudit:
    def record(self, *args, **kwargs) -> None:
        return None


def make_user(usuario_id="user-1", email="test@demo.mx", rol="Cliente", aseguradora_id="aseg-1") -> AuthenticatedUser:
    return AuthenticatedUser(
        usuario_id=usuario_id,
        email=email,
        rol=rol,
        aseguradora_id=aseguradora_id,
    )


@pytest.fixture
def client():
    from src.shared.audit.audit_logger import get_audit_logger

    app.dependency_overrides[get_current_user] = make_user
    app.dependency_overrides[get_audit_logger] = lambda: NoopAudit()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
