"""Pruebas de perfil del taller (GET + PUT /api/v1/taller/perfil)."""
import pytest
from datetime import datetime, timezone

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.taller.application.get_perfil_taller import GetPerfilTaller
from src.modules.taller.application.actualizar_perfil_taller import ActualizarPerfilTaller
from src.modules.taller.presentation import taller_v1_dependencies as deps

from tests.fakes.taller import FakePerfilTallerRepo
from tests.fakes.auth import FakeAuthRepo, FakeUser
from src.modules.aseguradora.domain.models.taller_model import TallerModel

BASE = "/api/v1/taller"


def _make_taller(id="taller-1", nombre="Taller Test", rfc="RFC123", direccion="Calle 123", telefono="555-1000"):
    return TallerModel(
        id=id,
        nombre_comercial=nombre,
        rfc=rfc,
        direccion_tecnica=direccion,
        telefono_contacto=telefono,
        version=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-t", email="taller@demo.mx", rol="Operador_Taller", aseguradora_id="aseg-1"
    )
    perfil = FakePerfilTallerRepo({"user-t": "taller-1"})

    taller_model = _make_taller()
    talleres = {"taller-1": taller_model}

    class FakeTallerRepo:
        def __init__(self):
            self.items = talleres
        def get_by_id(self, id):
            return self.items.get(id)
        def update(self, taller):
            self.items[taller.id] = taller
            return taller

    taller_repo = FakeTallerRepo()
    auth_repo = FakeAuthRepo()
    auth_repo.create(FakeUser(
        usuario_id="user-t", nombre="Operador", email="taller@demo.mx",
        password_hash="x", rol="Operador_Taller", aseguradora_id="aseg-1",
        telefono="555-2000",
    ))

    app.dependency_overrides[deps.get_perfil_taller_service] = lambda: GetPerfilTaller(perfil, taller_repo, auth_repo)
    app.dependency_overrides[deps.actualizar_perfil_taller_service] = lambda: ActualizarPerfilTaller(perfil, taller_repo, auth_repo)
    return {"client": client, "taller_repo": taller_repo, "auth_repo": auth_repo}


def test_get_perfil(wired):
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre_comercial"] == "Taller Test"
    assert body["rfc"] == "RFC123"
    assert body["direccion_tecnica"] == "Calle 123"
    assert body["telefono_contacto"] == "555-1000"
    assert body["nombre"] == "Operador"
    assert body["email"] == "taller@demo.mx"
    assert body["telefono"] == "555-2000"


def test_put_perfil_updates_taller_and_user(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={
        "nombre_comercial": "Taller Nuevo",
        "direccion_tecnica": "Av. Nueva 456",
        "telefono_contacto": "555-3000",
        "nombre": "Operador Nuevo",
        "email": "op.nuevo@taller.mx",
        "telefono": "555-4000",
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre_comercial"] == "Taller Nuevo"
    assert body["direccion_tecnica"] == "Av. Nueva 456"
    assert body["telefono_contacto"] == "555-3000"
    assert body["nombre"] == "Operador Nuevo"
    assert body["email"] == "op.nuevo@taller.mx"
    assert body["telefono"] == "555-4000"

    taller = wired["taller_repo"].get_by_id("taller-1")
    assert taller.nombre_comercial == "Taller Nuevo"
    assert taller.direccion_tecnica == "Av. Nueva 456"
    assert taller.telefono_contacto == "555-3000"

    user = wired["auth_repo"].get_by_id("user-t")
    assert user.nombre == "Operador Nuevo"
    assert user.email == "op.nuevo@taller.mx"
    assert user.telefono == "555-4000"


def test_put_perfil_partial_taller(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={"nombre_comercial": "Taller Parcial"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre_comercial"] == "Taller Parcial"
    assert body["rfc"] == "RFC123"
    assert body["nombre"] == "Operador"
    assert body["email"] == "taller@demo.mx"


def test_rol_no_taller_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-otro", email="otro@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 403
