"""Pruebas de Admin v1 (`/api/v1/admin/...`) — aseguradoras CRUD, ARCO, auditoría."""
import pytest
from datetime import datetime, timezone

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser

from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.actualizar_aseguradora import ActualizarAseguradoraUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.crear_operador_aseguradora import CrearOperadorAseguradoraUseCase
from src.modules.admin.application.aplicar_bloqueo_arco import AplicarBloqueoArcoUseCase
from src.modules.admin.application.consultar_auditoria import ConsultarAuditoriaUseCase
from src.modules.admin.presentation import dependencies as deps

from tests.fakes.admin import FakeAseguradoraRepo, FakeAuditLogRepo, FakeAdminUserRepo
from tests.fakes.auth import FakeAuthRepo, FakePasswordService

BASE = "/api/v1/admin"


class FakeAseguradoraTenant:
    """Minimal fake del modelo AseguradoraTenant para pruebas."""
    def __init__(self, id, nombre, rfc, dominio_correo, plan_suscripcion, contacto_legal_email,
                 limite_peritajes_mes=100, peritajes_consumidos_mes=0,
                 estatus_comercial="Activo", version=1, deleted_at=None):
        self.id = id
        self.nombre = nombre
        self.rfc = rfc
        self.dominio_correo = dominio_correo
        self.plan_suscripcion = plan_suscripcion
        self.limite_peritajes_mes = limite_peritajes_mes
        self.peritajes_consumidos_mes = peritajes_consumidos_mes
        self.estatus_comercial = estatus_comercial
        self.contacto_legal_email = contacto_legal_email
        self.version = version
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        self.deleted_at = deleted_at


class FakeDesincorporacionJob:
    def trigger_desincorporacion(self, aseguradora_id: str) -> None:
        pass


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="admin-1", email="admin@claimvision.mx", rol="Administrador_Global", aseguradora_id=None
    )
    aseg_repo = FakeAseguradoraRepo()
    audit_repo = FakeAuditLogRepo()
    user_repo = FakeAdminUserRepo()
    auth_repo = FakeAuthRepo()
    pw_svc = FakePasswordService()

    app.dependency_overrides[deps.registrar_aseguradora_service] = lambda: RegistrarAseguradoraUseCase(aseg_repo, audit_repo)
    app.dependency_overrides[deps.list_aseguradoras_service] = lambda: ListAseguradoras(aseg_repo)
    app.dependency_overrides[deps.get_aseguradora_by_id_service] = lambda: GetAseguradoraById(aseg_repo)
    app.dependency_overrides[deps.actualizar_aseguradora_service] = lambda: ActualizarAseguradoraUseCase(aseg_repo, audit_repo)
    app.dependency_overrides[deps.verificar_aseguradora_service] = lambda: VerificarAseguradoraUseCase(aseg_repo, audit_repo)
    app.dependency_overrides[deps.actualizar_suscripcion_service] = lambda: ActualizarSuscripcionUseCase(aseg_repo, audit_repo)
    app.dependency_overrides[deps.desincorporar_aseguradora_service] = lambda: DesincorporarAseguradoraUseCase(
        aseg_repo, audit_repo, FakeDesincorporacionJob(), user_repo
    )
    app.dependency_overrides[deps.crear_operador_aseguradora_service] = lambda: CrearOperadorAseguradoraUseCase(
        aseg_repo, audit_repo, auth_repo, pw_svc
    )
    app.dependency_overrides[deps.aplicar_bloqueo_arco_service] = lambda: AplicarBloqueoArcoUseCase(user_repo, audit_repo)
    app.dependency_overrides[deps.consultar_auditoria_service] = lambda: ConsultarAuditoriaUseCase(audit_repo)
    return {"client": client, "aseg_repo": aseg_repo, "audit_repo": audit_repo, "user_repo": user_repo}


REGISTER_BODY = {
    "nombre": "Aseguradora X",
    "rfc": "AXC123456789",
    "dominio_correo": "@asegx.mx",
    "plan_suscripcion": "Profesional",
    "contacto_legal_email": "legal@asegx.mx",
}


def test_registrar_aseguradora(wired):
    r = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["nombre"] == "Aseguradora X"
    assert body["rfc"] == "AXC123456789"
    assert body["plan_suscripcion"] == "Profesional"


def test_listar_aseguradoras(wired):
    wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY)
    r = wired["client"].get(f"{BASE}/aseguradoras?page=1&page_size=10")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["total"] >= 1
    assert len(body["data"]) >= 1


def test_get_aseguradora_por_id(wired):
    created = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY).json()
    r = wired["client"].get(f"{BASE}/aseguradoras/{created['id']}")
    assert r.status_code == 200, r.text
    assert r.json()["id"] == created["id"]


def test_actualizar_aseguradora(wired):
    created = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY).json()
    r = wired["client"].put(f"{BASE}/aseguradoras/{created['id']}", json={"nombre": "Aseguradora Y"})
    assert r.status_code == 200, r.text
    assert r.json()["nombre"] == "Aseguradora Y"


def test_verificar_aseguradora(wired):
    created = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY).json()
    r = wired["client"].post(f"{BASE}/aseguradoras/{created['id']}/verificar")
    assert r.status_code == 200, r.text


def test_actualizar_suscripcion(wired):
    created = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY).json()
    r = wired["client"].put(f"{BASE}/aseguradoras/{created['id']}/suscripcion", json={"nuevo_plan": "Enterprise"})
    assert r.status_code == 200, r.text
    assert r.json()["plan_suscripcion"] == "Enterprise"


def test_desincorporar_aseguradora(wired):
    created = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY).json()
    r = wired["client"].delete(f"{BASE}/aseguradoras/{created['id']}")
    assert r.status_code == 200, r.text
    assert r.json()["estatus_comercial"] == "Cancelado"


def test_crear_operador_aseguradora(wired):
    created = wired["client"].post(f"{BASE}/aseguradoras", json=REGISTER_BODY).json()
    r = wired["client"].post(f"{BASE}/aseguradoras/{created['id']}/operadores", json={
        "nombre": "Operador 1", "email": "op1@asegx.mx", "password": "pass1234",
    })
    assert r.status_code == 201, r.text


def test_bloqueo_arco(wired):
    wired["user_repo"].users["user-1"] = {"usuario_id": "user-1", "aseguradora_id": "aseg-1"}
    r = wired["client"].post(f"{BASE}/usuarios/user-1/bloqueo-arco")
    assert r.status_code == 200, r.text
    assert wired["user_repo"].users["user-1"]["bloqueado_arco"] is True


def test_consultar_auditoria(wired):
    r = wired["client"].get(f"{BASE}/auditoria/logs?page=1&page_size=10")
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body.keys()) == {"data", "total", "page", "page_size"}


def test_rol_no_admin_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-cli", email="c@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/aseguradoras")
    assert r.status_code == 403
