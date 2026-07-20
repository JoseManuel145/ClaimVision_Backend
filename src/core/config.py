from pathlib import Path
from pydantic_settings import BaseSettings

CORE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # SUPABASE
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET_IMG: str
    SUPABASE_BUCKET_PDF: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    # JWT CONFIGURATION
    SECRET_KEY: str
    ALGORITHM: str
    TIME_MINUTES: int

    BCRYPT_ROUNDS: int
    ENCRYPTION_KEY: str
    OCR_API_URL: str
    IA_SERVICE_URL: str
    REDIS_URL: str = ""

    # LOGGING & CORS
    LOG_LEVEL: str
    ORIGINS: list[str]

    # FIREBASE
    FIREBASE_CREDENTIALS_PATH: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
