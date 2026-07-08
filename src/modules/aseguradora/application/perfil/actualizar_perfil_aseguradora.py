from src.core.exceptions import NotFoundError
from datetime import datetime, timezone


class ActualizarPerfilAseguradora:
    def __init__(self, aseguradora_repo, auth_repo):
        self.aseguradora_repo = aseguradora_repo
        self.auth_repo = auth_repo

    def execute(self, aseguradora_id: str, usuario_id: str, nombre=None, rfc=None,
                dominio_correo=None, contacto_legal_email=None,
                operador_nombre=None, operador_email=None, operador_telefono=None):
        aseg = self.aseguradora_repo.get_by_id(aseguradora_id)
        if not aseg:
            raise NotFoundError("Aseguradora no encontrada.")

        if nombre is not None:
            aseg.nombre = nombre
        if rfc is not None:
            aseg.rfc = rfc
        if dominio_correo is not None:
            aseg.dominio_correo = dominio_correo
        if contacto_legal_email is not None:
            aseg.contacto_legal_email = contacto_legal_email
        aseg.updated_at = datetime.now(timezone.utc)
        self.aseguradora_repo.update(aseg)

        self.auth_repo.update_user_profile(usuario_id, nombre=operador_nombre, email=operador_email, telefono=operador_telefono)

        return self.aseguradora_repo.get_by_id(aseguradora_id)
