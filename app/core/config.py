from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:8000"]

    class Config:
        env_file = ".env"

settings = Settings()
