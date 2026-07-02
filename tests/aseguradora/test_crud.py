"""Pruebas de Aseguradora CRUD v1 (`/api/v1/aseguradora/...`) — ajustadores, clientes, talleres, ARCO."""
import pytest
from datetime import datetime, timezone
from dataclasses import dataclass
from uuid import uuid4

from src.main import app
from src.core.security import get_current_user, require_roles
from src.modules.auth.domain.models import AuthenticatedUser

from src.modules.ajustador.domain.ports.ajustador_module_port import AjustadorModulePort
from src.modules.cliente.domain.module_port import ClienteModulePort
from src.modules.taller.domain.ports.taller_module_port import TallerModulePort

from src.modules.aseguradora.presentation.ajustadores import ajustador_dependencies
from src.modules.aseguradora.presentation.clientes import cliente_dependencies
from src.modules.aseguradora.presentation.talleres import taller_dependencies
from src.modules.aseguradora.presentation.usuarios import usuario_dependencies

from tests.fakes.aseguradora import FakeAjustadorCrudRepo, FakeClienteAseguradoraRepo, FakeTallerCrudRepo, FakeUsuarioRepo
from tests.fakes.auth import FakeAuthRepo, FakePasswordService, FakeUser

BASE = "/api/v1/aseguradora/crud"


class FakeAjustadorAdapter:
    def __init__(self, ajustador_repo, auth_repo, password_service):
        self.repo = ajustador_repo
        self.auth_repo = auth_repo
        self.password_service = password_service

    def crear(self, aseguradora_id, nombre, email, telefono, password_temporal, cedula_profesional):
        usuario_id = str(uuid4())
        self.auth_repo.create(FakeUser(
            usuario_id=usuario_id, nombre=nombre, email=email,
            password_hash=self.password_service.hash(password_temporal),
            rol="Ajustador", aseguradora_id=aseguradora_id,
        ))
        model = FakeAjustadorModel(
            id=str(uuid4()), usuario_id=usuario_id, cedula_profesional=cedula_profesional,
            geolocalizacion_actual=None, activo_para_servicio=True,
            version=1, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
            aseguradora_id=aseguradora_id,
        )
        return self.repo.save(model)

    def obtener(self, ajustador_id):
        a = self.repo.get_by_id(ajustador_id)
        if not a:
            raise type("NotFound", (Exception,), {})()

        return a

    def listar(self, aseguradora_id, offset=0, limit=20, activo_para_servicio=None):
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit, activo_para_servicio)

    def actualizar(self, ajustador_id, cedula_profesional, activo_para_servicio):
        a = self.repo.get_by_id(ajustador_id)
        if not a:
            raise type("NotFound", (Exception,), {})()
        if cedula_profesional is not None:
            a.cedula_profesional = cedula_profesional
        if activo_para_servicio is not None:
            a.activo_para_servicio = activo_para_servicio
        a.updated_at = datetime.now()
        return self.repo.update(a)

    def eliminar(self, ajustador_id):
        a = self.repo.get_by_id(ajustador_id)
        if not a:
            raise type("NotFound", (Exception,), {})()
        self.repo.delete(ajustador_id)


@dataclass
class FakeAjustadorModel:
    id: str
    usuario_id: str
    cedula_profesional: str
    geolocalizacion_actual: tuple | None
    activo_para_servicio: bool
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    aseguradora_id: str | None = None


class FakeClienteModuleAdapter:
    def __init__(self, cliente_repo, auth_repo, password_service):
        self.repo = cliente_repo
        self.auth_repo = auth_repo
        self.password_service = password_service

    def crear(self, aseguradora_id, nombre, email, telefono, password_temporal):
        usuario_id = str(uuid4())
        self.auth_repo.create(FakeUser(
            usuario_id=usuario_id, nombre=nombre, email=email,
            password_hash=self.password_service.hash(password_temporal),
            rol="Cliente", aseguradora_id=aseguradora_id,
        ))
        model = FakeClienteModel(
            id=str(uuid4()), usuario_id=usuario_id, numero_poliza="POL-NEW",
            vigencia_poliza=__import__('datetime').date(2030, 12, 31),
            curp_rfc_cifrado="cifrado", consentimiento_aviso_privacidad=False,
            consentimiento_biometria=False, autoriza_transferencia_talleres=False,
            fecha_consentimiento=None, version=1,
            created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
            aseguradora_id=aseguradora_id,
        )
        return self.repo.save(model)

    def obtener(self, cliente_id):
        c = self.repo.get_by_id(cliente_id)
        if not c:
            raise type("NotFound", (Exception,), {})()
        return c

    def listar(self, aseguradora_id, offset=0, limit=20):
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit)


