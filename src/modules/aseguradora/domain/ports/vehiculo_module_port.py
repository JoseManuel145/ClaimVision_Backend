from typing import Protocol, List, Tuple
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel

class VehiculoModulePort(Protocol):
    def crear(
        self,
        aseguradora_id: str,
        cliente_id: str,
        marca: str,
        modelo: str,
        anio: int,
        placas: str,
        vin: str | None,
        color: str | None,
    ) -> VehiculoModel: ...

    def obtener(self, vehiculo_id: str) -> VehiculoModel: ...

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        cliente_id: str | None = None,
    ) -> Tuple[List[VehiculoModel], int]: ...

    def listar_por_cliente(
        self,
        cliente_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[VehiculoModel], int]: ...

    def actualizar(
        self,
        vehiculo_id: str,
        marca: str | None,
        modelo: str | None,
        anio: int | None,
        placas: str | None,
        vin: str | None,
        color: str | None,
    ) -> VehiculoModel: ...

    def eliminar(self, vehiculo_id: str) -> None: ...
