from src.modules.cliente.domain.module_port import ClienteModulePort
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel
from src.modules.aseguradora.presentation.clientes.cliente_dto import ClienteUpdateDTO


class UpdateCliente:
    def __init__(self, module: ClienteModulePort):
        self.module = module

    def execute(self, cliente_id: str, dto: ClienteUpdateDTO) -> ClienteModel:
        return self.module.actualizar(
            cliente_id=cliente_id,
            nombre=dto.nombre,
            email=dto.email,
            telefono=dto.telefono,
            numero_poliza=dto.numero_poliza,
            vigencia_poliza=dto.vigencia_poliza,
        )
