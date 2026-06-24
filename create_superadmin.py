import uuid
from datetime import datetime, timezone
import sys
import os

# Ensure the root folder is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.auth.infra.security.password_service import PasswordService
from src.core.security import encrypt_aes256
from src.shared.domain.models import Rol, EstadoUsuario

def run():
    db = SessionLocal()
    email = "admin@claimvision.com"
    
    # Check if exists
    existing = db.query(UserTable).filter(UserTable.email == email).first()
    if existing:
        print(f"Superadmin {email} ya existe.")
        return

    password_service = PasswordService()
    pwd_hash = password_service.hash("SuperAdmin123!")

    name_crypted = encrypt_aes256("Administrador Global")
    
    admin = UserTable(
        id=uuid.uuid4(),
        aseguradora_id=None,
        rol=Rol.SUPER_ADMINISTRADOR.value,
        email=email,
        password_hash=pwd_hash,
        nombre_completo_cifrado=name_crypted,
        telefono_cifrado=None,
        estatus_arco=EstadoUsuario.ACTIVO.value,
        fecha_creacion=datetime.now(timezone.utc)
    )
    
    db.add(admin)
    db.commit()
    print(f"Superadmin {email} creado exitosamente con contraseña 'SuperAdmin123!'")

if __name__ == "__main__":
    run()
