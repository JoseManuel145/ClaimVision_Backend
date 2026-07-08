"""Pruebas de perfil del ajustador (GET + PUT /api/v1/ajustador/perfil)."""
import pytest

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.ajustador.application.get_perfil_ajustador import GetPerfilAjustador
from src.modules.ajustador.application.actualizar_perfil_ajustador import ActualizarPerfilAjustador
from src.modules.ajustador.presentation import ajustador_dependencies as deps

from tests.fakes.ajustador import FakeAjustadorRepo, default_ajustador
from tests.fakes.auth import FakeAuthRepo, FakeUser

BASE = "/api/v1/ajustador"


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-aj", email="aj@demo.mx", rol="Ajustador", aseguradora_id="aseg-1"
    )
    auth_repo = FakeAuthRepo()
    auth_repo.create(FakeUser(
        usuario_id="user-aj", nombre="Juan", email="aj@demo.mx",
        password_hash="x", rol="Ajustador", aseguradora_id="aseg-1",
        telefono="555-0001",
    ))
    aj_repo = FakeAjustadorRepo({"user-aj": default_ajustador()}, auth_repo=auth_repo)

    app.dependency_overrides[deps.get_perfil_ajustador_service] = lambda: GetPerfilAjustador(aj_repo)
    app.dependency_overrides[deps.actualizar_perfil_ajustador_service] = lambda: ActualizarPerfilAjustador(aj_repo, auth_repo)
    return {"client": client, "aj_repo": aj_repo, "auth_repo": auth_repo}


def test_get_perfil(wired):
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["usuario_id"] == "user-aj"
    assert body["cedula_profesional"] == "CED-001"
    assert body["activo_para_servicio"] is True
    assert body["nombre"] == "Juan"
    assert body["email"] == "aj@demo.mx"
    assert body["telefono"] == "555-0001"


def test_put_perfil_updates_user(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={
        "nombre": "Juan Actualizado",
        "email": "juan.nuevo@demo.mx",
        "telefono": "555-9999",
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Juan Actualizado"
    assert body["email"] == "juan.nuevo@demo.mx"
    assert body["telefono"] == "555-9999"

    user = wired["auth_repo"].get_by_id("user-aj")
    assert user.nombre == "Juan Actualizado"
    assert user.email == "juan.nuevo@demo.mx"
    assert user.telefono == "555-9999"


def test_put_perfil_partial_update(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={"nombre": "Solo Nombre"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Solo Nombre"
    assert body["email"] == "aj@demo.mx"
    assert body["telefono"] == "555-0001"


def test_put_perfil_empty_body_no_changes(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Juan"
    assert body["email"] == "aj@demo.mx"
    assert body["telefono"] == "555-0001"


def test_perfil_rol_no_ajustador_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-otro", email="otro@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 403
