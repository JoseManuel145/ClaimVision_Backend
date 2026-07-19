import re
from supabase import Client
from src.core.logging import get_logger
from src.core.config import settings

logger = get_logger("storage.url_resolver")

_SIGNED_TTL = 3600
_PUBLIC_PATTERN = re.compile(r"/object/public/([^/]+)/(.+)$")


def resolve_storage_url(supabase_client: Client, url: str | None) -> str | None:
    if not url:
        return url

    if "/object/public/" not in url:
        return url

    match = _PUBLIC_PATTERN.search(url)
    if not match:
        logger.warning("resolve_storage_url: patron no matchea url=%s", url)
        return url

    bucket = match.group(1)
    path = match.group(2)

    try:
        signed = supabase_client.storage.from_(bucket).create_signed_url(path, _SIGNED_TTL)
        result = signed["signedURL"]
        logger.info(
            "resolve_storage_url: public→signed bucket=%s path=%s result=%s",
            bucket, path, result[:120],
        )
        return result
    except Exception as e:
        logger.error(
            "resolve_storage_url: create_signed_url fallo bucket=%s path=%s error=%s",
            bucket, path, e,
        )
        fallback = f"{settings.SUPABASE_URL}/storage/v1/object/sign/{bucket}/{path}"
        logger.warning("resolve_storage_url: usando fallback sin token url=%s", fallback)
        return fallback


def resolve_storage_urls(supabase_client: Client, urls: list[str | None]) -> list[str | None]:
    return [resolve_storage_url(supabase_client, url) for url in urls]
