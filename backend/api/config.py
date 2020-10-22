from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = None

    class Config:
        env_file = ".env"


config = Settings()