@dataclass
class FakeClienteModel:
    id: str
    usuario_id: str
    numero_poliza: str
    vigencia_poliza: object
    curp_rfc_cifrado: str
    consentimiento_aviso_privacidad: bool
    consentimiento_biometria: bool
    autoriza_transferencia_talleres: bool
    fecha_consentimiento: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    aseguradora_id: str | None = None


class FakeTallerModuleAdapter:
    def __init__(self, taller_repo, auth_repo, password_service):
        self.repo = taller_repo
        self.auth_repo = auth_repo
        self.password_service = password_service

    def crear(self, aseguradora_id, nombre_comercial, rfc, direccion_tecnica, telefono_contacto):
        model = FakeTallerModel(
            id=str(uuid4()), nombre_comercial=nombre_comercial, rfc=rfc,
            direccion_tecnica=direccion_tecnica, telefono_contacto=telefono_contacto,
            version=1, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc),
            aseguradora_id=aseguradora_id,
        )
        return self.repo.save(model)

    def obtener(self, taller_id):
        t = self.repo.get_by_id(taller_id)
        if not t:
            raise type("NotFound", (Exception,), {})()
        return t

    def listar(self, aseguradora_id, offset=0, limit=20):
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit)

    def actualizar(self, taller_id, nombre_comercial, direccion_tecnica, telefono_contacto):
        t = self.repo.get_by_id(taller_id)
        if not t:
            raise type("NotFound", (Exception,), {})()
        if nombre_comercial is not None:
            t.nombre_comercial = nombre_comercial
        if direccion_tecnica is not None:
            t.direccion_tecnica = direccion_tecnica
        if telefono_contacto is not None:
            t.telefono_contacto = telefono_contacto
        t.updated_at = datetime.now()
        return self.repo.update(t)

    def eliminar(self, taller_id, aseguradora_id):
        t = self.repo.get_by_id(taller_id)
        if not t:
            raise type("NotFound", (Exception,), {})()
        self.repo.delete(taller_id, aseguradora_id)

    def crear_operador(self, aseguradora_id, admin_id, taller_id, data):
        return {"id": str(uuid4()), "taller_id": taller_id, "email": data.email}


@dataclass
class FakeTallerModel:
    id: str
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    aseguradora_id: str | None = None


@pytest.fixture
def wired(client):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="op-1", email="op@aseg.mx", rol="Operador_Aseguradora", aseguradora_id="aseg-1"
    )

    ajustador_repo = FakeAjustadorCrudRepo()
    cliente_repo = FakeClienteAseguradoraRepo()
    taller_repo = FakeTallerCrudRepo()
    usuario_repo = FakeUsuarioRepo()
    auth_repo = FakeAuthRepo()
    pw_svc = FakePasswordService()

    ajustador_adapter = FakeAjustadorAdapter(ajustador_repo, auth_repo, pw_svc)
    cliente_adapter = FakeClienteModuleAdapter(cliente_repo, auth_repo, pw_svc)
    taller_adapter = FakeTallerModuleAdapter(taller_repo, auth_repo, pw_svc)

    from src.modules.aseguradora.application.ajustadores.create_ajustador import CreateAjustador
    from src.modules.aseguradora.application.ajustadores.list_ajustadores import ListAjustadores
    from src.modules.aseguradora.application.ajustadores.get_ajustador import GetAjustador
    from src.modules.aseguradora.application.ajustadores.update_ajustador import UpdateAjustador
    from src.modules.aseguradora.application.ajustadores.delete_ajustador import DeleteAjustador
    from src.modules.aseguradora.application.clientes.create_cliente import CreateClienteByAseguradora
    from src.modules.aseguradora.application.clientes.list_clientes import ListClientes
    from src.modules.aseguradora.application.clientes.get_cliente import GetCliente
    from src.modules.aseguradora.application.talleres.create_taller import CreateTaller
    from src.modules.aseguradora.application.talleres.list_talleres import ListTalleres
    from src.modules.aseguradora.application.talleres.get_taller import GetTaller
    from src.modules.aseguradora.application.talleres.update_taller import UpdateTaller
    from src.modules.aseguradora.application.talleres.delete_taller import DeleteTaller
    from src.modules.aseguradora.application.talleres.create_taller_user import CreateOperadorTallerUseCase
    from src.modules.aseguradora.application.usuarios.bloqueo_arco import BloqueoArcoAseguradora
    from src.modules.aseguradora.application.usuarios.desbloqueo_arco import DesbloqueoArcoAseguradora

    app.dependency_overrides[ajustador_dependencies.create_ajustador_service] = lambda: CreateAjustador(ajustador_adapter)
    app.dependency_overrides[ajustador_dependencies.list_ajustadores_service] = lambda: ListAjustadores(ajustador_adapter)
    app.dependency_overrides[ajustador_dependencies.get_ajustador_service] = lambda: GetAjustador(ajustador_adapter)
    app.dependency_overrides[ajustador_dependencies.update_ajustador_service] = lambda: UpdateAjustador(ajustador_adapter)
    app.dependency_overrides[ajustador_dependencies.delete_ajustador_service] = lambda: DeleteAjustador(ajustador_adapter)
    app.dependency_overrides[cliente_dependencies.create_cliente_service] = lambda: CreateClienteByAseguradora(cliente_adapter)
    app.dependency_overrides[cliente_dependencies.list_clientes_service] = lambda: ListClientes(cliente_adapter)
    app.dependency_overrides[cliente_dependencies.get_cliente_service] = lambda: GetCliente(cliente_adapter)
    app.dependency_overrides[taller_dependencies.create_taller_service] = lambda: CreateTaller(taller_adapter)
    app.dependency_overrides[taller_dependencies.list_talleres_service] = lambda: ListTalleres(taller_adapter)
    app.dependency_overrides[taller_dependencies.get_taller_service] = lambda: GetTaller(taller_adapter)
    app.dependency_overrides[taller_dependencies.update_taller_service] = lambda: UpdateTaller(taller_adapter)
    app.dependency_overrides[taller_dependencies.delete_taller_service] = lambda: DeleteTaller(taller_adapter)
    app.dependency_overrides[taller_dependencies.crear_operador_taller_service] = lambda: CreateOperadorTallerUseCase(taller_adapter)
    app.dependency_overrides[usuario_dependencies.bloqueo_arco_service] = lambda: BloqueoArcoAseguradora(usuario_repo)
    app.dependency_overrides[usuario_dependencies.desbloqueo_arco_service] = lambda: DesbloqueoArcoAseguradora(usuario_repo)

    return {
        "client": client,
        "ajustador_repo": ajustador_repo,
        "cliente_repo": cliente_repo,
        "taller_repo": taller_repo,
        "usuario_repo": usuario_repo,
    }


