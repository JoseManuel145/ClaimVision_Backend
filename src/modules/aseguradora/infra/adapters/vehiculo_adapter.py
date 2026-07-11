from datetime import datetime
from typing import List, Tuple

from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel
from src.modules.aseguradora.domain.ports.vehiculo_repository_port import VehiculoRepositoryPort
from src.core.exceptions import NotFoundError


class VehiculoAdapter(VehiculoModulePort):
    def __init__(self, vehiculo_repo: VehiculoRepositoryPort):
        self.vehiculo_repo = vehiculo_repo

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
    ) -> VehiculoModel:
        model = VehiculoModel(
            id="",
            aseguradora_id=aseguradora_id,
            cliente_id=cliente_id,
            marca=marca,
            modelo=modelo,
            anio=anio,
            placas=placas,
            vin=vin,
            color=color,
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return self.vehiculo_repo.save(model)

    def obtener(self, vehiculo_id: str) -> VehiculoModel:
        vehiculo = self.vehiculo_repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise NotFoundError("Vehiculo no encontrado")
        return vehiculo

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        cliente_id: str | None = None,
    ) -> Tuple[List[VehiculoModel], int]:
        return self.vehiculo_repo.list_by_aseguradora(aseguradora_id, offset, limit, cliente_id)

    def listar_por_cliente(
        self,
        cliente_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[VehiculoModel], int]:
        return self.vehiculo_repo.list_by_cliente(cliente_id, offset, limit)

    def actualizar(
        self,
        vehiculo_id: str,
        marca: str | None,
        modelo: str | None,
        anio: int | None,
        placas: str | None,
        vin: str | None,
        color: str | None,
    ) -> VehiculoModel:
        vehiculo = self.vehiculo_repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise NotFoundError("Vehiculo no encontrado")

        if marca is not None:
            vehiculo.marca = marca
        if modelo is not None:
            vehiculo.modelo = modelo
        if anio is not None:
            vehiculo.anio = anio
        if placas is not None:
            vehiculo.placas = placas
        if vin is not None:
            vehiculo.vin = vin
        if color is not None:
            vehiculo.color = color
        vehiculo.updated_at = datetime.now()
        return self.vehiculo_repo.update(vehiculo)

    def eliminar(self, vehiculo_id: str) -> None:
        vehiculo = self.vehiculo_repo.get_by_id(vehiculo_id)
        if not vehiculo:
            raise NotFoundError("Vehiculo no encontrado")
        self.vehiculo_repo.delete(vehiculo_id)
