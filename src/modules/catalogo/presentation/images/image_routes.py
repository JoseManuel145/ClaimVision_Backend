from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.params import File

from src.modules.catalogo.app.images import DesasociarImageFromProduct
from src.modules.catalogo.presentation.images.image_dependencies import desasociar_image_service
from src.modules.catalogo.app.images import (
    UploadImage,
    AsociarImageToProduct,
    GetImagesByProduct,
    DeleteImage,
    DeleteImagesByProduct
)
from src.modules.catalogo.presentation.images.image_dependencies import (
    upload_image_service,
    asociar_image_service,
    get_by_product_service,
    delete_image_service,
    delete_image_by_product_service
)
from src.modules.catalogo.presentation.images.images_dto import (
    ImagenDTO,
    ImagenCreateDTO,
    ProductoImagenDTO,
    ProductoImagenCreateDTO
)
router = APIRouter()

# --- 1. GESTIÓN GLOBAL DE IMÁGENES (Subida y Eliminación Física) ---
@router.post("", response_model=ImagenDTO, status_code=status.HTTP_201_CREATED)
async def subir_imagen(
    dto: ImagenCreateDTO = Depends(ImagenCreateDTO.as_form),
    file: UploadFile = File(...),
    service: UploadImage = Depends(upload_image_service)
):
    content = await file.read()
    file.filename = file.filename.replace(" ", "_")
    imagen = service.execute(
        imagen_data=content,
        filename=file.filename,
        orden=dto.orden
    )
    return ImagenDTO(
        imagen_id=imagen.imagen_id,
        path=imagen.path,
        orden=imagen.orden
    )

@router.delete("/{imagen_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_imagen(
    imagen_id: int,
    service: DeleteImage = Depends(delete_image_service)
):
    service.execute(imagen_id)


# --- 2. ASOCIACIÓN CON PRODUCTOS (Rutas fijas /productos) ---
@router.post("/productos", response_model=ProductoImagenDTO)
def asociar_imagen(
    dto: ProductoImagenCreateDTO,
    service: AsociarImageToProduct = Depends(asociar_image_service)
):
    return service.execute(dto)


# --- 3. OPERACIONES POR PRODUCTO (Sub-recursos) ---

@router.delete("/productos/{producto_id}/{imagen_id}", status_code=status.HTTP_204_NO_CONTENT)
def desasociar_imagen(
    producto_id: str,
    imagen_id: int,
    service: DesasociarImageFromProduct = Depends(desasociar_image_service)
):
    service.execute(producto_id, imagen_id)

@router.get("/productos/{producto_id}", response_model=list[ImagenDTO])
def get_imagenes_por_producto(
    producto_id: str,
    service: GetImagesByProduct = Depends(get_by_product_service)
):
    imagenes = service.execute(producto_id)
    return [ImagenDTO(imagen_id=img.imagen_id, path=img.path, orden=img.orden) for img in imagenes]

@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_imagenes_producto(
    producto_id: str,
    service: DeleteImagesByProduct = Depends(delete_image_by_product_service)
):
    service.execute(producto_id)