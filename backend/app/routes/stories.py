from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_optional_user, get_current_user
from app.models.user import User
from app.models.story import Story, StoryStatus, StoryVersion
from app.models.schemas import (
    StoryCreateRequest,
    StoryResponse,
    StoryStatusResponse,
    StoryListResponse,
    StoryVersionResponse,
    StoryVersionListResponse
)
from app.services.story_orchestrator import StoryOrchestrator
from app.core.config import settings
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stories", tags=["stories"])


async def generate_story_background(story_id: int, theme: str, character_name: str | None, age_group: str, db: Session):
    """Background task to generate story"""
    try:
        # Get story from database
        story = db.query(Story).filter(Story.id == story_id).first()
        if not story:
            logger.error(f"Story {story_id} not found")
            return

        # Update status
        story.status = StoryStatus.GENERATING_TEXT
        db.commit()

        # Initialize orchestrator
        orchestrator = StoryOrchestrator()

        # Generate complete story
        result = await orchestrator.generate_complete_story(
            story_id=story_id,
            theme=theme,
            character_name=character_name,
            age_group=age_group
        )

        # Update database with results
        if result.get("error"):
            story.status = StoryStatus.FAILED
            story.error_message = result["error"]
        else:
            story.status = StoryStatus.COMPLETED
            story.story_text = result["story_text"]
            story.story_text_html = result.get("story_text_html", result["story_text"])
            story.story_title = result["story_title"]
            story.word_count = result["word_count"]
            story.final_audio_path = result["final_audio_path"]
            story.duration_seconds = result["duration_seconds"]
            story.completed_at = datetime.now()

            # Generate URL for frontend
            filename = os.path.basename(result["final_audio_path"])
            story.audio_url = f"/api/v1/stories/audio/{filename}"

        db.commit()
        logger.info(f"Story {story_id} generation completed: {story.status}")

    except Exception as e:
        logger.error(f"Error in background story generation: {str(e)}")
        story = db.query(Story).filter(Story.id == story_id).first()
        if story:
            story.status = StoryStatus.FAILED
            story.error_message = str(e)
            db.commit()


