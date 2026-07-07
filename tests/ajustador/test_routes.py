"""Pruebas de §5 Ajustador (`/api/v1/ajustador/...`)."""
import pytest
from concurrent.futures import ThreadPoolExecutor

from src.main import app
from src.core.security import get_current_user
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel

from src.modules.ajustador.application.list_mis_asignaciones import ListMisAsignaciones
from src.modules.ajustador.application.get_mi_siniestro import GetMiSiniestro
from src.modules.ajustador.application.registrar_peritaje import RegistrarPeritaje
from src.modules.ajustador.application.editar_peritaje import EditarPeritaje
from src.modules.ajustador.application.agregar_dano import AgregarDano
from src.modules.ajustador.application.actualizar_disponibilidad import ActualizarDisponibilidad
from src.modules.ajustador.application.actualizar_geolocalizacion import ActualizarGeolocalizacion
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
    sin_repo.items["sin-borrador"] = make_siniestro("sin-borrador", "aj-profile-1", "Asignado_A_Ajustador")
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


def _seed_borrador(per_repo, siniestro_id="sin-borrador", ajustador_id="aj-profile-1") -> str:
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
    assert body["total"] == 3


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


# ── Tests complejos ─────────────────────────────────────────────────────

def test_asignaciones_paginacion_extrema(wired):
    """Paginación con valores límite válidos funciona; inválidos dan 422."""
    for page, ps, expected in [(0, 10, 422), (-1, 10, 422), (1, 0, 422), (1, 9999, 422), (1, 1, 200), (1, 100, 200)]:
        r = wired["client"].get(f"{BASE}/asignaciones?page={page}&page_size={ps}")
        assert r.status_code == expected, f"page={page} page_size={ps} — {r.text}"


def test_asignaciones_filtro_estatus(wired):
    """Filtrar asignaciones por estatus."""
    r = wired["client"].get(f"{BASE}/asignaciones?estatus=Asignado_A_Ajustador")
    assert r.status_code == 200
    assert all(s["estatus"] == "Asignado_A_Ajustador" for s in r.json()["data"])

    r = wired["client"].get(f"{BASE}/asignaciones?estatus=Entregado")
    assert len(r.json()["data"]) == 0


def test_asignaciones_sin_resultados(wired):
    """Página más allá del total debe devolver lista vacía."""
    r = wired["client"].get(f"{BASE}/asignaciones?page=999&page_size=10")
    assert r.status_code == 200
    body = r.json()
    assert body["data"] == []


def test_detalle_siniestro_inexistente_404(wired):
    """UUID que no existe debe devolver 404."""
    r = wired["client"].get(f"{BASE}/siniestros/00000000-0000-0000-0000-000000000000")
    assert r.status_code == 404


def test_registrar_peritaje_sin_firma(wired):
    """Peritaje sin firma digital es rechazado (422 por campo requerido)."""
    body = {k: v for k, v in PERITAJE_BODY.items() if k != "firma_digital_ajustador"}
    r = wired["client"].post(f"{BASE}/siniestros/sin-1/peritaje", json=body)
    assert r.status_code in (400, 422), r.text


def test_registrar_peritaje_siniestro_inexistente(wired):
    """Peritaje sobre siniestro que no existe → 404."""
    r = wired["client"].post(f"{BASE}/siniestros/no-existe/peritaje", json=PERITAJE_BODY)
    assert r.status_code == 404


def test_registrar_peritaje_concurrente(wired):
    """Dos peticiones en paralelo: solo una crea el peritaje."""
    def post_peritaje():
        return wired["client"].post(f"{BASE}/siniestros/sin-1/peritaje", json=PERITAJE_BODY)

    with ThreadPoolExecutor(max_workers=2) as pool:
        fut1 = pool.submit(post_peritaje)
        fut2 = pool.submit(post_peritaje)
        r1, r2 = fut1.result(), fut2.result()

    codigos = {r1.status_code, r2.status_code}
    assert codigos == {201, 409}, f"Esperaba 201 y 409, obtuvo {codigos}"


