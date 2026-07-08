from src.core.exceptions import NotFoundError, ForbiddenError
from datetime import datetime, timezone


class ActualizarPerfilTaller:
    def __init__(self, perfil_taller_repo, taller_repo, auth_repo):
        self.perfil_taller_repo = perfil_taller_repo
        self.taller_repo = taller_repo
        self.auth_repo = auth_repo

    def execute(self, usuario_id: str, nombre_comercial=None, direccion_tecnica=None,
                telefono_contacto=None, nombre=None, email=None, telefono=None):
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise ForbiddenError("El usuario no tiene un perfil de taller asignado.")
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado.")

        if nombre_comercial is not None:
            taller.nombre_comercial = nombre_comercial
        if direccion_tecnica is not None:
            taller.direccion_tecnica = direccion_tecnica
        if telefono_contacto is not None:
            taller.telefono_contacto = telefono_contacto
        taller.updated_at = datetime.now(timezone.utc)
        self.taller_repo.update(taller)

        self.auth_repo.update_user_profile(usuario_id, nombre=nombre, email=email, telefono=telefono)

        taller = self.taller_repo.get_by_id(taller_id)
        user_data = self.auth_repo.get_by_id(usuario_id)
        return taller, user_data
