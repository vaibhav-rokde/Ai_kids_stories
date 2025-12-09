from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Google Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"

    # Azure Text-to-Speech
    AZURE_SPEECH_KEY: str
    AZURE_SPEECH_REGION: str
    AZURE_VOICE_NAME: str = "en-US-JennyNeural"

    # Mubert Music API
    MUBERT_API_KEY: str
    MUBERT_LICENSE: str

    # Story Configuration
    STORY_MIN_LENGTH: int = 400
    STORY_MAX_LENGTH: int = 600
    STORY_TARGET_DURATION: int = 240  # 4 minutes
    TARGET_AGE_DEFAULT: str = "5-7"

    # Audio Configuration
    AUDIO_FORMAT: str = "mp3"
    AUDIO_BITRATE: str = "128k"
    AUDIO_SAMPLE_RATE: int = 44100

    # File Storage
    STORIES_DIR: str = "./stories"
    MAX_STORY_FILE_SIZE_MB: int = 50

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
