from fastapi import Depends
from src.core.database import get_session
from src.modules.aseguradora.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.aseguradora.application.clientes.list_clientes import ListClientes
from src.modules.aseguradora.application.clientes.get_cliente import GetCliente
from src.modules.aseguradora.application.clientes.create_cliente import CreateClienteByAseguradora
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository as ClienteModuleRepository

def cliente_repo(session=Depends(get_session)) -> ClienteRepository:
    return ClienteRepository(session)

def list_clientes_service(repo: ClienteRepository = Depends(cliente_repo)) -> ListClientes:
    return ListClientes(repo)

def get_cliente_service(repo: ClienteRepository = Depends(cliente_repo)) -> GetCliente:
    return GetCliente(repo)

def create_cliente_service(session=Depends(get_session)) -> CreateClienteByAseguradora:
    auth_repo = AuthRepository(session)
    cliente_module_repo = ClienteModuleRepository(session)
    password_service = PasswordService()
    return CreateClienteByAseguradora(auth_repo, cliente_module_repo, password_service)
