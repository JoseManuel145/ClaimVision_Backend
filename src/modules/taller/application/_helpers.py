from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.core.exceptions import ForbiddenError


def taller_id(perfil_repo: PerfilTallerRepositoryPort, usuario_id: str) -> str:
    id_ = perfil_repo.get_taller_id_by_usuario(usuario_id)
    if not id_:
        raise ForbiddenError("El usuario no tiene un perfil de taller asignado.")
    return id_
