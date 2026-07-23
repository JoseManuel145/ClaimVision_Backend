from src.core.exceptions import NotFoundError
from src.modules.cliente.domain.ports import ClienteDocumentoRepositoryPort


class GetDocumentosByClienteId:
    def __init__(self, doc_repo: ClienteDocumentoRepositoryPort):
        self.doc_repo = doc_repo

    def execute(self, usuario_id: str) -> dict:
        doc = self.doc_repo.get_by_usuario_id(usuario_id)

        if not doc:
            return {"identificacion": None, "poliza": None}

        identificacion = None
        if doc.identificacion_url:
            identificacion = {
                "url": doc.identificacion_url,
                "tipo": doc.identificacion_tipo,
                "subido_en": doc.identificacion_subido_en,
            }

        poliza = None
        if doc.poliza_url:
            poliza = {
                "url": doc.poliza_url,
                "tipo": doc.poliza_tipo,
                "subido_en": doc.poliza_subido_en,
            }

        return {"identificacion": identificacion, "poliza": poliza}
