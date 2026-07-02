"""Pruebas de §6 Taller (`/api/v1/taller/...`)."""
import pytest

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser

from src.modules.taller.application.expedientes.list_expedientes import ListExpedientesTallerUseCase
from src.modules.taller.application.expedientes.get_expediente import GetExpedienteTallerUseCase
from src.modules.taller.application.expedientes.concluir_expediente import ConcluirExpedienteUseCase
from src.modules.taller.application.expedientes.marcar_listo_entrega import MarcarListoEntrega
from src.modules.taller.application.cotizaciones_v1 import CrearCotizacion, EditarCotizacion
from src.modules.taller.presentation.v1 import taller_v1_dependencies as deps

from tests.fakes import (
    FakeSiniestroRepo, FakePeritajeRepo, FakeCotizacionRepo, FakePerfilTallerRepo,
    make_siniestro, make_cotizacion, make_peritaje,
)

BASE = "/api/v1/taller"
COTIZACION_BODY = {
    "monto_mano_obra": 4000.0,
    "monto_refacciones": 6000.0,
    "monto_total": 10000.0,
    "desglose_pdf_url": "https://x/desglose.pdf",
    "observaciones_tecnicas": "Incluye pintura",
}


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-t", email="taller@demo.mx", rol="Operador_Taller", aseguradora_id="aseg-1"
    )
    perfil = FakePerfilTallerRepo({"user-t": "taller-1"})
    sin = FakeSiniestroRepo()
    sin.items["sin-t"] = make_siniestro("sin-t", "aj-profile-1", "Asignado_A_Taller", taller_id="taller-1")
    sin.items["sin-listo"] = make_siniestro("sin-listo", "aj-profile-1", "Trabajo_Concluido", taller_id="taller-1")
    sin.items["sin-ajeno"] = make_siniestro("sin-ajeno", "aj-profile-1", "Asignado_A_Taller", taller_id="otro")
    per = FakePeritajeRepo()
    per.guardar_peritaje(make_peritaje("sin-t"))
    cot = FakeCotizacionRepo()

    app.dependency_overrides[deps.list_ordenes_service] = lambda: ListExpedientesTallerUseCase(sin, perfil)
    app.dependency_overrides[deps.get_orden_service] = lambda: GetExpedienteTallerUseCase(sin, per, cot, perfil)
    app.dependency_overrides[deps.crear_cotizacion_service] = lambda: CrearCotizacion(sin, cot, perfil, per)
    app.dependency_overrides[deps.editar_cotizacion_service] = lambda: EditarCotizacion(cot, perfil)
    app.dependency_overrides[deps.concluir_trabajo_service] = lambda: ConcluirExpedienteUseCase(sin, cot, perfil)
    app.dependency_overrides[deps.listo_entrega_service] = lambda: MarcarListoEntrega(sin, perfil)
    return {"client": client, "sin": sin, "cot": cot, "per": per}


def test_listar_ordenes(wired):
    r = wired["client"].get(f"{BASE}/ordenes?page=1&page_size=10")
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body.keys()) == {"data", "total", "page", "page_size"}
    # sin-t y sin-listo pertenecen a taller-1
    assert body["total"] == 2


def test_detalle_orden(wired):
    r = wired["client"].get(f"{BASE}/siniestros/sin-t")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["peritaje"] is not None
    assert body["cotizacion"] is None


def test_detalle_orden_ajena_403(wired):
    r = wired["client"].get(f"{BASE}/siniestros/sin-ajeno")
    assert r.status_code == 403


def test_crear_cotizacion(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-t/cotizacion", json=COTIZACION_BODY)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["estatus"] == "Pendiente_Aprobacion"
    assert body["monto_total"] == 10000.0
    assert body["taller_id"] == "taller-1"


def test_crear_cotizacion_sin_peritaje_409(wired):
    # sin-listo no tiene peritaje seedeado, y además no está Asignado_A_Taller
    r = wired["client"].post(f"{BASE}/siniestros/sin-listo/cotizacion", json=COTIZACION_BODY)
    assert r.status_code == 409


def test_editar_cotizacion(wired):
    cid = wired["client"].post(f"{BASE}/siniestros/sin-t/cotizacion", json=COTIZACION_BODY).json()["id"]
    r = wired["client"].patch(f"{BASE}/cotizaciones/{cid}", json={"monto_mano_obra": 5000.0})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["monto_mano_obra"] == 5000.0
    assert body["monto_total"] == 11000.0  # recomputado 5000 + 6000


def test_editar_cotizacion_aprobada_bloqueada(wired):
    wired["cot"].by_id["cot-aprob"] = make_cotizacion("cot-aprob", "sin-t", "taller-1", estatus="Aprobada")
    r = wired["client"].patch(f"{BASE}/cotizaciones/cot-aprob", json={"monto_mano_obra": 1.0})
    assert r.status_code == 409


def test_concluir_trabajo_requiere_cotizacion_aprobada(wired):
    # Sin cotización aprobada → 400
    r = wired["client"].post(f"{BASE}/siniestros/sin-t/concluir-trabajo")
    assert r.status_code == 400

    # Con cotización aprobada → 200 y estatus Trabajo_Concluido
    wired["cot"].by_siniestro["sin-t"] = make_cotizacion("cot-ap", "sin-t", "taller-1", estatus="Aprobada")
    r2 = wired["client"].post(f"{BASE}/siniestros/sin-t/concluir-trabajo")
    assert r2.status_code == 200, r2.text
    assert wired["sin"].items["sin-t"].estatus == "Trabajo_Concluido"


def test_listo_entrega(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-listo/listo-entrega")
    assert r.status_code == 200, r.text
    assert r.json()["estatus"] == "Listo_Para_Entrega"


def test_listo_entrega_estatus_invalido_409(wired):
    # sin-t está Asignado_A_Taller, no Trabajo_Concluido → transición inválida
    r = wired["client"].post(f"{BASE}/siniestros/sin-t/listo-entrega")
    assert r.status_code == 409


def test_rol_no_taller_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-cli", email="c@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/ordenes")
    assert r.status_code == 403
