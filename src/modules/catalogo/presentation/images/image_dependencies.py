from fastapi import Depends
from src.core.supabase_config import get_supabase_client
from src.core.database import get_session
from src.modules.catalogo.infra.images.db.image_repository import ImageRepository
from src.modules.catalogo.infra.images.db.product_image_repository import ProductImageRepository
from src.modules.catalogo.infra.images.storage.supabase_storage_repository import SupabaseStorageRepository
from src.modules.catalogo.app.images import (
    AsociarImageToProduct,
    DesasociarImageFromProduct,
    UploadImage,
    DeleteImage,
    DeleteImagesByProduct,
    GetImagesByProduct,
)

def asociar_image_service(session = Depends(get_session)):
    repo = ProductImageRepository(session)
    return AsociarImageToProduct(repo)

def desasociar_image_service(session = Depends(get_session)):
    repo = ProductImageRepository(session)
    return DesasociarImageFromProduct(repo)

def upload_image_service(session = Depends(get_session), client=Depends(get_supabase_client)):
    repo = ImageRepository(session)
    storage = SupabaseStorageRepository(client)
    return UploadImage(repo, storage)

def delete_image_service(session = Depends(get_session), client=Depends(get_supabase_client)):
    repo = ImageRepository(session)
    storage = SupabaseStorageRepository(client)
    return DeleteImage(repo, storage)

def delete_image_by_product_service(session = Depends(get_session), client=Depends(get_supabase_client)):
    repo_image = ImageRepository(session)
    repo_product_image = ProductImageRepository(session)
    storage = SupabaseStorageRepository(client)
    return DeleteImagesByProduct(repo_image, repo_product_image, storage)

def get_by_product_service(session = Depends(get_session)):
    repo = ImageRepository(session)
    repo_product_image = ProductImageRepository(session)
    return GetImagesByProduct(repo, repo_product_image)
