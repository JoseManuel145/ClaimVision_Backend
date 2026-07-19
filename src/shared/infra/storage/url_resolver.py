import re
from supabase import Client

_SIGNED_TTL = 3600


def resolve_storage_url(supabase_client: Client, url: str | None) -> str | None:
    if not url:
        return url

    if "/object/public/" not in url:
        return url

    match = re.search(r"/object/public/([^/]+)/(.+)$", url)
    if not match:
        return url

    bucket = match.group(1)
    path = match.group(2)

    signed = supabase_client.storage.from_(bucket).create_signed_url(path, _SIGNED_TTL)
    return signed["signedURL"]


def resolve_storage_urls(supabase_client: Client, urls: list[str | None]) -> list[str | None]:
    return [resolve_storage_url(supabase_client, url) for url in urls]
