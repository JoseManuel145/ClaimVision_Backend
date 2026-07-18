import uuid
from datetime import datetime, timezone
from typing import List, Tuple

from sqlalchemy.exc import IntegrityError

from src.modules.taller.domain.ports.taller_module_port import TallerModulePort
from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.modules.admin.domain.ports import AuditLogRepositoryPort
from src.modules.auth.domain.ports import AuthPort, PasswordPort
from src.modules.auth.domain.models import User
from src.modules.admin.domain.models import AuditLog
from src.shared.domain.models import Rol, EstadoUsuario
from src.core.exceptions import NotFoundError, BusinessRuleError, ConflictError


class TallerAdapter(TallerModulePort):
    def __init__(
        self,
        taller_repo: TallerRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort,
        auth_repo: AuthPort,
        password_port: PasswordPort,
        audit_repo: AuditLogRepositoryPort | None = None,
    ):
        self.taller_repo = taller_repo
        self.perfil_taller_repo = perfil_taller_repo
        self.auth_repo = auth_repo
        self.password_port = password_port
        self.audit_repo = audit_repo

    def crear(
        self,
        aseguradora_id: str,
        nombre_comercial: str,
        rfc: str,
        direccion_tecnica: str,
        telefono_contacto: str,
    ) -> TallerModel:
        model = TallerModel(
            id="",
            nombre_comercial=nombre_comercial,
            rfc=rfc,
            direccion_tecnica=direccion_tecnica,
            telefono_contacto=telefono_contacto,
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        try:
            taller = self.taller_repo.save(model)
        except IntegrityError:
            raise ConflictError("Ya existe un taller registrado con ese RFC")
        self.taller_repo.vincular_taller_aseguradora(taller.id, aseguradora_id)
        return taller

    def obtener(self, taller_id: str) -> TallerModel:
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado")
        return taller

    def listar(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[TallerModel], int]:
        return self.taller_repo.list_by_aseguradora(aseguradora_id, offset, limit)

    def actualizar(
        self,
        taller_id: str,
        nombre_comercial: str | None,
        direccion_tecnica: str | None,
        telefono_contacto: str | None,
    ) -> TallerModel:
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado")

        if nombre_comercial is not None:
            taller.nombre_comercial = nombre_comercial
        if direccion_tecnica is not None:
            taller.direccion_tecnica = direccion_tecnica
        if telefono_contacto is not None:
            taller.telefono_contacto = telefono_contacto
        taller.updated_at = datetime.now()
        return self.taller_repo.update(taller)

    def eliminar(self, taller_id: str, aseguradora_id: str) -> None:
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado")
        self.taller_repo.desvincular_taller_aseguradora(taller_id, aseguradora_id)

    def crear_operador(
        self,
        aseguradora_id: str,
        admin_id: str,
        taller_id: str,
        data,
    ) -> dict:
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado.")

        existing_user = self.auth_repo.get_by_email(data.email)
        if existing_user:
            raise BusinessRuleError("El correo electrónico ya está registrado.")

        hashed_pwd = self.password_port.hash(data.password)

        new_user = User(
            usuario_id=str(uuid.uuid4()),
            nombre=data.nombre,
            email=data.email,
            password=hashed_pwd,
            telefono="",
            rol=Rol.TALLER.value,
            estado=EstadoUsuario.ACTIVO.value,
            aseguradora_id=None,
            fecha_creacion=datetime.now(timezone.utc),
            is_authenticated=False,
            fecha_eliminacion=None,
        )
        user_created = self.auth_repo.create(new_user)
        self.perfil_taller_repo.add_usuario_a_taller(
            user_created.usuario_id, taller_id, data.puesto
        )

        if self.audit_repo:
            self.audit_repo.append(AuditLog(
                id=str(uuid.uuid4()),
                usuario_id=admin_id,
                aseguradora_id=aseguradora_id,
                accion_realizada="CREAR_OPERADOR_TALLER",
                evento_modulo="TALLERES",
                metadata_context={
                    "operador_email": data.email,
                    "operador_id": user_created.usuario_id,
                    "taller_id": taller_id,
                },
                direccion_ip="[IP_ADDRESS]",
                user_agent=admin_id,
                created_at=datetime.now(),
            ))

        return {
            "usuario_id": user_created.usuario_id,
            "email": user_created.email,
            "rol": user_created.rol,
            "taller_id": taller_id,
            "puesto": data.puesto,
        }
