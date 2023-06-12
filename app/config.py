from pydantic import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"


def get_settings():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return Settings()


settings = get_settings()
