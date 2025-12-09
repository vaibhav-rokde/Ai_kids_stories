from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import init_db
from app.routes import stories
from app.models.schemas import HealthCheckResponse
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="StoryMagic API",
    description="AI-Powered Immersive Kids Story Generation API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stories.router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    logger.info("Starting StoryMagic API...")

    # Create directories
    os.makedirs(settings.STORIES_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Initialize database
    init_db()
    logger.info("Database initialized")

    logger.info(f"StoryMagic API started on {settings.API_HOST}:{settings.API_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down StoryMagic API...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "StoryMagic API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now()
    )


@app.get("/api/v1/stories/audio/{filename}")
async def serve_audio(filename: str):
    """Serve audio files"""
    file_path = os.path.join(settings.STORIES_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
