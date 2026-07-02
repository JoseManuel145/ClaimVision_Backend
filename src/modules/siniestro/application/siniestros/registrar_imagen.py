import uuid
from datetime import datetime
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.ports.imagen_siniestro_repository_port import ImagenSiniestroRepositoryPort
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.cliente_checker_port import ClienteCheckerPort
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError


class RegistrarImagenSiniestro:
    """
    Registra una imagen ya subida (vía URL prefirmada, §8) en
    `imagenes_siniestro`. La validación de calidad por IA (`es_calidad_valida`)
    se ejecuta de forma asíncrona después (§7); aquí se persiste como válida por
    defecto. Valida la propiedad del siniestro por el cliente autenticado.
    """

    def __init__(
        self,
        imagen_repo: ImagenSiniestroRepositoryPort,
        siniestro_repo: SiniestroRepositoryPort,
        cliente_checker: ClienteCheckerPort,
    ):
        self.imagen_repo = imagen_repo
        self.siniestro_repo = siniestro_repo
        self.cliente_checker = cliente_checker

    def execute(
        self, usuario_id: str, siniestro_id: str, imagen_url: str, metadatos_json: dict | None = None
    ) -> ImagenSiniestroModel:
        perfil_cliente_id = self.cliente_checker.get_perfil_cliente_id_by_usuario(usuario_id)
        if not perfil_cliente_id:
            raise BusinessRuleError("El usuario no tiene un perfil de cliente (onboarding incompleto).")

        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.cliente_id != perfil_cliente_id:
            raise ForbiddenError("Este siniestro no pertenece al cliente autenticado.")

        imagen = ImagenSiniestroModel(
            id=str(uuid.uuid4()),
            siniestro_id=siniestro_id,
            imagen_url=imagen_url,
            es_calidad_valida=True,
            metadatos_json=metadatos_json,
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            deleted_at=None,
        )
        return self.imagen_repo.save(imagen)
