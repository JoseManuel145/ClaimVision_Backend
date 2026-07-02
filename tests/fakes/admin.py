"""Fakes del módulo Admin."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class FakeAseguradoraRepo:
    def __init__(self):
        self.items: dict[str, dict] = {}

    def save(self, aseguradora: Any):
        self.items[aseguradora.id] = aseguradora
        return aseguradora

    def get_by_id(self, id: str):
        return self.items.get(id)

    def update(self, aseguradora: Any):
        self.items[aseguradora.id] = aseguradora
        return aseguradora

    def list_all(self, offset=0, limit=20, include_deleted=False) -> Tuple[List[Any], int]:
        rows = list(self.items.values())
        if not include_deleted:
            rows = [r for r in rows if getattr(r, "deleted_at", None) is None and getattr(r, "estatus_comercial", None) != "Cancelado"]
        total = len(rows)
        return rows[offset: offset + limit], total

    def desincorporar(self, id: str):
        if id in self.items:
            self.items[id].deleted_at = datetime.now(timezone.utc)
            self.items[id].estatus_comercial = "Cancelado"
        return self.items.get(id)

    def find_by_rfc(self, rfc: str):
        for item in self.items.values():
            if item.rfc == rfc:
                return item
        return None


class FakeAuditLogRepo:
    def __init__(self):
        self.logs: List[Any] = []

    def append(self, log: Any):
        self.logs.append(log)

    def list_logs(self, offset=0, limit=20) -> Tuple[List[Any], int]:
        total = len(self.logs)
        return self.logs[offset: offset + limit], total

    def get_by_entity(self, entidad_afectada: str) -> List[Any]:
        return [l for l in self.logs if hasattr(l, "entidad_afectada") and l.entidad_afectada == entidad_afectada]


class FakeAdminUserRepo:
    def __init__(self):
        self.users: dict[str, dict] = {}

    def get_by_id(self, usuario_id: str):
        return self.users.get(usuario_id)

    def bloquear_por_arco(self, usuario_id: str):
        if usuario_id in self.users:
            self.users[usuario_id]["bloqueado_arco"] = True

    def block_all_users_from_tenant(self, tenant_id: str):
        pass
