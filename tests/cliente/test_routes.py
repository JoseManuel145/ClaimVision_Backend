"""Pruebas de §4 Cliente (`/api/v1/cliente/...`) — siniestros + onboarding."""
import pytest
from concurrent.futures import ThreadPoolExecutor

from src.main import app
from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros_cliente import ListSiniestrosCliente
from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente
from src.modules.siniestro.application.siniestros.registrar_imagen import RegistrarImagenSiniestro
from src.modules.cliente.application.get_perfil_cliente import GetPerfilCliente
from src.modules.cliente.application.actualizar_perfil_cliente import ActualizarPerfilCliente
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
    app.dependency_overrides[deps.actualizar_perfil_cliente_service] = lambda: ActualizarPerfilCliente(cli_repo, auth_repo)
    app.dependency_overrides[deps.get_auth_repo_for_enrichment] = lambda: auth_repo
    app.dependency_overrides[confirm_data_service] = lambda: ConfirmData(cli_repo)
    app.dependency_overrides[process_ocr_service] = lambda: FakeOcrService()
    return {"client": client, "sin_repo": sin_repo, "img_repo": img_repo, "cli_repo": cli_repo, "auth_repo": auth_repo}


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


def test_put_perfil_updates_user(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={
        "nombre": "Cliente Nuevo",
        "email": "cli.nuevo@x.mx",
        "telefono": "555-9999",
    })
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["numero_poliza"] == "POL-123"
    assert body["nombre"] == "Cliente Nuevo"
    assert body["email"] == "cli.nuevo@x.mx"
    assert body["telefono"] == "555-9999"

    user = wired["auth_repo"].get_by_id("user-1")
    assert user.nombre == "Cliente Nuevo"
    assert user.email == "cli.nuevo@x.mx"
    assert user.telefono == "555-9999"


