"""Fakes del módulo Aseguradora (CRUD: ajustadores, clientes, talleres, usuarios)."""
from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple


class FakeAjustadorCrudRepo:
    def __init__(self):
        self.items: dict[str, Any] = {}
        self.by_usuario: dict[str, Any] = {}

    def save(self, ajustador):
        self.items[ajustador.id] = ajustador
        self.by_usuario[ajustador.usuario_id] = ajustador
        return ajustador

    def get_by_id(self, id: str):
        return self.items.get(id)

    def get_by_usuario_id(self, usuario_id: str):
        return self.by_usuario.get(usuario_id)

    def update(self, ajustador):
        self.items[ajustador.id] = ajustador
        self.by_usuario[ajustador.usuario_id] = ajustador
        return ajustador

    def delete(self, id: str):
        self.items.pop(id, None)

    def list_by_aseguradora(self, aseguradora_id: str, offset=0, limit=20, activo_para_servicio=None):
        rows = [a for a in self.items.values() if a.aseguradora_id == aseguradora_id]
        if activo_para_servicio is not None:
            rows = [a for a in rows if a.activo_para_servicio == activo_para_servicio]
        total = len(rows)
        return rows[offset: offset + limit], total


class FakeClienteAseguradoraRepo:
    def __init__(self):
        self.items: dict[str, Any] = {}

    def save(self, cliente):
        self.items[cliente.id] = cliente
        return cliente

    def get_by_id(self, id: str):
        return self.items.get(id)

    def list_by_aseguradora(self, aseguradora_id: str, offset=0, limit=20):
        rows = [c for c in self.items.values() if c.aseguradora_id == aseguradora_id]
        total = len(rows)
        return rows[offset: offset + limit], total


class FakeTallerCrudRepo:
    def __init__(self):
        self.items: dict[str, Any] = {}

    def save(self, taller):
        self.items[taller.id] = taller
        return taller

    def get_by_id(self, id: str):
        return self.items.get(id)

    def update(self, taller):
        self.items[taller.id] = taller
        return taller

    def delete(self, id: str, aseguradora_id: str):
        self.items.pop(id, None)

    def list_by_aseguradora(self, aseguradora_id: str, offset=0, limit=20):
        rows = [t for t in self.items.values() if t.aseguradora_id == aseguradora_id]
        total = len(rows)
        return rows[offset: offset + limit], total


class FakeUsuarioRepo:
    def __init__(self):
        self.users: dict[str, dict] = {}

    def get_by_id(self, id: str):
        return self.users.get(id)

    def bloquear_arco(self, aseguradora_id: str, usuario_id: str):
        self.users[usuario_id] = {"bloqueado": True}

    def desbloquear_arco(self, aseguradora_id: str, usuario_id: str):
        self.users[usuario_id] = {"bloqueado": False}

    def bloquear_por_arco(self, id: str):
        self.users[id] = {"bloqueado": True}

    def desbloquear_por_arco(self, id: str):
        self.users[id] = {"bloqueado": False}

