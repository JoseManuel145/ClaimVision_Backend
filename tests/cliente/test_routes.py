"""Pruebas de §4 Cliente (`/api/v1/cliente/...`) — siniestros + onboarding."""
import pytest

from src.main import app
from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros_cliente import ListSiniestrosCliente
from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente
from src.modules.siniestro.application.siniestros.registrar_imagen import RegistrarImagenSiniestro
from src.modules.cliente.application.get_perfil_cliente import GetPerfilCliente
from src.modules.cliente.application.confirm_data import ConfirmData
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.cliente.presentation import cliente_v1_dependencies as deps
from src.modules.cliente.presentation.dependencies import confirm_data_service, process_ocr_service
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser

from tests.fakes.cliente import FakeClienteChecker, FakeClienteRepo, FakeOcrService, default_cliente_profile
from tests.fakes.siniestro import FakeSiniestroRepo, FakeImagenRepo
from tests.fakes.auth import FakeAuthRepo, FakeUser

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
    checker = FakeClienteChecker({"user-1": "perfil-1"})
    sin_repo = FakeSiniestroRepo()
    img_repo = FakeImagenRepo()
    cli_repo = FakeClienteRepo(default_cliente_profile())
    auth_repo = FakeAuthRepo()
    auth_repo.create(FakeUser(usuario_id="user-1", nombre="Cliente", email="cli@x.mx",
                              password_hash="x", rol="Cliente", aseguradora_id="aseg-1",
                              email_verificado=False))

    app.dependency_overrides[deps.reportar_siniestro_service] = lambda: InicializarSiniestro(sin_repo, checker)
    app.dependency_overrides[deps.list_siniestros_cliente_service] = lambda: ListSiniestrosCliente(sin_repo, checker)
    app.dependency_overrides[deps.get_siniestro_cliente_service] = lambda: GetSiniestroCliente(sin_repo, img_repo, checker)
    app.dependency_overrides[deps.registrar_imagen_service] = lambda: RegistrarImagenSiniestro(img_repo, sin_repo, checker)
    app.dependency_overrides[deps.get_perfil_cliente_service] = lambda: GetPerfilCliente(cli_repo)
    app.dependency_overrides[deps.confirm_consent_service] = lambda: ConfirmConsent(cli_repo, auth_repo)
    app.dependency_overrides[confirm_data_service] = lambda: ConfirmData(cli_repo)
    app.dependency_overrides[process_ocr_service] = lambda: FakeOcrService()
    return {"client": client, "sin_repo": sin_repo, "img_repo": img_repo, "cli_repo": cli_repo}


def test_reportar_siniestro_crea_en_estatus_preliminar(wired):
    r = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["estatus"] == "Reportado_Preliminar"
    assert body["cliente_id"] == "perfil-1"
    assert body["indicaciones_dano_interno"] is True


def test_reportar_sin_onboarding_falla(wired):
    app.dependency_overrides[deps.reportar_siniestro_service] = lambda: InicializarSiniestro(
        wired["sin_repo"], FakeClienteChecker({})
    )
    r = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r.status_code == 409


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
    assert "curp_rfc_cifrado" not in body


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
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u2", email="taller@x.mx", rol="Operador_Taller", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 403


def test_ocr_extraction(wired):
    r = wired["client"].post(f"{BASE}/onboarding/ocr", files={
        "cedula": ("ced.jpg", b"fake-image-data", "image/jpeg"),
        "poliza": ("pol.jpg", b"fake-image-data", "image/jpeg"),
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["numero_poliza"] == "POL-999"


def test_confirmar_datos_onboarding(wired):
    r = wired["client"].post(f"{BASE}/onboarding/confirmar-datos", json={
        "numero_poliza": "POL-999",
        "vigencia_poliza": "2030-12-31",
        "curp_rfc": "CURP123456XYZ",
    })
    assert r.status_code == 200, r.text
    assert wired["cli_repo"].profile.numero_poliza == "POL-999"


def test_onboarding_rol_no_cliente_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u2", email="taller@x.mx", rol="Operador_Taller", aseguradora_id="aseg-1"
    )
    r = wired["client"].post(f"{BASE}/onboarding/confirmar-datos", json={
        "numero_poliza": "POL-999", "vigencia_poliza": "2030-12-31", "curp_rfc": "CURP",
    })
    assert r.status_code == 403