@router.post("/", response_model=StoryResponse, status_code=202)
async def create_story(
    request: StoryCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Create a new story (async generation)

    The story generation happens in the background.
    Use GET /stories/{id}/status to check progress.

    If authenticated, the story will be associated with the user.
    """
    try:
        # Create story record
        story = Story(
            theme=request.theme,
            character_name=request.character_name,
            age_group=request.age_group,
            status=StoryStatus.PENDING,
            user_id=current_user.id if current_user else None
        )
        db.add(story)
        db.commit()
        db.refresh(story)

        logger.info(f"Story {story.id} created, starting generation...")

        # Start background generation
        # Note: We need to create a new db session for background task
        from app.core.database import SessionLocal
        bg_db = SessionLocal()

        background_tasks.add_task(
            generate_story_background,
            story_id=story.id,
            theme=request.theme,
            character_name=request.character_name,
            age_group=request.age_group,
            db=bg_db
        )

        return story

    except Exception as e:
        logger.error(f"Error creating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")


@router.get("/my-stories", response_model=StoryListResponse)
def list_my_stories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """List current user's stories with pagination"""
    total = db.query(Story).filter(Story.user_id == current_user.id).count()
    stories = (
        db.query(Story)
        .filter(Story.user_id == current_user.id)
        .order_by(Story.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return StoryListResponse(
        stories=stories,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(story_id: int, db: Session = Depends(get_db)):
    """Get story by ID"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.get("/{story_id}/status", response_model=StoryStatusResponse)
def get_story_status(story_id: int, db: Session = Depends(get_db)):
    """Check story generation status"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Map status to progress message
    progress_messages = {
        StoryStatus.PENDING: "Your story is in the queue...",
        StoryStatus.GENERATING_TEXT: "Creating your magical story...",
        StoryStatus.GENERATING_AUDIO: "Bringing the story to life with narration...",
        StoryStatus.ADDING_MUSIC: "Adding enchanting background music...",
        StoryStatus.COMPLETED: "Your story is ready!",
        StoryStatus.FAILED: "Oh no! Something went wrong."
    }

    return StoryStatusResponse(
        id=story.id,
        status=story.status,
        progress_message=progress_messages.get(story.status, "Processing..."),
        audio_url=story.audio_url,
        error_message=story.error_message
    )


@router.get("/", response_model=StoryListResponse)
def list_stories(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all stories with pagination"""
    total = db.query(Story).count()
    stories = db.query(Story).order_by(Story.created_at.desc()).offset(skip).limit(limit).all()

    return StoryListResponse(
        stories=stories,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.delete("/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    """Delete a story"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Delete audio files if they exist
    if story.final_audio_path and os.path.exists(story.final_audio_path):
        os.remove(story.final_audio_path)
    if story.audio_file_path and os.path.exists(story.audio_file_path):
        os.remove(story.audio_file_path)
    if story.music_file_path and os.path.exists(story.music_file_path):
        os.remove(story.music_file_path)

    db.delete(story)
    db.commit()

    return {"message": "Story deleted successfully"}


def save_story_version(story: Story, db: Session):
    """Helper function to save current story as a version before regenerating"""
    if not story.story_text:
        # Don't save version if story generation never completed
        return

    version = StoryVersion(
        story_id=story.id,
        version_number=story.current_version,
        theme=story.theme,
        character_name=story.character_name,
        age_group=story.age_group,
        story_text=story.story_text,
        story_text_html=story.story_text_html,
        story_title=story.story_title,
        audio_file_path=story.audio_file_path,
        music_file_path=story.music_file_path,
        final_audio_path=story.final_audio_path,
        audio_url=story.audio_url,
        word_count=story.word_count,
        duration_seconds=story.duration_seconds
    )
    db.add(version)
    db.commit()
    logger.info(f"Saved version {version.version_number} for story {story.id}")


@router.post("/{story_id}/regenerate", response_model=StoryResponse, status_code=202)
async def regenerate_story(
    story_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Regenerate an existing story

    This will:
    1. Save the current version to history
    2. Increment version number
    3. Generate a new story with same parameters
    """
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    try:
        # Save current version before regenerating
        save_story_version(story, db)

        # Increment version number
        story.current_version += 1
        story.status = StoryStatus.PENDING
        story.error_message = None
        db.commit()

        logger.info(f"Regenerating story {story_id}, new version: {story.current_version}")

        # Start background generation with same parameters
        from app.core.database import SessionLocal
        bg_db = SessionLocal()

        background_tasks.add_task(
            generate_story_background,
            story_id=story.id,
            theme=story.theme,
            character_name=story.character_name,
            age_group=story.age_group,
            db=bg_db
        )

        db.refresh(story)
        return story

    except Exception as e:
        logger.error(f"Error regenerating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to regenerate story: {str(e)}")


@router.get("/{story_id}/versions", response_model=StoryVersionListResponse)
def get_story_versions(story_id: int, db: Session = Depends(get_db)):
    """Get all versions of a story"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    versions = (
        db.query(StoryVersion)
        .filter(StoryVersion.story_id == story_id)
        .order_by(StoryVersion.version_number.desc())
        .all()
    )

    return StoryVersionListResponse(
        versions=versions,
        total=len(versions)
    )


@router.get("/{story_id}/versions/{version_number}", response_model=StoryVersionResponse)
def get_story_version(
    story_id: int,
    version_number: int,
    db: Session = Depends(get_db)
):
    """Get a specific version of a story"""
    version = (
        db.query(StoryVersion)
        .filter(
            StoryVersion.story_id == story_id,
            StoryVersion.version_number == version_number
        )
        .first()
    )

    if not version:
        raise HTTPException(
            status_code=404,
            detail=f"Version {version_number} not found for story {story_id}"
        )

    return version
