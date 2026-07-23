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
# Cuando un URL apunta a un bucket/prefijo legacy y falla la resolución,
# se intenta resolver (y migrar) al bucket/prefijo nuevo.
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


def _resolve_legacy(
    supabase_client: Client,
    bucket: str,
    path: str,
) -> str | None:
    """
    Intenta resolver un URL legacy buscando un mapeo en _LEGACY_MAP.
    Si encuentra match, migra el archivo al bucket nuevo y retorna la URL firmada nueva.
    """
    for (legacy_bucket, legacy_prefix), (new_bucket, new_prefix) in _LEGACY_MAP.items():
        if bucket == legacy_bucket and path.startswith(legacy_prefix):
            new_path = new_prefix + path[len(legacy_prefix):]

            migrated = _migrate_file(supabase_client, bucket, path, new_bucket, new_path)
            target_bucket = new_bucket if migrated else bucket
            target_path = new_path if migrated else path

            try:
                signed = supabase_client.storage.from_(target_bucket).create_signed_url(
                    target_path, _SIGNED_TTL,
                )
                result = signed["signedURL"]
                logger.info(
                    "resolve_legacy: resuelto bucket=%s path=%s → %s (migrated=%s)",
                    bucket, path, result[:120], migrated,
                )
                return result
            except Exception as e:
                logger.error(
                    "resolve_legacy: fallo resolución post-migración bucket=%s path=%s: %s",
                    target_bucket, target_path, e,
                )
    return None


def resolve_storage_url(supabase_client: Client, url: str | None) -> str | None:
    if not url:
        return url

    bucket, path = _parse_url(url)
    if not bucket or not path:
        return url

    # 1. Intentar resolver con el bucket/path actual
    try:
        signed = supabase_client.storage.from_(bucket).create_signed_url(path, _SIGNED_TTL)
        result = signed["signedURL"]
        logger.info(
            "resolve_storage_url: resolved bucket=%s path=%s result=%s",
            bucket, path, result[:120],
        )
        return result
    except Exception as e:
        logger.warning(
            "resolve_storage_url: create_signed_url fallo bucket=%s path=%s error=%s",
            bucket, path, e,
        )

    # 2. Intentar resolver como legacy (con migración automática)
    legacy_url = _resolve_legacy(supabase_client, bucket, path)
    if legacy_url:
        return legacy_url

    # 3. Fallback: URL firmada sin token (puede que funcione si el bucket es público)
    fallback = f"{settings.SUPABASE_URL}/storage/v1/object/sign/{bucket}/{path}"
    logger.warning("resolve_storage_url: usando fallback sin token url=%s", fallback)
    return fallback


def resolve_storage_urls(supabase_client: Client, urls: list[str | None]) -> list[str | None]:
    return [resolve_storage_url(supabase_client, url) for url in urls]
