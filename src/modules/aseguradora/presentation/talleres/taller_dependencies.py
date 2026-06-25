from fastapi import Depends
from src.core.database import get_session
from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.aseguradora.application.talleres.create_taller import CreateTaller
from src.modules.aseguradora.application.talleres.list_talleres import ListTalleres
from src.modules.aseguradora.application.talleres.get_taller import GetTaller
from src.modules.aseguradora.application.talleres.update_taller import UpdateTaller
from src.modules.aseguradora.application.talleres.delete_taller import DeleteTaller

def taller_repo(session=Depends(get_session)) -> TallerRepository:
    return TallerRepository(session)

def create_taller_service(repo: TallerRepository = Depends(taller_repo)) -> CreateTaller:
    return CreateTaller(repo)

def list_talleres_service(repo: TallerRepository = Depends(taller_repo)) -> ListTalleres:
    return ListTalleres(repo)

def get_taller_service(repo: TallerRepository = Depends(taller_repo)) -> GetTaller:
    return GetTaller(repo)

def update_taller_service(repo: TallerRepository = Depends(taller_repo)) -> UpdateTaller:
    return UpdateTaller(repo)

def delete_taller_service(repo: TallerRepository = Depends(taller_repo)) -> DeleteTaller:
    return DeleteTaller(repo)

def crear_operador_taller_service(session=Depends(get_session)):
    from src.modules.aseguradora.application.talleres.create_taller_user import CreateOperadorTallerUseCase
    from src.modules.taller.infra.db.repositories.perfil_taller_repository import PerfilTallerRepository
    from src.modules.admin.infra.db.repositories.audit_log_repository import AuditLogRepository
    from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
    from src.modules.auth.infra.security.password_service import PasswordService
    
    taller_repo_inst = TallerRepository(session)
    perfil_taller_repo = PerfilTallerRepository(session)
    audit_repo = AuditLogRepository(session)
    auth_repo = AuthRepository(session)
    password_port = PasswordService()
    
    return CreateOperadorTallerUseCase(
        taller_repo_inst, 
        perfil_taller_repo, 
        audit_repo, 
        auth_repo, 
        password_port
    )
