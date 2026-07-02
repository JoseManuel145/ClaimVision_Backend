from typing import List, Tuple
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.imagen_siniestro_repository_port import ImagenSiniestroRepositoryPort
from src.modules.siniestro.domain.ports.cliente_checker_port import ClienteCheckerPort
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


class GetSiniestroCliente:
    """
    Detalle de un siniestro para el cliente dueño, con sus imágenes. Valida la
    propiedad (el siniestro debe pertenecer al perfil del usuario autenticado).
    """

    def __init__(
        self,
        repo: SiniestroRepositoryPort,
        imagen_repo: ImagenSiniestroRepositoryPort,
        cliente_checker: ClienteCheckerPort,
    ):
        self.repo = repo
        self.imagen_repo = imagen_repo
        self.cliente_checker = cliente_checker

    def execute(self, usuario_id: str, siniestro_id: str) -> Tuple[SiniestroModel, List[ImagenSiniestroModel]]:
        perfil_cliente_id = self.cliente_checker.get_perfil_cliente_id_by_usuario(usuario_id)
        if not perfil_cliente_id:
            raise BusinessRuleError("El usuario no tiene un perfil de cliente (onboarding incompleto).")

        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.cliente_id != perfil_cliente_id:
            raise ForbiddenError("Este siniestro no pertenece al cliente autenticado.")

        imagenes = self.imagen_repo.get_by_siniestro_id(siniestro_id)
        return siniestro, imagenes
