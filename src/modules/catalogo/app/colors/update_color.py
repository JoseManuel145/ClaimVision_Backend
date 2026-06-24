from src.modules.catalogo.domain.models import ColorModel
from src.modules.catalogo.domain.ports import ColorPort
from src.modules.catalogo.presentation.colors.color_dto import ColorUpdateDTO


class UpdateColor:
    def __init__(self, repo: ColorPort):
        self.repo = repo

    def execute(self, color_id: int, dto: ColorUpdateDTO) -> ColorModel:
        current = self.repo.get_by_id(color_id)
        if not current:
            raise ValueError(f"Color id {color_id} no existe")
        current.nombre = dto.nombre
        return self.repo.update(color_id, current)
