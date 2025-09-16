from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    ENV: str = "development"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:8000"]

    POSTGRES_USER: str = "grader"
    POSTGRES_PASSWORD: str = "grader"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB: str = "grader"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

settings = Settings()
