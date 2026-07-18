from typing import Protocol, List, Tuple
from src.modules.cliente.domain.models import ClienteProfile
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel


class ClienteModulePort(Protocol):
    def crear(
        self,
        aseguradora_id: str,
        nombre: str,
        email: str,
        telefono: str,
        password_temporal: str,
    ) -> ClienteProfile: ...

    def obtener(self, cliente_id: str) -> ClienteModel: ...

    def actualizar(
        self,
        cliente_id: str,
        nombre: str | None = None,
        email: str | None = None,
        telefono: str | None = None,
        numero_poliza: str | None = None,
        vigencia_poliza=None,
    ) -> ClienteModel: ...

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[ClienteModel], int]: ...
