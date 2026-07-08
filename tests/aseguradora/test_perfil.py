"""Pruebas de perfil de la aseguradora (GET + PUT /api/v1/aseguradora/perfil)."""
import pytest
from datetime import datetime, timezone

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.admin.domain.models import AseguradoraTenant
from src.modules.aseguradora.application.perfil.get_perfil_aseguradora import GetPerfilAseguradora
from src.modules.aseguradora.application.perfil.actualizar_perfil_aseguradora import ActualizarPerfilAseguradora
from src.modules.aseguradora.presentation.perfil import perfil_dependencies as deps

from tests.fakes.auth import FakeAuthRepo, FakeUser

BASE = "/api/v1/aseguradora/perfil"


def _make_aseg(id="aseg-1", nombre="Aseguradora X", rfc="AXC123456789"):
    return AseguradoraTenant(
        id=id,
        nombre=nombre,
        rfc=rfc,
        dominio_correo="@asegx.mx",
        plan_suscripcion="Profesional",
        limite_peritajes_mes=100,
        peritajes_consumidos_mes=0,
        estatus_comercial="Activo",
        contacto_legal_email="legal@asegx.mx",
        version=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-op", email="op@asegx.mx", rol="Operador_Aseguradora", aseguradora_id="aseg-1"
    )
    aseg_model = _make_aseg()

    class FakeAseguradoraRepo:
        def __init__(self):
            self.items = {"aseg-1": aseg_model}
        def get_by_id(self, id):
            return self.items.get(id)
        def update(self, aseg):
            self.items[aseg.id] = aseg
            return self.get_by_id(aseg.id)

    aseg_repo = FakeAseguradoraRepo()
    auth_repo = FakeAuthRepo()
    auth_repo.create(FakeUser(
        usuario_id="user-op", nombre="Operador", email="op@asegx.mx",
        password_hash="x", rol="Operador_Aseguradora", aseguradora_id="aseg-1",
        telefono="555-0001",
    ))

    app.dependency_overrides[deps.get_perfil_aseguradora_service] = lambda: GetPerfilAseguradora(aseg_repo)
    app.dependency_overrides[deps.actualizar_perfil_aseguradora_service] = lambda: ActualizarPerfilAseguradora(aseg_repo, auth_repo)
    return {"client": client, "aseg_repo": aseg_repo, "auth_repo": auth_repo}


def test_get_perfil(wired):
    r = wired["client"].get(BASE)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Aseguradora X"
    assert body["rfc"] == "AXC123456789"
    assert body["plan_suscripcion"] == "Profesional"
    assert body["dominio_correo"] == "@asegx.mx"


def test_put_perfil_updates_aseguradora_and_operador(wired):
    r = wired["client"].put(BASE, json={
        "nombre": "Aseguradora Y",
        "rfc": "RFC999999999",
        "dominio_correo": "@asegy.mx",
        "contacto_legal_email": "legal@asegy.mx",
        "operador_nombre": "Operador Nuevo",
        "operador_email": "op.nuevo@asegy.mx",
        "operador_telefono": "555-9999",
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Aseguradora Y"
    assert body["rfc"] == "RFC999999999"
    assert body["dominio_correo"] == "@asegy.mx"
    assert body["contacto_legal_email"] == "legal@asegy.mx"

    aseg = wired["aseg_repo"].get_by_id("aseg-1")
    assert aseg.nombre == "Aseguradora Y"
    assert aseg.rfc == "RFC999999999"

    user = wired["auth_repo"].get_by_id("user-op")
    assert user.nombre == "Operador Nuevo"
    assert user.email == "op.nuevo@asegy.mx"
    assert user.telefono == "555-9999"


def test_put_perfil_partial_update_aseguradora(wired):
    r = wired["client"].put(BASE, json={"nombre": "Solo Nombre Aseguradora"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Solo Nombre Aseguradora"
    assert body["rfc"] == "AXC123456789"
    assert body["plan_suscripcion"] == "Profesional"


def test_put_perfil_partial_update_operador(wired):
    r = wired["client"].put(BASE, json={"operador_nombre": "Solo Operador"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Aseguradora X"

    user = wired["auth_repo"].get_by_id("user-op")
    assert user.nombre == "Solo Operador"


def test_rol_no_operador_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-otro", email="otro@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(BASE)
    assert r.status_code == 403
