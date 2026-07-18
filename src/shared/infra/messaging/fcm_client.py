from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger("fcm")


def init_firebase():
    import firebase_admin
    from firebase_admin import credentials

    if not firebase_admin._apps:
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        if not cred_path:
            logger.warning("FIREBASE_CREDENTIALS_PATH está vacío. Firebase no se inicializará.")
            return
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK inicializado correctamente.")
        except Exception as e:
            logger.error(f"Error al inicializar Firebase: {e}")


def get_messaging():
    import firebase_admin
    from firebase_admin import messaging

    if not firebase_admin._apps:
        init_firebase()
    return messaging
