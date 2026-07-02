"""
Bootstrap de pruebas. No requiere base de datos ni servicios externos: se
inyectan variables de entorno dummy antes de importar la app y los casos de uso
se cablean con repositorios en memoria vía `app.dependency_overrides`.
"""
import base64
import os

# --- Variables de entorno mínimas para que `Settings()` cargue (no hay .env en CI) ---
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

import pytest  # noqa: E402
from starlette.testclient import TestClient  # noqa: E402

from src.main import app  # noqa: E402
from src.core.security import get_current_user  # noqa: E402
from src.modules.auth.domain.models import AuthenticatedUser  # noqa: E402


class NoopAudit:
    """AuditLogger de pruebas: no escribe nada."""

    def record(self, *args, **kwargs) -> None:
        return None


def make_cliente_user() -> AuthenticatedUser:
    return AuthenticatedUser(
        usuario_id="user-1",
        email="cliente@demo.mx",
        rol="Cliente",
        aseguradora_id="aseg-1",
    )


@pytest.fixture
def client():
    """TestClient con autenticación y auditoría neutralizadas por defecto."""
    from src.shared.audit.audit_logger import get_audit_logger

    app.dependency_overrides[get_current_user] = make_cliente_user
    app.dependency_overrides[get_audit_logger] = lambda: NoopAudit()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
