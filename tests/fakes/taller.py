"""Fakes del módulo Taller."""


class FakePerfilTallerRepo:
    def __init__(self, mapping: dict[str, str]):
        self.mapping = mapping

    def get_taller_id_by_usuario(self, usuario_id: str):
        return self.mapping.get(usuario_id)
