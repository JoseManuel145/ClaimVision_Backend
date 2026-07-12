from fastapi import Depends
from src.core.database import get_session
from sqlalchemy.orm import Session
from src.modules.aseguradora.infra.db.repositories.vehiculo_repository import VehiculoRepository
from src.modules.aseguradora.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.aseguradora.infra.adapters.vehiculo_adapter import VehiculoAdapter
from src.modules.aseguradora.application.vehiculos.create_vehiculo import CreateVehiculo
from src.modules.aseguradora.application.vehiculos.list_vehiculos import ListVehiculos
from src.modules.aseguradora.application.vehiculos.get_vehiculo import GetVehiculo
from src.modules.aseguradora.application.vehiculos.update_vehiculo import UpdateVehiculo
from src.modules.aseguradora.application.vehiculos.delete_vehiculo import DeleteVehiculo


def _adapter(session: Session = Depends(get_session)) -> VehiculoAdapter:
    return VehiculoAdapter(
        vehiculo_repo=VehiculoRepository(session),
        cliente_repo=ClienteRepository(session),
    )


def create_vehiculo_service(module: VehiculoAdapter = Depends(_adapter)) -> CreateVehiculo:
    return CreateVehiculo(module)


def list_vehiculos_service(module: VehiculoAdapter = Depends(_adapter)) -> ListVehiculos:
    return ListVehiculos(module)


def get_vehiculo_service(module: VehiculoAdapter = Depends(_adapter)) -> GetVehiculo:
    return GetVehiculo(module)


def update_vehiculo_service(module: VehiculoAdapter = Depends(_adapter)) -> UpdateVehiculo:
    return UpdateVehiculo(module)


def delete_vehiculo_service(module: VehiculoAdapter = Depends(_adapter)) -> DeleteVehiculo:
    return DeleteVehiculo(module)
