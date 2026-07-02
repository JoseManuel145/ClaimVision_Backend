from typing import Protocol, List, Tuple
from src.modules.aseguradora.domain.models.taller_model import TallerModel

class TallerModulePort(Protocol):
    def crear(
        self,
        aseguradora_id: str,
        nombre_comercial: str,
        rfc: str,
        direccion_tecnica: str,
        telefono_contacto: str,
    ) -> TallerModel: ...

    def obtener(self, taller_id: str) -> TallerModel: ...

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[TallerModel], int]: ...

    def actualizar(
        self,
        taller_id: str,
        nombre_comercial: str | None,
        direccion_tecnica: str | None,
        telefono_contacto: str | None,
    ) -> TallerModel: ...

    def eliminar(self, taller_id: str, aseguradora_id: str) -> None: ...

    def crear_operador(
        self,
        aseguradora_id: str,
        admin_id: str,
        taller_id: str,
        data,
    ) -> dict: ...
