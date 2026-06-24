from src.modules.catalogo.domain.ports import SeccionPort


class DeleteSeccion:
    def __init__(self, reop: SeccionPort):
        self.reop = reop

    def execute(self, seccion_id: int) -> None:
        return self.reop.delete_seccion(seccion_id)