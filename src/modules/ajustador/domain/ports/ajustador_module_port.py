from typing import Protocol, List, Tuple
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel

class AjustadorModulePort(Protocol):
    def crear(
        self,
        aseguradora_id: str,
        nombre: str,
        email: str,
        telefono: str,
        password_temporal: str,
        cedula_profesional: str,
    ) -> AjustadorModel: ...

    def obtener(self, ajustador_id: str) -> AjustadorModel: ...

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        activo_para_servicio: bool | None = None,
    ) -> Tuple[List[AjustadorModel], int]: ...

    def actualizar(
        self,
        ajustador_id: str,
        cedula_profesional: str | None,
        activo_para_servicio: bool | None,
    ) -> AjustadorModel: ...

    def eliminar(self, ajustador_id: str) -> None: ...
