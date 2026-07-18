from fastapi import Depends
from src.core.database import get_session
from sqlalchemy.orm import Session
from src.modules.aseguradora.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.aseguradora.infra.adapters.cliente_adapter import ClienteAdapter
from src.modules.aseguradora.application.clientes.list_clientes import ListClientes
from src.modules.aseguradora.application.clientes.get_cliente import GetCliente
from src.modules.aseguradora.application.clientes.create_cliente import CreateClienteByAseguradora
from src.modules.aseguradora.application.clientes.update_cliente import UpdateCliente
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository as ClienteModuleRepository


def _adapter(session: Session = Depends(get_session)) -> ClienteAdapter:
    return ClienteAdapter(
        auth_repo=AuthRepository(session),
        cliente_repo=ClienteRepository(session),
        cliente_module_repo=ClienteModuleRepository(session),
        password_service=PasswordService(),
    )


def create_cliente_service(module: ClienteAdapter = Depends(_adapter)) -> CreateClienteByAseguradora:
    return CreateClienteByAseguradora(module)


def list_clientes_service(module: ClienteAdapter = Depends(_adapter)) -> ListClientes:
    return ListClientes(module)


def get_cliente_service(module: ClienteAdapter = Depends(_adapter)) -> GetCliente:
    return GetCliente(module)


def update_cliente_service(module: ClienteAdapter = Depends(_adapter)) -> UpdateCliente:
    return UpdateCliente(module)
