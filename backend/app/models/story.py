from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Nullable for backward compatibility

    # Input parameters
    theme = Column(Text, nullable=False)
    character_name = Column(String(100), nullable=True)
    age_group = Column(String(20), default="5-7")

    # Generated content
    story_text = Column(Text, nullable=True)
    story_text_html = Column(Text, nullable=True)
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

    # Version tracking
    current_version = Column(Integer, default=1)

    # Relationships
    user = relationship("User", back_populates="stories")
    versions = relationship("StoryVersion", back_populates="story", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Story(id={self.id}, title='{self.story_title}', status='{self.status}')>"


class StoryVersion(Base):
    """Story version history model"""
    __tablename__ = "story_versions"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)

    # Snapshot of story content at this version
    theme = Column(Text, nullable=False)
    character_name = Column(String(100), nullable=True)
    age_group = Column(String(20))
    story_text = Column(Text, nullable=True)
    story_text_html = Column(Text, nullable=True)
    story_title = Column(String(200), nullable=True)

    # Audio files for this version
    audio_file_path = Column(String(500), nullable=True)
    music_file_path = Column(String(500), nullable=True)
    final_audio_path = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)

    # Metadata
    word_count = Column(Integer, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    story = relationship("Story", back_populates="versions")

    def __repr__(self):
        return f"<StoryVersion(id={self.id}, story_id={self.story_id}, version={self.version_number})>"
