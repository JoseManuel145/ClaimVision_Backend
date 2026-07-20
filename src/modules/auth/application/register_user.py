from src.modules.auth.domain.ports import AuthPort, PasswordPort, TokenPort
from src.modules.auth.domain.models import User, TokenPayload
from src.core.exceptions import ConflictError
from datetime import datetime, timedelta, timezone
from src.shared.domain.models import Rol, EstadoUsuario
from uuid import uuid4

class RegisterUser:

    def __init__(
        self,
        auth_repo: AuthPort,
        password_port: PasswordPort,
        token_port: TokenPort,
        cliente_repo=None,
    ):
        self.auth_repo = auth_repo
        self.password_repo = password_port
        self.token_repo = token_port
        self.cliente_repo = cliente_repo

    async def execute(self, user: User):
        existing = self.auth_repo.get_by_email(user.email)
        if existing:
            raise ConflictError("Email already registered")

        hashed = self.password_repo.hash(user.password)

        model = User(
            usuario_id=str(uuid4()),
            nombre=user.nombre,
            email=user.email,
            rol=Rol.CLIENTE.value,
            fecha_creacion=datetime.now(timezone.utc),
            is_authenticated=False,
            estado=EstadoUsuario.ACTIVO.value,
            aseguradora_id=None,
            password=hashed,
            telefono="",
        )

        user_created = self.auth_repo.create(model)

        if self.cliente_repo and model.rol == Rol.CLIENTE.value:
            from src.modules.cliente.domain.models import ClienteProfile
            profile = ClienteProfile(
                id=str(uuid4()),
                usuario_id=model.usuario_id,
                numero_poliza="",
                vigencia_poliza=datetime.now(timezone.utc).date(),
                curp_rfc_cifrado="",
                consentimiento_aviso_privacidad=False,
                consentimiento_biometria=False,
                autoriza_transferencia_talleres=False,
                fecha_consentimiento=None,
                fecha_creacion=datetime.now(timezone.utc)
            )
            self.cliente_repo.save(profile)

        payload = TokenPayload(
            usuario_id=user_created.usuario_id,
            email=user_created.email,
            rol=user_created.rol,
            aseguradora_id=user_created.aseguradora_id,
            exp=datetime.now(timezone.utc) + timedelta(minutes=15),
        )

        token = self.token_repo.generate(payload)

        return {
            "token": token,
            "usuario_id": user_created.usuario_id,
            "email": user_created.email,
            "rol": user_created.rol,
            "aseguradora_id": user_created.aseguradora_id,
            "primer_cambio_password": False,
        }