# ── Ajustadores ────────────────────────────────────────────────────────────

def test_crear_ajustador(wired):
    r = wired["client"].post(f"{BASE}/ajustadores", json={
        "nombre": "Ajustador 1", "email": "aj1@aseg.mx", "telefono": "555",
        "password_temporal": "temp123", "cedula_profesional": "CED-001",
    })
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["cedula_profesional"] == "CED-001"
    assert body["activo_para_servicio"] is True


def test_listar_ajustadores(wired):
    wired["client"].post(f"{BASE}/ajustadores", json={
        "nombre": "A1", "email": "a1@x.mx", "telefono": "555",
        "password_temporal": "t", "cedula_profesional": "C1",
    })
    r = wired["client"].get(f"{BASE}/ajustadores?page=1&page_size=10")
    assert r.status_code == 200, r.text
    assert r.json()["total"] >= 1


def test_obtener_ajustador(wired):
    created = wired["client"].post(f"{BASE}/ajustadores", json={
        "nombre": "A2", "email": "a2@x.mx", "telefono": "555",
        "password_temporal": "t", "cedula_profesional": "C2",
    }).json()
    r = wired["client"].get(f"{BASE}/ajustadores/{created['id']}")
    assert r.status_code == 200, r.text
    assert r.json()["id"] == created["id"]


def test_actualizar_ajustador(wired):
    created = wired["client"].post(f"{BASE}/ajustadores", json={
        "nombre": "A3", "email": "a3@x.mx", "telefono": "555",
        "password_temporal": "t", "cedula_profesional": "C3",
    }).json()
    r = wired["client"].put(f"{BASE}/ajustadores/{created['id']}", json={
        "cedula_profesional": "CED-NEW", "activo_para_servicio": False,
    })
    assert r.status_code == 200, r.text
    assert r.json()["cedula_profesional"] == "CED-NEW"
    assert r.json()["activo_para_servicio"] is False


def test_eliminar_ajustador(wired):
    created = wired["client"].post(f"{BASE}/ajustadores", json={
        "nombre": "A4", "email": "a4@x.mx", "telefono": "555",
        "password_temporal": "t", "cedula_profesional": "C4",
    }).json()
    r = wired["client"].delete(f"{BASE}/ajustadores/{created['id']}")
    assert r.status_code == 204, r.text


# ── Clientes ───────────────────────────────────────────────────────────────

