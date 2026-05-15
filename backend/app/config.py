from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "MsAlisia Phase 0 API"
    environment: str = "development"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    cors_origin_regex: str | None = r"http://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|172\.\d+\.\d+\.\d+):5173"

    # Groq / LLM settings
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-haiku-latest"
    anthropic_base_url: str = "https://api.anthropic.com/v1"
    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_temperature: float = 0.35
    llm_max_tokens: int = 420

    # Local prototype persistence
    database_path: str = "./data/msalisia_phase0.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
