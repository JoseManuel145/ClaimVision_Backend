import pytest
from datetime import datetime, date
from src.modules.cliente.domain.models import ClienteProfile, ClienteDocumento
from src.modules.cliente.application.subir_documentos import SubirDocumentos
from src.modules.cliente.application.obtener_documentos import ObtenerDocumentos
from src.core.exceptions import BadRequestError
from tests.fakes.cliente import FakeClienteRepo, FakeClienteDocumentoRepo, FakeStorage, default_cliente_profile

def test_obtener_documentos_vacios():
    doc_repo = FakeClienteDocumentoRepo()
    profile_repo = FakeClienteRepo(default_cliente_profile())
    
    uc = ObtenerDocumentos(doc_repo, profile_repo)
    res = uc.execute("user-1")
    
    assert res["identificacion"] is None
    assert res["poliza"] is None

def test_subir_documentos_exitoso():
    doc_repo = FakeClienteDocumentoRepo()
    storage = FakeStorage()
    
    uc = SubirDocumentos(doc_repo, storage)
    res = uc.execute(
        usuario_id="user-1",
        identificacion_bytes=b"ine-content",
        identificacion_filename="ine.png",
        identificacion_content_type="image/png",
        poliza_bytes=b"poliza-content",
        poliza_filename="poliza.pdf",
        poliza_content_type="application/pdf"
    )
    
    assert "identificacion_url" in res
    assert "poliza_url" in res
    assert "subido_en" in res
    
    # Verify saved state in repo
    saved_doc = doc_repo.get_by_usuario_id("user-1")
    assert saved_doc is not None
    assert saved_doc.identificacion_tipo == "png"
    assert saved_doc.poliza_tipo == "pdf"

def test_obtener_documentos_enriquecidos():
    doc_repo = FakeClienteDocumentoRepo()
    profile = default_cliente_profile()
    profile.numero_poliza = "POL-9999"
    profile.vigencia_poliza = date(2028, 12, 31)
    profile_repo = FakeClienteRepo(profile)
    
    # First upload
    subir_uc = SubirDocumentos(doc_repo, FakeStorage())
    subir_uc.execute(
        usuario_id="user-1",
        identificacion_bytes=b"ine-content",
        identificacion_filename="ine.jpg",
        identificacion_content_type="image/jpeg",
        poliza_bytes=b"pol-content",
        poliza_filename="poliza.pdf",
        poliza_content_type="application/pdf"
    )
    
    # Retrieve
    obtener_uc = ObtenerDocumentos(doc_repo, profile_repo)
    res = obtener_uc.execute("user-1")
    
    assert res["identificacion"] is not None
    assert res["identificacion"]["tipo"] == "jpg"
    assert res["poliza"] is not None
    assert res["poliza"]["tipo"] == "pdf"
    assert res["poliza"]["numero_poliza"] == "POL-9999"
    assert res["poliza"]["vigencia"] == date(2028, 12, 31)

def test_subir_documentos_valida_tamano():
    doc_repo = FakeClienteDocumentoRepo()
    uc = SubirDocumentos(doc_repo, FakeStorage())
    
    # Exceed limit
    large_file = b"x" * (10 * 1024 * 1024 + 1)
    
    with pytest.raises(BadRequestError) as exc_info:
        uc.execute(
            usuario_id="user-1",
            identificacion_bytes=large_file,
            identificacion_filename="ine.png",
            identificacion_content_type="image/png",
            poliza_bytes=b"pol-content",
            poliza_filename="poliza.pdf",
            poliza_content_type="application/pdf"
        )
    assert "supera el límite de 10MB" in str(exc_info.value)

def test_subir_documentos_valida_formatos():
    doc_repo = FakeClienteDocumentoRepo()
    uc = SubirDocumentos(doc_repo, FakeStorage())
    
    # Invalid INE type
    with pytest.raises(BadRequestError) as exc_info:
        uc.execute(
            usuario_id="user-1",
            identificacion_bytes=b"ine",
            identificacion_filename="ine.txt",
            identificacion_content_type="text/plain",
            poliza_bytes=b"pol-content",
            poliza_filename="poliza.pdf",
            poliza_content_type="application/pdf"
        )
    assert "debe ser PDF o imagen" in str(exc_info.value)

    # Invalid Poliza type
    with pytest.raises(BadRequestError) as exc_info:
        uc.execute(
            usuario_id="user-1",
            identificacion_bytes=b"ine",
            identificacion_filename="ine.png",
            identificacion_content_type="image/png",
            poliza_bytes=b"pol-content",
            poliza_filename="poliza.png",
            poliza_content_type="image/png"
        )
    assert "debe ser de tipo PDF" in str(exc_info.value)


def test_resolve_storage_url_compatibilidad():
    from src.shared.infra.storage.url_resolver import resolve_storage_url
    from unittest.mock import MagicMock

    client = MagicMock()
    # Mock supabase storage client
    client.storage.from_().create_signed_url.return_value = {"signedURL": "http://fresh-signed-url"}

    # 1. Test public URL
    url_pub = "https://abc.supabase.co/storage/v1/object/public/pdfs/file.pdf"
    res_pub = resolve_storage_url(client, url_pub)
    assert res_pub == "http://fresh-signed-url"

    # 2. Test old signed URL (with token query param)
    url_sign = "https://abc.supabase.co/storage/v1/object/sign/pdfs/file.pdf?token=oldjwt"
    res_sign = resolve_storage_url(client, url_sign)
    assert res_sign == "http://fresh-signed-url"

