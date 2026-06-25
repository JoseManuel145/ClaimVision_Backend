from httpx import AsyncClient
from supabase import create_client, Client
from src.core.config import settings

_supabase_client: Client | None = None

def get_supabase_client() -> Client:
    """Obtiene o crea la instancia global del cliente Supabase."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _supabase_client

async def get_supabase_async_client() -> AsyncClient:
    """Obtiene o crea la instancia global del cliente Supabase asíncrono."""
    global _supabase_async_client
    if _supabase_async_client is None:
        _supabase_async_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _supabase_async_client
