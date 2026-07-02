"""Pruebas de §3 Aseguradora (`/api/v1/aseguradora/...`)."""
import pytest

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser

from src.modules.siniestro.application.siniestros.asignar_ajustador import AsignarAjustador
from src.modules.siniestro.application.siniestros.enviar_taller import EnviarTaller
from src.modules.aseguradora.application.siniestros.autorizar_entrega_v1 import AutorizarEntregaV1
from src.modules.aseguradora.application.siniestros.bandeja import (
    ListSiniestrosAseguradora, GetSiniestroAseguradora,
)
from src.modules.aseguradora.application.cotizaciones.aprobar_rechazar import (
    AprobarCotizacion, RechazarCotizacion,
)
from src.modules.aseguradora.presentation.v1 import aseguradora_v1_dependencies as adeps
from src.modules.siniestro.presentation.siniestros import siniestro_dependencies as sdeps

from tests.fakes import (
    FakeSiniestroRepo, FakeImagenRepo, FakePeritajeRepo, FakeCotizacionRepo,
    FakeAjustadorChecker, FakeTallerChecker, make_siniestro, make_cotizacion,
)

BASE = "/api/v1/aseguradora"


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-op", email="op@demo.mx", rol="Operador_Aseguradora", aseguradora_id="aseg-1"
    )
    sin = FakeSiniestroRepo()
    sin.items["sin-rep"] = make_siniestro("sin-rep", None, "Reportado_Preliminar")
    sin.items["sin-perit"] = make_siniestro("sin-perit", "aj-1", "Peritaje_Validado")
    sin.items["sin-listo"] = make_siniestro("sin-listo", "aj-1", "Listo_Para_Entrega", taller_id="taller-1")
    ajeno = make_siniestro("sin-otra", None, "Reportado_Preliminar")
    ajeno.aseguradora_id = "aseg-2"
    sin.items["sin-otra"] = ajeno

    img = FakeImagenRepo()
    per = FakePeritajeRepo()
    cot = FakeCotizacionRepo()
    cot.by_id["cot-1"] = make_cotizacion("cot-1", "sin-perit", "taller-1", "Pendiente_Aprobacion")
    cot.by_siniestro["sin-perit"] = cot.by_id["cot-1"]
    cot_ajena = make_cotizacion("cot-aj", "sin-otra", "taller-9", "Pendiente_Aprobacion")
    cot.by_id["cot-aj"] = cot_ajena

    app.dependency_overrides[adeps.list_siniestros_service] = lambda: ListSiniestrosAseguradora(sin)
    app.dependency_overrides[adeps.get_siniestro_service] = lambda: GetSiniestroAseguradora(sin, img, per, cot)
    app.dependency_overrides[adeps.aprobar_cotizacion_service] = lambda: AprobarCotizacion(cot, sin)
    app.dependency_overrides[adeps.rechazar_cotizacion_service] = lambda: RechazarCotizacion(cot, sin)
    app.dependency_overrides[adeps.autorizar_entrega_service] = lambda: AutorizarEntregaV1(sin)
    app.dependency_overrides[sdeps.asignar_ajustador_service] = lambda: AsignarAjustador(sin, FakeAjustadorChecker({"aj-1"}))
    app.dependency_overrides[sdeps.enviar_taller_service] = lambda: EnviarTaller(sin, FakeTallerChecker({"taller-1"}))
    return {"client": client, "sin": sin, "cot": cot}


def test_listar_siniestros_solo_tenant(wired):
    r = wired["client"].get(f"{BASE}/siniestros?page=1&page_size=10")
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body.keys()) == {"data", "total", "page", "page_size"}
    assert body["total"] == 3  # sin-otra (aseg-2) queda excluido


def test_listar_filtro_q(wired):
    r = wired["client"].get(f"{BASE}/siniestros?q=ABC")
    assert r.status_code == 200, r.text
    assert r.json()["total"] == 3  # todas tienen placas ABC-123


def test_detalle_siniestro(wired):
    r = wired["client"].get(f"{BASE}/siniestros/sin-perit")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["cotizacion"]["estatus"] == "Pendiente_Aprobacion"
    assert body["peritaje_ia"] is None


def test_detalle_otra_aseguradora_403(wired):
    r = wired["client"].get(f"{BASE}/siniestros/sin-otra")
    assert r.status_code == 403


def test_asignar_ajustador(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-rep/asignar-ajustador", json={"ajustador_id": "aj-1"})
    assert r.status_code == 200, r.text
    assert wired["sin"].items["sin-rep"].estatus == "Asignado_A_Ajustador"


def test_enviar_taller(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-perit/enviar-taller", json={"taller_id": "taller-1"})
    assert r.status_code == 200, r.text
    assert wired["sin"].items["sin-perit"].estatus == "Asignado_A_Taller"


def test_autorizar_entrega_va_a_entregado(wired):
    # Transición corregida: Listo_Para_Entrega → Entregado (no Listo, como el legacy)
    r = wired["client"].post(f"{BASE}/siniestros/sin-listo/autorizar-entrega")
    assert r.status_code == 200, r.text
    assert r.json()["estatus"] == "Entregado"


def test_aprobar_cotizacion(wired):
    r = wired["client"].post(f"{BASE}/cotizaciones/cot-1/aprobar")
    assert r.status_code == 200, r.text
    assert r.json()["estatus"] == "Aprobada"


def test_rechazar_cotizacion_con_motivo(wired):
    r = wired["client"].post(f"{BASE}/cotizaciones/cot-1/rechazar", json={"motivo": "Monto excesivo"})
    assert r.status_code == 200, r.text
    assert r.json()["estatus"] == "Rechazada"


def test_aprobar_cotizacion_de_otra_aseguradora_403(wired):
    r = wired["client"].post(f"{BASE}/cotizaciones/cot-aj/aprobar")
    assert r.status_code == 403


def test_rol_no_operador_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-cli", email="c@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/siniestros")
    assert r.status_code == 403
