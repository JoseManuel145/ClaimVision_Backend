from src.modules.auth.domain.ports import AuthPort, PasswordPort


class ChangePassword:

    def __init__(self, auth_repo: AuthPort, password_port: PasswordPort):
        self.auth_repo = auth_repo
        self.password_port = password_port

    async def execute(self, user_id: str, old_password: str, new_password: str):
        user = self.auth_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        if not self.password_port.verify(old_password, user.password):
            raise ValueError("La contraseña actual es incorrecta")

        new_hash = self.password_port.hash(new_password)
        self.auth_repo.update_password_with_flag(user_id, new_hash, primer_cambio=False)
