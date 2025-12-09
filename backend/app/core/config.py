from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # Ignore extra fields from .env
    )
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

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"  # Change this in production!

    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from comma-separated string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    # Google Gemini API
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-pro"

    # Azure Text-to-Speech
    AZURE_SPEECH_KEY: str = "your_azure_speech_key_here"  # Set to use Azure TTS
    AZURE_SPEECH_REGION: str = "your_azure_region_here"
    AZURE_VOICE_NAME: str = "en-US-JennyNeural"
    USE_FALLBACK_TTS: bool = False  # Set to True to use gTTS instead of Azure

    # Cartesia TTS API
    CARTESIA_API_KEY: str = ""
    CARTESIA_MODEL_ID: str = "sonic-english"
    CARTESIA_VOICE_ID: str = "694f9389-aac1-45b6-b726-9d9369183238"  # Child-friendly voice
    USE_CARTESIA_TTS: bool = True  # Use Cartesia instead of Azure

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


settings = Settings()
