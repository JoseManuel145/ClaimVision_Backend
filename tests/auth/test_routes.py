"""Pruebas de Auth v1 (`/api/v1/auth/...`) — registro, login, recovery, consentimiento."""
import pytest

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.auth.application.register_user import RegisterUser
from src.modules.auth.application.login_user import LoginUser
from src.modules.auth.application.generate_code import GenerateRecoveryCode
from src.modules.auth.application.send_recovery_code import SendRecoveryCode
from src.modules.auth.application.verify_code import VerifyRecoveryCode
from src.modules.auth.application.reset_password import ResetPassword
from src.modules.auth.application.verify_user import VerifyUser
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.auth.presentation import dependencies as deps

from tests.fakes.auth import (
    FakeAuthRepo,
    FakePasswordService,
    FakeTokenService,
    FakeRecoveryRepo,
    FakeEmailService,
    FakeRateLimitRepo,
    FakeUser,
)
from tests.fakes.cliente import FakeClienteRepo, default_cliente_profile

BASE = "/api/v1/auth"


@pytest.fixture
def wired(client):
    auth_repo = FakeAuthRepo()
    pw_svc = FakePasswordService()
    token_svc = FakeTokenService()
    recovery_repo = FakeRecoveryRepo()
    email_svc = FakeEmailService()
    rate_limit = FakeRateLimitRepo()

    app.dependency_overrides[deps.register_user_service] = lambda: RegisterUser(auth_repo, pw_svc, token_svc)
    app.dependency_overrides[deps.login_user_service] = lambda: LoginUser(auth_repo, pw_svc, token_svc, rate_limit)
    app.dependency_overrides[deps.generate_recovery_code_service] = lambda: GenerateRecoveryCode(recovery_repo, auth_repo)
    app.dependency_overrides[deps.send_recovery_code_service] = lambda: SendRecoveryCode(email_svc)
    app.dependency_overrides[deps.verify_recovery_code_service] = lambda: VerifyRecoveryCode(recovery_repo)
    app.dependency_overrides[deps.reset_password_service] = lambda: ResetPassword(auth_repo, pw_svc)
    app.dependency_overrides[deps.verify_user_service] = lambda: VerifyUser(auth_repo)

    cli_repo = FakeClienteRepo(default_cliente_profile())
    auth_repo.create(FakeUser(usuario_id="user-1", nombre="Test", email="test@x.mx",
                              password_hash="x", rol="Cliente", aseguradora_id="aseg-1"))
    app.dependency_overrides[deps.confirm_consent_service] = lambda: ConfirmConsent(cli_repo, auth_repo)

    return {"client": client, "auth_repo": auth_repo, "recovery_repo": recovery_repo, "rate_limit": rate_limit}


REGISTER_DATA = {"nombre": "Juan Pérez", "email": "juan@claimvision.mx", "password": "SecurePass1"}


def test_register_crea_usuario_y_retorna_token(wired):
    r = wired["client"].post(f"{BASE}/register", json=REGISTER_DATA)
    assert r.status_code == 201, r.text
    body = r.json()
    assert "token" in body
    assert body["email"] == "juan@claimvision.mx"
    assert body["rol"] == "Cliente"


def test_register_email_duplicado_rechazado(wired):
    wired["client"].post(f"{BASE}/register", json=REGISTER_DATA)
    import pytest
    with pytest.raises(Exception) as exc_info:
        wired["client"].post(f"{BASE}/register", json=REGISTER_DATA)
    assert "already registered" in str(exc_info.value) or "duplicate" in str(exc_info.value).lower()


def test_login_exitoso(wired):
    wired["client"].post(f"{BASE}/register", json=REGISTER_DATA)
    r = wired["client"].post(f"{BASE}/login", json={"email": "juan@claimvision.mx", "password": "SecurePass1"})
    assert r.status_code == 200, r.text
    assert "token" in r.json()


def test_login_credenciales_invalidas(wired):
    r = wired["client"].post(f"{BASE}/login", json={"email": "no@existe.mx", "password": "x"})
    assert r.status_code == 401, r.text


def test_login_cuenta_bloqueada_tras_5_intentos(wired):
    wired["client"].post(f"{BASE}/register", json=REGISTER_DATA)
    for _ in range(5):
        wired["client"].post(f"{BASE}/login", json={"email": "juan@claimvision.mx", "password": "wrong"})
    r = wired["client"].post(f"{BASE}/login", json={"email": "juan@claimvision.mx", "password": "wrong"})
    assert r.status_code == 401, r.text
    assert "bloqueada" in r.text.lower()


def test_login_cuenta_arco_bloqueada(wired):
    wired["auth_repo"].create(FakeUser(
        usuario_id="user-blocked", nombre="Bloqueado", email="bloq@x.mx",
        password_hash="hashed_p", rol="Cliente", estado="Bloqueado_ARCO",
    ))
    r = wired["client"].post(f"{BASE}/login", json={"email": "bloq@x.mx", "password": "p"})
    assert r.status_code == 403, r.text


def test_me_autenticado_devuelve_usuario(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u1", email="me@x.mx", rol="Ajustador", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/me")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["email"] == "me@x.mx"



def test_me_sin_token_401(wired):
    app.dependency_overrides[get_current_user] = lambda: (_ for _ in ()).throw(
        __import__('fastapi').HTTPException(status_code=401)
    )
    r = wired["client"].get(f"{BASE}/me")
    assert r.status_code == 401


def test_recovery_request(wired):
    wired["auth_repo"].create(FakeUser(
        usuario_id="u-rec", nombre="Rec", email="rec@x.mx",
        password_hash="x", rol="Cliente",
    ))
    r = wired["client"].post(f"{BASE}/recovery/request", params={"email": "rec@x.mx"})
    assert r.status_code == 200, r.text
    assert len(r.json()) == 2


def test_recovery_verify(wired):
    wired["auth_repo"].create(FakeUser(
        usuario_id="u-vrf", nombre="Vrf", email="vrf@x.mx",
        password_hash="x", rol="Cliente",
    ))
    from src.modules.auth.domain.models import RecoveryCode
    from datetime import datetime, timedelta, timezone
    wired["recovery_repo"].save(RecoveryCode(
        id=None, usuario_id="u-vrf", code="123456",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    ))
    r = wired["client"].post(f"{BASE}/recovery/verify", params={"usuario_id": "u-vrf", "code": "123456"})
    assert r.status_code == 200, r.text


def test_recovery_reset_password(wired):
    wired["auth_repo"].create(FakeUser(
        usuario_id="u-rst", nombre="Rst", email="rst@x.mx",
        password_hash="hashed_old", rol="Cliente",
    ))
    r = wired["client"].post(f"{BASE}/recovery/reset", params={"usuario_id": "u-rst", "new_password": "NewPass1"})
    assert r.status_code == 200, r.text
    assert wired["auth_repo"].get_by_id("u-rst").password_hash == "hashed_NewPass1"


def test_consentimiento(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-1", email="cons@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].post(f"{BASE}/consentimiento", json={
        "aviso_privacidad": True,
        "biometria": True,
        "transferencia_talleres": False,
    })
    assert r.status_code == 200, r.text
