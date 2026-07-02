"""Pruebas de §4 Cliente (`/api/v1/cliente/...`)."""
import pytest

from src.main import app
from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros_cliente import ListSiniestrosCliente
from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente
from src.modules.siniestro.application.siniestros.registrar_imagen import RegistrarImagenSiniestro
from src.modules.cliente.application.get_perfil_cliente import GetPerfilCliente
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.cliente.presentation.v1 import cliente_v1_dependencies as deps
from src.core.security import get_current_user

from tests.fakes import (
    FakeClienteChecker, FakeSiniestroRepo, FakeImagenRepo,
    FakeClienteRepo, FakeAuthRepo, default_cliente_profile,
)

BASE = "/api/v1/cliente"
REPORTE = {
    "vehiculo_marca": "Toyota",
    "vehiculo_modelo": "Corolla",
    "vehiculo_anio": 2020,
    "vehiculo_placas": "ABC-123",
    "latitud_siniestro": 19.4326,
    "longitud_siniestro": -99.1332,
    "narracion_texto": "Choque leve",
    "indicaciones_dano_interno": True,
}


@pytest.fixture
def wired(client):
    """Cablea las dependencias del dominio Cliente con fakes compartidos."""
    checker = FakeClienteChecker({"user-1": "perfil-1"})
    sin_repo = FakeSiniestroRepo()
    img_repo = FakeImagenRepo()
    cli_repo = FakeClienteRepo(default_cliente_profile())
    auth_repo = FakeAuthRepo()

    app.dependency_overrides[deps.reportar_siniestro_service] = lambda: InicializarSiniestro(sin_repo, checker)
    app.dependency_overrides[deps.list_siniestros_cliente_service] = lambda: ListSiniestrosCliente(sin_repo, checker)
    app.dependency_overrides[deps.get_siniestro_cliente_service] = lambda: GetSiniestroCliente(sin_repo, img_repo, checker)
    app.dependency_overrides[deps.registrar_imagen_service] = lambda: RegistrarImagenSiniestro(img_repo, sin_repo, checker)
    app.dependency_overrides[deps.get_perfil_cliente_service] = lambda: GetPerfilCliente(cli_repo)
    app.dependency_overrides[deps.confirm_consent_service] = lambda: ConfirmConsent(cli_repo, auth_repo)
    return {"client": client, "sin_repo": sin_repo, "img_repo": img_repo, "cli_repo": cli_repo}


def test_reportar_siniestro_crea_en_estatus_preliminar(wired):
    r = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["estatus"] == "Reportado_Preliminar"
    assert body["cliente_id"] == "perfil-1"
    assert body["indicaciones_dano_interno"] is True


def test_reportar_sin_onboarding_falla(wired):
    # Sobrescribe el checker a uno que no conoce al usuario
    app.dependency_overrides[deps.reportar_siniestro_service] = lambda: InicializarSiniestro(
        wired["sin_repo"], FakeClienteChecker({})
    )
    r = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r.status_code == 409  # BusinessRuleError


def test_listar_mis_siniestros_paginado(wired):
    wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    r = wired["client"].get(f"{BASE}/siniestros?page=1&page_size=10")
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body.keys()) == {"data", "total", "page", "page_size"}
    assert body["total"] == 1
    assert body["page"] == 1
    assert len(body["data"]) == 1


def test_detalle_incluye_timeline_e_imagenes(wired):
    sid = wired["client"].post(f"{BASE}/siniestros", json=REPORTE).json()["id"]
    wired["client"].post(f"{BASE}/siniestros/{sid}/imagenes", json={"imagen_url": "https://x/img.jpg"})
    r = wired["client"].get(f"{BASE}/siniestros/{sid}")
    assert r.status_code == 200, r.text
    body = r.json()
    assert len(body["imagenes"]) == 1
    assert len(body["timeline"]) == 7
    primero = body["timeline"][0]
    assert primero["estatus"] == "Reportado_Preliminar"
    assert primero["alcanzado"] is True and primero["actual"] is True


def test_detalle_de_otro_cliente_prohibido(wired):
    sid = wired["client"].post(f"{BASE}/siniestros", json=REPORTE).json()["id"]
    # El siniestro pertenece a 'perfil-1'; cambiamos el checker a otro perfil
    from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente as GC
    app.dependency_overrides[deps.get_siniestro_cliente_service] = lambda: GC(
        wired["sin_repo"], wired["img_repo"], FakeClienteChecker({"user-1": "perfil-OTRO"})
    )
    r = wired["client"].get(f"{BASE}/siniestros/{sid}")
    assert r.status_code == 403


def test_registrar_imagen(wired):
    sid = wired["client"].post(f"{BASE}/siniestros", json=REPORTE).json()["id"]
    r = wired["client"].post(f"{BASE}/siniestros/{sid}/imagenes", json={"imagen_url": "https://x/a.jpg", "metadatos_json": {"k": 1}})
    assert r.status_code == 201, r.text
    assert r.json()["imagen_url"] == "https://x/a.jpg"
    assert r.json()["es_calidad_valida"] is True


def test_perfil_cliente(wired):
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["numero_poliza"] == "POL-123"
    assert "curp_rfc_cifrado" not in body  # PII cifrada no se expone


def test_actualizar_consentimientos(wired):
    r = wired["client"].patch(f"{BASE}/consentimientos", json={
        "consentimiento_aviso_privacidad": True,
        "consentimiento_biometria": False,
        "autoriza_transferencia_talleres": True,
    })
    assert r.status_code == 200, r.text
    assert wired["cli_repo"].profile.consentimiento_aviso_privacidad is True
    assert wired["cli_repo"].profile.fecha_consentimiento is not None


def test_rol_no_cliente_rechazado(wired):
    from src.modules.auth.domain.models import AuthenticatedUser
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u2", email="taller@x.mx", rol="Operador_Taller", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 403
