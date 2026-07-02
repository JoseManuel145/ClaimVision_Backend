from src.modules.cliente.domain.module_port import ClienteModulePort
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel


class GetCliente:
    def __init__(self, cliente_module: ClienteModulePort):
        self.cliente_module = cliente_module

    def execute(self, id: str) -> ClienteModel:
        return self.cliente_module.obtener(id)
