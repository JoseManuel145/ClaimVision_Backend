from src.modules.cliente.domain.module_port import ClienteModulePort
from src.modules.cliente.domain.models import ClienteProfile
from src.modules.aseguradora.presentation.clientes.cliente_dto import ClienteCreateDTO


class CreateClienteByAseguradora:
    def __init__(self, cliente_module: ClienteModulePort):
        self.cliente_module = cliente_module

    def execute(self, aseguradora_id: str, dto: ClienteCreateDTO) -> ClienteProfile:
        return self.cliente_module.crear(
            aseguradora_id=aseguradora_id,
            nombre=dto.nombre,
            email=dto.email,
            telefono=dto.telefono,
            password_temporal=dto.password_temporal,
        )
