import re
from supabase import Client
from src.core.logging import get_logger
from src.core.config import settings

logger = get_logger("storage.url_resolver")

_SIGNED_TTL = 3600
_PUBLIC_PATTERN = re.compile(r"/object/public/([^/]+)/(.+)$")
_SIGN_PATTERN = re.compile(r"/object/sign/([^/]+)/([^?]+)")

# Mapeo de paths legacy → estándar nuevo.
# Clave: (bucket_viejo, prefijo_path_viejo)  →  Valor: (bucket_nuevo, prefijo_path_nuevo)
_LEGACY_MAP: dict[tuple[str, str], tuple[str, str]] = {
    ("cotizaciones", "documentos/"): ("documentos", "documentos/"),
}


def resolve_bucket(file_path: str) -> str:
    """
    Determina el bucket correcto analizando el path del archivo.
    Reglas de routing:
      - siniestros/* → imagenes (fotos y audio de siniestros)
      - cotizacion_* o *_cotizacion_* → cotizaciones (PDFs de taller)
      - *_ine.* o *_poliza.* → documentos (documentos de onboarding del cliente)
      - default → cotizaciones (fallback general para PDFs)
    """
    lower = file_path.lower()

    if lower.startswith("siniestros/"):
        return settings.SUPABASE_BUCKET_IMG

    if "cotizacion" in lower:
        return settings.SUPABASE_BUCKET_PDF

    if "_ine." in lower or "_poliza." in lower:
        return settings.SUPABASE_BUCKET_DOCUMENTOS

    return settings.SUPABASE_BUCKET_PDF


def _parse_url(url: str) -> tuple[str | None, str | None]:
    """Extrae (bucket, path) de una URL de Supabase Storage."""
    if "/object/public/" in url:
        match = _PUBLIC_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
    elif "/object/sign/" in url:
        match = _SIGN_PATTERN.search(url)
        if match:
            return match.group(1), match.group(2)
    return None, None


def _migrate_file(
    supabase_client: Client,
    old_bucket: str,
    old_path: str,
    new_bucket: str,
    new_path: str,
) -> bool:
    """
    Migra un archivo de un bucket/path legacy al estándar nuevo.
    Descarga del bucket viejo, sube al nuevo, borra el viejo.
    Retorna True si la migración fue exitosa.
    """
    try:
        logger.info(
            "migrate_file: descargando de %s/%s", old_bucket, old_path,
        )
        file_bytes = supabase_client.storage.from_(old_bucket).download(old_path)

        content_type = "application/pdf"
        if old_path.endswith((".jpg", ".jpeg")):
            content_type = "image/jpeg"
        elif old_path.endswith(".png"):
            content_type = "image/png"

        logger.info(
            "migrate_file: subiendo a %s/%s (%d bytes)",
            new_bucket, new_path, len(file_bytes),
        )
        supabase_client.storage.from_(new_bucket).upload(
            new_path,
            file_bytes,
            file_options={"content-type": content_type, "upsert": "true"},
        )

        try:
            supabase_client.storage.from_(old_bucket).remove([old_path])
            logger.info("migrate_file: eliminado %s/%s", old_bucket, old_path)
        except Exception as e:
            logger.warning(
                "migrate_file: no se pudo eliminar archivo legacy %s/%s: %s",
                old_bucket, old_path, e,
            )

        return True
    except Exception as e:
        logger.error(
            "migrate_file: fallo migración %s/%s → %s/%s: %s",
            old_bucket, old_path, new_bucket, new_path, e,
        )
        return False


def _try_sign(supabase_client: Client, bucket: str, path: str) -> str | None:
    """Intenta crear una URL firmada. Retorna None si falla."""
    try:
        signed = supabase_client.storage.from_(bucket).create_signed_url(path, _SIGNED_TTL)
        return signed["signedURL"]
    except Exception:
        return None


def resolve_storage_url(supabase_client: Client, url: str | None) -> str | None:
    if not url:
        return url

    bucket, path = _parse_url(url)
    if not bucket or not path:
        return url

    # 1. Verificar si es un path legacy → migrar PRIMERO, resolver del bucket nuevo
    for (legacy_bucket, legacy_prefix), (new_bucket, new_prefix) in _LEGACY_MAP.items():
        if bucket == legacy_bucket and path.startswith(legacy_prefix):
            new_path = new_prefix + path[len(legacy_prefix):]

            # Si el archivo ya existe en el bucket nuevo, resolver directo desde ahí
            signed_new = _try_sign(supabase_client, new_bucket, new_path)
            if signed_new:
                logger.info(
                    "resolve_storage_url: legacy ya migrado, resolviendo de %s/%s",
                    new_bucket, new_path,
                )
                return signed_new

            # Migrar del bucket viejo al nuevo
            migrated = _migrate_file(supabase_client, bucket, path, new_bucket, new_path)
            if migrated:
                signed_new = _try_sign(supabase_client, new_bucket, new_path)
                if signed_new:
                    logger.info(
                        "resolve_storage_url: migrado y resuelto %s/%s → %s",
                        bucket, path, signed_new[:120],
                    )
                    return signed_new

            # Migración fallida — intentar resolver del bucket legacy como último recurso
            signed_legacy = _try_sign(supabase_client, bucket, path)
            if signed_legacy:
                logger.warning(
                    "resolve_storage_url: migración fallida, resolviendo de legacy %s/%s",
                    bucket, path,
                )
                return signed_legacy

            # Ni legacy ni nuevo funcionan — fallback sin token
            fallback = f"{settings.SUPABASE_URL}/storage/v1/object/sign/{new_bucket}/{new_path}"
            logger.error(
                "resolve_storage_url: fallo total bucket=%s path=%s, fallback=%s",
                bucket, path, fallback,
            )
            return fallback

    # 2. No es legacy — resolver normalmente del bucket actual
    signed = _try_sign(supabase_client, bucket, path)
    if signed:
        logger.info(
            "resolve_storage_url: resolved bucket=%s path=%s result=%s",
            bucket, path, signed[:120],
        )
        return signed

    # 3. Fallback: URL firmada sin token
    fallback = f"{settings.SUPABASE_URL}/storage/v1/object/sign/{bucket}/{path}"
    logger.warning("resolve_storage_url: usando fallback sin token url=%s", fallback)
    return fallback


def resolve_storage_urls(supabase_client: Client, urls: list[str | None]) -> list[str | None]:
    return [resolve_storage_url(supabase_client, url) for url in urls]