def test_crear_cliente(wired):
    r = wired["client"].post(f"{BASE}/clientes", json={
        "nombre": "Cliente 1", "email": "cli1@aseg.mx", "telefono": "555",
        "password_temporal": "temp123",
    })
    assert r.status_code == 201, r.text
    body = r.json()
    assert "id" in body


def test_listar_clientes(wired):
    wired["client"].post(f"{BASE}/clientes", json={
        "nombre": "C1", "email": "c1@x.mx", "telefono": "555", "password_temporal": "t",
    })
    r = wired["client"].get(f"{BASE}/clientes?page=1&page_size=10")
    assert r.status_code == 200, r.text
    assert r.json()["total"] >= 1


def test_obtener_cliente(wired):
    created = wired["client"].post(f"{BASE}/clientes", json={
        "nombre": "C2", "email": "c2@x.mx", "telefono": "555", "password_temporal": "t",
    }).json()
    r = wired["client"].get(f"{BASE}/clientes/{created['id']}")
    assert r.status_code == 200, r.text
    assert r.json()["id"] == created["id"]


# ── Talleres ───────────────────────────────────────────────────────────────

def test_crear_taller(wired):
    r = wired["client"].post(f"{BASE}/talleres", json={
        "nombre_comercial": "Taller 1", "rfc": "TAL123456789",
        "direccion_tecnica": "Calle 123", "telefono_contacto": "555-1234",
    })
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["nombre_comercial"] == "Taller 1"


def test_listar_talleres(wired):
    wired["client"].post(f"{BASE}/talleres", json={
        "nombre_comercial": "T1", "rfc": "RFC1", "direccion_tecnica": "D1", "telefono_contacto": "T",
    })
    r = wired["client"].get(f"{BASE}/talleres?page=1&page_size=10")
    assert r.status_code == 200, r.text
    assert r.json()["total"] >= 1


def test_obtener_taller(wired):
    created = wired["client"].post(f"{BASE}/talleres", json={
        "nombre_comercial": "T2", "rfc": "RFC2", "direccion_tecnica": "D2", "telefono_contacto": "T",
    }).json()
    r = wired["client"].get(f"{BASE}/talleres/{created['id']}")
    assert r.status_code == 200, r.text


def test_actualizar_taller(wired):
    created = wired["client"].post(f"{BASE}/talleres", json={
        "nombre_comercial": "T3", "rfc": "RFC3", "direccion_tecnica": "D3", "telefono_contacto": "T",
    }).json()
    r = wired["client"].put(f"{BASE}/talleres/{created['id']}", json={
        "nombre_comercial": "Taller Actualizado",
    })
    assert r.status_code == 200, r.text
    assert r.json()["nombre_comercial"] == "Taller Actualizado"


def test_eliminar_taller(wired):
    created = wired["client"].post(f"{BASE}/talleres", json={
        "nombre_comercial": "T4", "rfc": "RFC4", "direccion_tecnica": "D4", "telefono_contacto": "T",
    }).json()
    r = wired["client"].delete(f"{BASE}/talleres/{created['id']}")
    assert r.status_code == 204, r.text


def test_crear_operador_taller(wired):
    created = wired["client"].post(f"{BASE}/talleres", json={
        "nombre_comercial": "T5", "rfc": "RFC5", "direccion_tecnica": "D5", "telefono_contacto": "T",
    }).json()
    r = wired["client"].post(f"{BASE}/talleres/{created['id']}/operadores", json={
        "nombre": "Operador T", "email": "op@taller.mx", "password": "securePass1",
    })
    assert r.status_code == 201, r.text


# ── ARCO ───────────────────────────────────────────────────────────────────

def test_bloqueo_arco_aseguradora(wired):
    wired["usuario_repo"].users["user-arco"] = {"id": "user-arco", "aseguradora_id": "aseg-1"}
    r = wired["client"].post(f"{BASE}/usuarios/user-arco/bloqueo-arco")
    assert r.status_code == 200, r.text


def test_desbloqueo_arco_aseguradora(wired):
    wired["usuario_repo"].users["user-arco2"] = {"id": "user-arco2", "aseguradora_id": "aseg-1"}
    r = wired["client"].post(f"{BASE}/usuarios/user-arco2/desbloqueo-arco")
    assert r.status_code == 200, r.text


# ── Roles ──────────────────────────────────────────────────────────────────

def test_rol_no_operador_rechazado(wired):
    app.dependency_overrides[get_current_user] = lambda: AuthenticatedUser(
        usuario_id="u-cli", email="cli@x.mx", rol="Cliente", aseguradora_id="aseg-1"
    )
    r = wired["client"].get(f"{BASE}/ajustadores")
    assert r.status_code == 403, r.text
