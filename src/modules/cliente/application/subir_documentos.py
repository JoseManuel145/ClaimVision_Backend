import uuid
from datetime import datetime, timezone
from src.modules.cliente.domain.models import ClienteDocumento
from src.modules.cliente.domain.ports import ClienteDocumentoRepositoryPort
from src.modules.siniestro.domain.ports.storage_port import StoragePort
from src.core.exceptions import BadRequestError
from src.core.config import settings

class SubirDocumentos:
    def __init__(self, doc_repo: ClienteDocumentoRepositoryPort, storage: StoragePort):
        self.doc_repo = doc_repo
        self.storage = storage

    def execute(
        self,
        usuario_id: str,
        identificacion_bytes: bytes,
        identificacion_filename: str,
        identificacion_content_type: str,
        poliza_bytes: bytes,
        poliza_filename: str,
        poliza_content_type: str,
    ) -> dict:
        # 1. Validar tamaños (max 10MB = 10,485,760 bytes)
        MAX_SIZE = 10 * 1024 * 1024
        if len(identificacion_bytes) > MAX_SIZE:
            raise BadRequestError("La identificación supera el límite de 10MB.")
        if len(poliza_bytes) > MAX_SIZE:
            raise BadRequestError("La póliza supera el límite de 10MB.")

        # 2. Validar formatos
        id_ext = identificacion_filename.split(".")[-1].lower() if "." in identificacion_filename else ""
        if id_ext not in ["pdf", "jpg", "jpeg", "png"] and identificacion_content_type not in [
            "application/pdf", "image/jpeg", "image/png"
        ]:
            raise BadRequestError("La identificación debe ser PDF o imagen (JPG, PNG).")

        pol_ext = poliza_filename.split(".")[-1].lower() if "." in poliza_filename else ""
        if pol_ext != "pdf" and poliza_content_type != "application/pdf":
            raise BadRequestError("La póliza debe ser de tipo PDF.")

        # Determinar buckets adecuados
        id_bucket = settings.SUPABASE_BUCKET_PDF if id_ext == "pdf" or identificacion_content_type == "application/pdf" else settings.SUPABASE_BUCKET_IMG
        pol_bucket = settings.SUPABASE_BUCKET_PDF

        # Rutas de almacenamiento únicas por usuario
        id_path = f"documentos/{usuario_id}_ine.{id_ext or 'pdf'}"
        pol_path = f"documentos/{usuario_id}_poliza.{pol_ext or 'pdf'}"

        # 3. Subir a storage
        # La llamada a self.storage.upload_file sube los bytes al bucket correspondiente
        self.storage.upload_file(
            bucket_name=id_bucket,
            file_path=id_path,
            file_bytes=identificacion_bytes,
            content_type=identificacion_content_type,
        )

        self.storage.upload_file(
            bucket_name=pol_bucket,
            file_path=pol_path,
            file_bytes=poliza_bytes,
            content_type=poliza_content_type,
        )

        # Generar URLs persistentes en el formato que resolve_storage_url reconoce
        id_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{id_bucket}/{id_path}"
        pol_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{pol_bucket}/{pol_path}"

        now = datetime.now(timezone.utc)

        # 4. Registrar en base de datos (guardar o sobreescribir)
        doc = self.doc_repo.get_by_usuario_id(usuario_id)
        if not doc:
            doc = ClienteDocumento(
                id=str(uuid.uuid4()),
                usuario_id=usuario_id,
                identificacion_url=id_url,
                identificacion_tipo=id_ext or "pdf",
                identificacion_subido_en=now,
                poliza_url=pol_url,
                poliza_tipo=pol_ext or "pdf",
                poliza_subido_en=now,
                created_at=now,
                updated_at=now,
            )
            doc = self.doc_repo.save(doc)
        else:
            doc.identificacion_url = id_url
            doc.identificacion_tipo = id_ext or "pdf"
            doc.identificacion_subido_en = now
            doc.poliza_url = pol_url
            doc.poliza_tipo = pol_ext or "pdf"
            doc.poliza_subido_en = now
            doc.updated_at = now
            doc = self.doc_repo.update(doc)

        return {
            "identificacion_url": id_url,
            "poliza_url": pol_url,
            "subido_en": now,
        }
