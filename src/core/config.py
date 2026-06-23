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

    # GOOGLE OAUTH
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # JWT CONFIGURATION
    SECRET_KEY: str
    ALGORITHM: str
    TIME_MINUTES: int

    BCRYPT_ROUNDS: int

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
