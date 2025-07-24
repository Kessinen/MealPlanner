from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

from os import getenv

print(
    getenv("DB_USER"),
    getenv("DB_PASSWORD"),
    getenv("DB_NAME"),
    getenv("DB_HOST"),
    getenv("DB_PORT"),
)


class Settings(BaseSettings):
    # Application settings
    APP_HOST: str = Field("127.0.0.1", env="APP_HOST")
    APP_PORT: int = Field(8000, env="APP_PORT")
    LOG_DIR: Path = Field(Path("data") / "logs", env="LOG_DIR")

    # Database settings
    DB_HOST: str = Field(getenv("DB_HOST", "127.0.0.1"), env="DB_HOST")
    DB_PORT: int = Field(getenv("DB_PORT", 5422), env="DB_PORT")
    DB_USER: str = Field(getenv("DB_USER", "user"), env="DB_USER")
    DB_PASSWORD: str = Field(getenv("DB_PASSWORD", "password"), env="DB_PASSWORD")
    DB_NAME: str = Field(getenv("DB_NAME", "meal_planner"), env="DB_NAME")

    @property
    def db_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # API keys
    OPENROUTER_API_KEY: str = Field("", env="OPENROUTER_API_KEY")
    MISTRAL_API_KEY: str = Field("", env="MISTRAL_API_KEY")
    GEMINI_API_KEY: str = Field("", env="GEMINI_API_KEY")

    # Ollama settings
    OLLAMA_HOST: str = Field("127.0.0.1", env="OLLAMA_HOST")
    OLLAMA_PORT: int = Field(11431, env="OLLAMA_PORT")

    @property
    def ollama_url(self):
        return f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}"


settings = Settings()