def test_editar_peritaje_ajeno(wired):
    """No se puede editar un peritaje que no pertenece al ajustador."""
    pid = _seed_borrador(wired["per_repo"], ajustador_id="otro-aj")
    r = wired["client"].patch(f"{BASE}/peritajes/{pid}", json={"costo_definitivo_ajustador": 999.0})
    assert r.status_code == 403


def test_agregar_dano_sin_peritaje(wired):
    """Agregar daño a un peritaje que no existe → 404."""
    r = wired["client"].post(f"{BASE}/peritajes/no-existe/danos", json={
        "zona_vehiculo": "Puerta", "tipo": "Rayadura",
        "severidad": "Bajo", "costo_real_reparacion": 500.0,
    })
    assert r.status_code == 404


def test_disponibilidad_sin_campo(wired):
    """Body vacío en disponibilidad → 422."""
    r = wired["client"].patch(f"{BASE}/disponibilidad", json={})
    assert r.status_code == 422


def test_geolocalizacion_coordenadas_invalidas(wired):
    """Coordenadas fuera de rango son aceptadas o rechazadas."""
    r = wired["client"].put(f"{BASE}/geolocalizacion", json={"latitud": 100.0, "longitud": 200.0})
    assert r.status_code in (200, 422), r.text


def test_tester_global_bypass_ajustador(wired):
    """Tester_Global accede a todos los endpoints de ajustador."""
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="user-tester-aj", email="tester@x.mx", rol="Tester_Global", aseguradora_id="aseg-1"
    )
    aj_repo_tester = FakeAjustadorRepo({"user-tester-aj": default_ajustador(
        usuario_id="user-tester-aj", ajustador_id="aj-tester"
    )})
    sin_repo_tester = FakeSiniestroRepo()
    sin_repo_tester.items["sin-tester"] = make_siniestro("sin-tester", "aj-tester", "Asignado_A_Ajustador")
    per_repo_tester = FakePeritajeRepo()
    app.dependency_overrides = {k: v for k, v in app.dependency_overrides.items()
                                if k in (get_current_user,)}
    app.dependency_overrides[deps.list_asignaciones_service] = lambda: ListMisAsignaciones(aj_repo_tester, sin_repo_tester)
    app.dependency_overrides[deps.get_siniestro_service] = lambda: GetMiSiniestro(aj_repo_tester, sin_repo_tester, FakeImagenRepo(), per_repo_tester)
    app.dependency_overrides[deps.registrar_peritaje_service] = lambda: RegistrarPeritaje(aj_repo_tester, sin_repo_tester, per_repo_tester)
    app.dependency_overrides[deps.disponibilidad_service] = lambda: ActualizarDisponibilidad(aj_repo_tester)
    app.dependency_overrides[deps.geolocalizacion_service] = lambda: ActualizarGeolocalizacion(aj_repo_tester)

    r_list = wired["client"].get(f"{BASE}/asignaciones")
    assert r_list.status_code == 200, f"asignaciones: {r_list.text}"

    r_detalle = wired["client"].get(f"{BASE}/siniestros/sin-tester")
    assert r_detalle.status_code == 200, f"detalle: {r_detalle.text}"

    r_peritaje = wired["client"].post(f"{BASE}/siniestros/sin-tester/peritaje", json=PERITAJE_BODY)
    assert r_peritaje.status_code == 201, f"peritaje: {r_peritaje.text}"

    r_disp = wired["client"].patch(f"{BASE}/disponibilidad", json={"activo_para_servicio": False})
    assert r_disp.status_code == 200, f"disponibilidad: {r_disp.text}"

    r_geo = wired["client"].put(f"{BASE}/geolocalizacion", json={"latitud": 10.0, "longitud": -10.0})
    assert r_geo.status_code == 200, f"geolocalizacion: {r_geo.text}"