def test_put_perfil_partial_update(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={"nombre": "Solo Nombre"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Solo Nombre"
    assert body["numero_poliza"] == "POL-123"


def test_put_perfil_empty_body_no_changes(wired):
    r = wired["client"].put(f"{BASE}/perfil", json={})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["nombre"] == "Cliente"
    assert body["email"] == "cli@x.mx"


def test_put_perfil_rol_no_cliente_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u2", email="taller@x.mx", rol="Operador_Taller", aseguradora_id="aseg-1"
    )
    r = wired["client"].put(f"{BASE}/perfil", json={"nombre": "X"})
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


# ── Tests complejos ─────────────────────────────────────────────────────

def test_reportar_siniestro_faltan_campos_obligatorios(wired):
    """422 si faltan campos obligatorios en el reporte."""
    r = wired["client"].post(f"{BASE}/siniestros", json={})
    assert r.status_code == 422

    r = wired["client"].post(f"{BASE}/siniestros", json={
        "vehiculo_marca": "Toyota", "vehiculo_modelo": "Corolla",
    })
    assert r.status_code == 422


def test_reportar_siniestro_valores_extremos(wired):
    """Acepta strings largos, SQL injection, años extremos."""
    sql_injection = "ABC-123'; DROP TABLE siniestros; --"
    marca_larga = "X" * 500
    r = wired["client"].post(f"{BASE}/siniestros", json={
        "vehiculo_marca": marca_larga,
        "vehiculo_modelo": "Modelo",
        "vehiculo_anio": 9999,
        "vehiculo_placas": sql_injection,
        "latitud_siniestro": 90.0,
        "longitud_siniestro": 180.0,
    })
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["vehiculo_marca"] == marca_larga
    assert body["vehiculo_placas"] == sql_injection
    assert body["estatus"] == "Reportado_Preliminar"


def test_reportar_siniestro_idempotente(wired):
    """Mismo payload dos veces → 201 ambos, IDs distintos."""
    r1 = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r1.status_code == 201
    r2 = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r2.status_code == 201
    assert r1.json()["id"] != r2.json()["id"]


def test_listar_siniestros_paginacion_extrema(wired):
    """Paginación con valores límite válidos funciona; inválidos dan 422."""
    wired["client"].post(f"{BASE}/siniestros", json=REPORTE)

    for page, ps, expected in [(0, 10, 422), (-1, 10, 422), (1, 0, 422), (1, 9999, 422), (1, 1, 200), (1, 100, 200)]:
        r = wired["client"].get(f"{BASE}/siniestros?page={page}&page_size={ps}")
        assert r.status_code == expected, f"page={page} page_size={ps} — {r.text}"


def test_listar_siniestros_filtro_estatus(wired):
    """Filtrar por estatus existente e inexistente."""
    r = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    sid = r.json()["id"]

    r = wired["client"].get(f"{BASE}/siniestros?estatus=Reportado_Preliminar")
    assert r.status_code == 200
    ids = [s["id"] for s in r.json()["data"]]
    assert sid in ids

    r = wired["client"].get(f"{BASE}/siniestros?estatus=Entregado")
    assert len(r.json()["data"]) == 0


def test_listar_siniestros_sin_resultados(wired):
    """Página más allá del total debe devolver lista vacía."""
    r = wired["client"].get(f"{BASE}/siniestros?page=999&page_size=10")
    assert r.status_code == 200
    body = r.json()
    assert body["data"] == []
    assert body["total"] == 0


def test_detalle_siniestro_inexistente_404(wired):
    """UUID que no existe debe devolver 404."""
    r = wired["client"].get(f"{BASE}/siniestros/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404


def test_registrar_imagen_url_invalida(wired):
    """URL vacía debe ser aceptada o rechazada elegantemente."""
    sid = wired["client"].post(f"{BASE}/siniestros", json=REPORTE).json()["id"]
    r = wired["client"].post(f"{BASE}/siniestros/{sid}/imagenes", json={"imagen_url": ""})
    assert r.status_code in (201, 422), r.text


def test_perfil_sin_onboarding_404(wired):
    """Cliente sin perfil → 404 elegante."""
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-sin-perfil", email="noprofile@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/perfil")
    assert r.status_code == 404


def test_confirmar_datos_onboarding_duplicado(wired):
    """Confirmar datos dos veces es seguro (idempotente)."""
    payload = {"numero_poliza": "POL-DUP", "vigencia_poliza": "2030-12-31", "curp_rfc": "CURPDUP"}
    r1 = wired["client"].post(f"{BASE}/onboarding/confirmar-datos", json=payload)
    assert r1.status_code == 200
    r2 = wired["client"].post(f"{BASE}/onboarding/confirmar-datos", json=payload)
    assert r2.status_code == 200
    assert wired["cli_repo"].profile.numero_poliza == "POL-DUP"


def test_consentimientos_sin_aviso_privacidad(wired):
    """Rechazar consentimiento sin aviso de privacidad → 409."""
    r = wired["client"].patch(f"{BASE}/consentimientos", json={
        "consentimiento_aviso_privacidad": False,
        "consentimiento_biometria": False,
        "autoriza_transferencia_talleres": False,
    })
    assert r.status_code == 409


def test_tester_global_bypass_cliente(wired):
    """Tester_Global accede a todos los endpoints de cliente."""
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-tester", email="tester@x.mx", rol="Tester_Global", aseguradora_id="aseg-1"
    )
    cli_repo_tester = FakeClienteRepo(default_cliente_profile())
    cli_repo_tester.profile.usuario_id = "user-tester"
    app.dependency_overrides[deps.get_perfil_cliente_service] = lambda: GetPerfilCliente(cli_repo_tester)

    checker_tester = FakeClienteChecker({"user-tester": "perfil-tester"})
    sin_repo_tester = FakeSiniestroRepo()
    app.dependency_overrides[deps.list_siniestros_cliente_service] = lambda: ListSiniestrosCliente(sin_repo_tester, checker_tester)
    app.dependency_overrides[deps.reportar_siniestro_service] = lambda: InicializarSiniestro(sin_repo_tester, checker_tester)

    r_perfil = wired["client"].get(f"{BASE}/perfil")
    assert r_perfil.status_code == 200, r_perfil.text

    r_list = wired["client"].get(f"{BASE}/siniestros")
    assert r_list.status_code == 200, r_list.text

    r_create = wired["client"].post(f"{BASE}/siniestros", json=REPORTE)
    assert r_create.status_code == 201, r_create.text
