"""Pruebas de §5 Ajustador (`/api/v1/ajustador/...`)."""
import pytest

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel

from src.modules.ajustador.application.asignaciones import ListMisAsignaciones, GetMiSiniestro
from src.modules.ajustador.application.peritaje import RegistrarPeritaje, EditarPeritaje, AgregarDano
from src.modules.ajustador.application.perfil import ActualizarDisponibilidad, ActualizarGeolocalizacion
from src.modules.ajustador.presentation import ajustador_dependencies as deps

from tests.fakes.ajustador import FakeAjustadorRepo, default_ajustador
from tests.fakes.siniestro import FakeSiniestroRepo, FakeImagenRepo, FakePeritajeRepo, make_siniestro

BASE = "/api/v1/ajustador"
PERITAJE_BODY = {
    "costo_definitivo_ajustador": 15000.0,
    "firma_digital_ajustador": "data:image/png;base64,xxx",
    "observaciones_campo": "Daño frontal",
    "danos": [
        {"zona_vehiculo": "Cofre", "tipo": "Abolladura", "severidad": "Medio", "costo_real_reparacion": 5000.0},
    ],
}


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-aj", email="aj@demo.mx", rol="Ajustador", aseguradora_id="aseg-1"
    )
    aj_repo = FakeAjustadorRepo({"user-aj": default_ajustador()})
    sin_repo = FakeSiniestroRepo()
    sin_repo.items["sin-1"] = make_siniestro("sin-1", "aj-profile-1", "Asignado_A_Ajustador")
    sin_repo.items["sin-prelim"] = make_siniestro("sin-prelim", "aj-profile-1", "Reportado_Preliminar")
    sin_repo.items["sin-ajeno"] = make_siniestro("sin-ajeno", "otro-aj", "Asignado_A_Ajustador")
    img_repo = FakeImagenRepo()
    per_repo = FakePeritajeRepo()

    app.dependency_overrides[deps.list_asignaciones_service] = lambda: ListMisAsignaciones(aj_repo, sin_repo)
    app.dependency_overrides[deps.get_siniestro_service] = lambda: GetMiSiniestro(aj_repo, sin_repo, img_repo, per_repo)
    app.dependency_overrides[deps.registrar_peritaje_service] = lambda: RegistrarPeritaje(aj_repo, sin_repo, per_repo)
    app.dependency_overrides[deps.editar_peritaje_service] = lambda: EditarPeritaje(aj_repo, sin_repo, per_repo)
    app.dependency_overrides[deps.agregar_dano_service] = lambda: AgregarDano(aj_repo, sin_repo, per_repo)
    app.dependency_overrides[deps.disponibilidad_service] = lambda: ActualizarDisponibilidad(aj_repo)
    app.dependency_overrides[deps.geolocalizacion_service] = lambda: ActualizarGeolocalizacion(aj_repo)
    return {"client": client, "aj_repo": aj_repo, "sin_repo": sin_repo, "per_repo": per_repo}


def _seed_borrador(per_repo, siniestro_id="sin-1", ajustador_id="aj-profile-1") -> str:
    p = PeritajeAjustadorModel(
        id="per-1", siniestro_id=siniestro_id, ajustador_id=ajustador_id,
        costo_definitivo_ajustador=1000.0, firma_digital_ajustador="firma",
        observaciones_campo=None, danos=[], version=1,
        created_at=None, updated_at=None,
    )
    return per_repo.guardar_peritaje(p).id


def test_asignaciones_paginado(wired):
    r = wired["client"].get(f"{BASE}/asignaciones?page=1&page_size=10")
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body.keys()) == {"data", "total", "page", "page_size"}
    assert body["total"] == 2


def test_detalle_sin_peritaje_ni_ia(wired):
    r = wired["client"].get(f"{BASE}/siniestros/sin-1")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["peritaje"] is None
    assert body["peritaje_ia"] is None
    assert body["imagenes"] == []


def test_detalle_de_siniestro_ajeno_prohibido(wired):
    r = wired["client"].get(f"{BASE}/siniestros/sin-ajeno")
    assert r.status_code == 403


def test_registrar_peritaje_valida_siniestro(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-1/peritaje", json=PERITAJE_BODY)
    assert r.status_code == 201, r.text
    assert wired["sin_repo"].items["sin-1"].estatus == "Peritaje_Validado"
    body = r.json()
    assert body["ajustador_id"] == "aj-profile-1"
    assert len(body["danos"]) == 1


def test_registrar_peritaje_estatus_invalido_409(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-prelim/peritaje", json=PERITAJE_BODY)
    assert r.status_code == 409


def test_registrar_peritaje_siniestro_ajeno_403(wired):
    r = wired["client"].post(f"{BASE}/siniestros/sin-ajeno/peritaje", json=PERITAJE_BODY)
    assert r.status_code == 403


def test_editar_borrador_antes_de_validar(wired):
    pid = _seed_borrador(wired["per_repo"])
    r = wired["client"].patch(f"{BASE}/peritajes/{pid}", json={"costo_definitivo_ajustador": 2500.0})
    assert r.status_code == 200, r.text
    assert r.json()["costo_definitivo_ajustador"] == 2500.0


def test_agregar_dano_a_borrador(wired):
    pid = _seed_borrador(wired["per_repo"])
    r = wired["client"].post(f"{BASE}/peritajes/{pid}/danos", json={
        "zona_vehiculo": "Puerta", "tipo": "Rayadura", "severidad": "Bajo", "costo_real_reparacion": 800.0,
    })
    assert r.status_code == 201, r.text
    assert len(r.json()["danos"]) == 1


def test_editar_tras_validar_bloqueado(wired):
    wired["client"].post(f"{BASE}/siniestros/sin-1/peritaje", json=PERITAJE_BODY)
    pid = wired["per_repo"].by_siniestro["sin-1"].id
    r = wired["client"].patch(f"{BASE}/peritajes/{pid}", json={"costo_definitivo_ajustador": 9.0})
    assert r.status_code == 409


def test_disponibilidad(wired):
    r = wired["client"].patch(f"{BASE}/disponibilidad", json={"activo_para_servicio": False})
    assert r.status_code == 200, r.text
    assert r.json()["activo_para_servicio"] is False
    assert wired["aj_repo"].by_usuario["user-aj"].activo_para_servicio is False


def test_geolocalizacion(wired):
    r = wired["client"].put(f"{BASE}/geolocalizacion", json={"latitud": 19.43, "longitud": -99.13})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["latitud"] == 19.43 and body["longitud"] == -99.13


def test_rol_no_ajustador_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-cli", email="c@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/asignaciones")
    assert r.status_code == 403
