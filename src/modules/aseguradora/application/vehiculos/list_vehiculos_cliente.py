from typing import List, Tuple
from src.modules.aseguradora.domain.ports.vehiculo_module_port import VehiculoModulePort
from src.modules.aseguradora.domain.models.vehiculo_model import VehiculoModel
from src.modules.siniestro.domain.ports.cliente_checker_port import ClienteCheckerPort
from src.core.exceptions import BusinessRuleError


class ListVehiculosCliente:
    def __init__(self, vehiculo_module: VehiculoModulePort, cliente_checker: ClienteCheckerPort):
        self.vehiculo_module = vehiculo_module
        self.cliente_checker = cliente_checker

    def execute(
        self,
        usuario_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[VehiculoModel], int]:
        perfil_cliente_id = self.cliente_checker.get_perfil_cliente_id_by_usuario(usuario_id)
        if not perfil_cliente_id:
            raise BusinessRuleError("Debe completar su registro de poliza (Onboarding) para ver sus vehiculos.")
        return self.vehiculo_module.listar_por_cliente(perfil_cliente_id, offset, limit)
