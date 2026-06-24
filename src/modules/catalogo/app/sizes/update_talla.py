from src.modules.catalogo.domain.models import TallaModel
from src.modules.catalogo.domain.ports import TallaPort
from src.modules.catalogo.presentation.sizes.talla_dto import TallaUpdateDTO


class UpdateTalla:
    def __init__(self, repo: TallaPort):
        self.repo = repo

    def execute(self, talla_id: int, dto: TallaUpdateDTO) -> TallaModel:
        current = self.repo.get_by_id(talla_id)
        if not current:
            raise ValueError(f"Talla id {talla_id} no existe")
        current.nombre = dto.nombre
        return self.repo.update(talla_id, current)
