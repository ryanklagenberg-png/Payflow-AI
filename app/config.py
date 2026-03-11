from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    DATABASE_URL: str = "postgresql+asyncpg://payflow:payflow@db:5432/payflow"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 20
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    JWT_SECRET: str = "change-me-in-production-use-a-real-secret"
    JWT_EXPIRATION_HOURS: int = 24

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
