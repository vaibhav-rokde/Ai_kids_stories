from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.story import StoryStatus


# Request Schemas
class StoryCreateRequest(BaseModel):
    """Request schema for creating a story"""
    theme: str = Field(..., min_length=10, max_length=500, description="Story theme or idea")
    character_name: Optional[str] = Field(None, max_length=100, description="Main character name")
    age_group: str = Field(default="5-7", description="Target age group (3-5, 5-7, 7-10)")

    class Config:
        json_schema_extra = {
            "example": {
                "theme": "A brave squirrel who learns to share with friends",
                "character_name": "Squeaky",
                "age_group": "5-7"
            }
        }


# Response Schemas
class StoryResponse(BaseModel):
    """Response schema for story"""
    id: int
    theme: str
    character_name: Optional[str]
    age_group: str
    story_text: Optional[str]
    story_title: Optional[str]
    audio_url: Optional[str]
    status: StoryStatus
    word_count: Optional[int]
    duration_seconds: Optional[float]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class StoryListResponse(BaseModel):
    """Response schema for list of stories"""
    stories: list[StoryResponse]
    total: int
    page: int
    page_size: int


class StoryStatusResponse(BaseModel):
    """Response schema for story status check"""
    id: int
    status: StoryStatus
    progress_message: str
    audio_url: Optional[str]
    error_message: Optional[str]

    class Config:
        from_attributes = True


# Health Check Schema
class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    environment: str
    timestamp: datetime
