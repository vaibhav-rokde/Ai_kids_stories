from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class StoryStatus(str, enum.Enum):
    """Story generation status"""
    PENDING = "pending"
    GENERATING_TEXT = "generating_text"
    GENERATING_AUDIO = "generating_audio"
    ADDING_MUSIC = "adding_music"
    COMPLETED = "completed"
    FAILED = "failed"


class Story(Base):
    """Story model"""
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)

    # Input parameters
    theme = Column(Text, nullable=False)
    character_name = Column(String(100), nullable=True)
    age_group = Column(String(20), default="5-7")

    # Generated content
    story_text = Column(Text, nullable=True)
    story_title = Column(String(200), nullable=True)

    # File paths and URLs
    audio_file_path = Column(String(500), nullable=True)
    music_file_path = Column(String(500), nullable=True)
    final_audio_path = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)

    # Metadata
    status = Column(Enum(StoryStatus), default=StoryStatus.PENDING)
    word_count = Column(Integer, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Story(id={self.id}, title='{self.story_title}', status='{self.status}')>"
