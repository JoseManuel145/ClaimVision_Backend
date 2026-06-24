from src.modules.catalogo.domain.models import ColorModel
from src.modules.catalogo.domain.ports import ColorPort
from src.modules.catalogo.presentation.colors.color_dto import ColorCreateDTO


class CreateColor:
    def __init__(self, repo: ColorPort):
        self.repo = repo

    def execute(self, dto: ColorCreateDTO) -> ColorModel:
        model = ColorModel(
            color_id=None,
            nombre=dto.nombre
        )
        return self.repo.create(model)
