from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.core.exceptions import BusinessRuleError


def resolver_ajustador_id(ajustador_repo: AjustadorRepositoryPort, usuario_id: str) -> str:
    ajustador = ajustador_repo.get_by_usuario_id(usuario_id)
    if not ajustador:
        raise BusinessRuleError("El usuario no tiene un perfil de ajustador.")
    return ajustador.id
