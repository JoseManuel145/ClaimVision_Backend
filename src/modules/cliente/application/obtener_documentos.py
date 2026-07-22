from src.modules.cliente.domain.ports import ClienteDocumentoRepositoryPort, ClienteRepositoryPort

class ObtenerDocumentos:
    def __init__(self, doc_repo: ClienteDocumentoRepositoryPort, profile_repo: ClienteRepositoryPort):
        self.doc_repo = doc_repo
        self.profile_repo = profile_repo

    def execute(self, usuario_id: str) -> dict:
        doc = self.doc_repo.get_by_usuario_id(usuario_id)
        profile = self.profile_repo.get_by_usuario_id(usuario_id)

        if not doc:
            return {
                "identificacion": None,
                "poliza": None
            }

        identificacion = None
        if doc.identificacion_url:
            identificacion = {
                "url": doc.identificacion_url,
                "tipo": doc.identificacion_tipo,
                "subido_en": doc.identificacion_subido_en
            }

        poliza = None
        if doc.poliza_url:
            poliza = {
                "url": doc.poliza_url,
                "tipo": doc.poliza_tipo,
                "numero_poliza": profile.numero_poliza if profile else None,
                "vigencia": profile.vigencia_poliza if profile else None,
                "subido_en": doc.poliza_subido_en
            }

        return {
            "identificacion": identificacion,
            "poliza": poliza
        }
