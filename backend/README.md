# StoryMagic Backend API

AI-Powered Immersive Kids Story Generation Backend built with FastAPI, Gemini AI, Azure TTS, and Mubert.

## Features

- **Story Generation**: AI-powered story creation using Google Gemini
- **Natural Narration**: High-quality Text-to-Speech using Azure Cognitive Services
- **Background Music**: Dynamic music generation using Mubert API
- **Audio Mixing**: Professional audio mixing with PyDub
- **Workflow Orchestration**: LangGraph-based pipeline management
- **SQLite Database**: Story management and metadata storage
- **RESTful API**: FastAPI-based REST endpoints

## Technology Stack

- **Framework**: FastAPI
- **AI Services**:
  - Google Gemini (Story Generation)
  - Azure Cognitive Services (Text-to-Speech)
  - Mubert (Music Generation)
- **Workflow**: LangGraph
- **Database**: SQLite + SQLAlchemy
- **Audio**: PyDub
- **Python**: 3.10+

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install System Dependencies (for audio processing)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download and install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Azure Text-to-Speech
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here

# Mubert Music API
MUBERT_API_KEY=your_mubert_api_key_here
MUBERT_LICENSE=your_mubert_license_here
```

## Getting API Keys

### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to `.env`

### Azure Speech Services
1. Go to [Azure Portal](https://portal.azure.com)
2. Create a "Speech Services" resource
3. Copy the Key and Region to `.env`

### Mubert API
1. Go to [Mubert API](https://mubert.com/api)
2. Sign up for API access
3. Get your API key and license

## Running the Server

### Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or simply:

```bash
python app/main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Create Story
```
POST /api/v1/stories/
Content-Type: application/json

{
  "theme": "A brave squirrel who learns to share",
  "character_name": "Squeaky",
  "age_group": "5-7"
}
```

### Get Story Status
```
GET /api/v1/stories/{story_id}/status
```

### Get Story Details
```
GET /api/v1/stories/{story_id}
```

### List Stories
```
GET /api/v1/stories/?skip=0&limit=20
```

### Get Audio File
```
GET /api/v1/stories/audio/{filename}
```

### Delete Story
```
DELETE /api/v1/stories/{story_id}
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Project Structure

```
backend/
├── app/
│   ├── core/           # Configuration and database
│   │   ├── config.py
│   │   └── database.py
│   ├── models/         # Database models and schemas
│   │   ├── story.py
│   │   └── schemas.py
│   ├── routes/         # API endpoints
│   │   └── stories.py
│   ├── services/       # Business logic
│   │   ├── story_generator.py
│   │   ├── tts_service.py
│   │   ├── music_service.py
│   │   ├── audio_mixer.py
│   │   └── story_orchestrator.py
│   ├── utils/          # Utilities
│   └── main.py         # FastAPI app
├── stories/            # Generated audio files
├── logs/               # Application logs
├── requirements.txt
├── .env.example
└── README.md
```

## Workflow

The story generation follows this LangGraph-orchestrated workflow:

```
1. Generate Story Text (Gemini AI)
   ↓
2. Generate Speech Narration (Azure TTS)
   ↓
3. Generate Background Music (Mubert)
   ↓
4. Mix Audio (PyDub)
   ↓
5. Save Final MP3
```

## Development

### Run Tests
```bash
pytest
```

### Code Linting
```bash
black app/
flake8 app/
```

## Troubleshooting

### FFmpeg Not Found
Make sure FFmpeg is installed and in your PATH:
```bash
ffmpeg -version
```

### Azure TTS Authentication Error
Verify your Azure Speech Key and Region are correct in `.env`

### Gemini API Rate Limit
Gemini API has rate limits. Consider implementing retry logic or upgrading your plan.

### Database Locked
If you get "database is locked" errors, it's because SQLite doesn't handle concurrent writes well. Consider upgrading to PostgreSQL for production.

## Cost Estimation

Based on our research for 100,000 stories:

- **Gemini API**: $650
- **Azure TTS**: $4,320
- **Mubert Music**: $30,000
- **Total**: ~$35,970 ($0.36 per story)

See `research_phase1.md` for detailed cost analysis and optimization strategies.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please create an issue in the GitHub repository.
