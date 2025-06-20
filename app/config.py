import sys
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from pathlib import Path

def find_env_file():
    """Поиск .env файла в родительских директориях"""
    current_path = Path(__file__).parent.absolute()
    for parent in current_path.parents:
        env_path = parent / '.env'
        if env_path.exists():
            return env_path
    return None
class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    APP_URL: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    TG_BOT_TOKEN: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    
    @property
    def DATABASE_URL(self):
        encoded_pass = quote_plus(self.DB_PASS)
        return f"postgres://{self.DB_USER}:{encoded_pass}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = find_env_file() or '.env'


config = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": config.DATABASE_URL,
    },
    "apps": {
        "app": {
            "models": ["aerich.models", "app.database.models"],
            "default_connection": "default",
        },
    },
}