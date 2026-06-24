from src.modules.catalogo.domain.ports import SeccionPort
from src.modules.catalogo.domain.models import SeccionModel
from src.modules.catalogo.presentation.section.seccion_dto import SeccionUpdate


class UpdateSeccion:
    def __init__(self, repo: SeccionPort):
        self.repo = repo

    def execute(self, seccion_id: int, dto: SeccionUpdate) -> SeccionModel | None:
        seccion = self.repo.get_seccion_by_id(seccion_id)
        if not seccion:
            raise ValueError(f'Seccion {seccion_id} no existe')
        seccion.nombre = dto.nombre
        return self.repo.update_seccion(seccion_id, seccion)