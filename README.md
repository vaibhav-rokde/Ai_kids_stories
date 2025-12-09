# StoryMagic - AI-Powered Kids Story Generation

An immersive storytelling platform that generates personalized children's stories with narration and background music using AI.

## Features

- **AI Story Generation**: Personalized stories using Google Gemini
- **Natural Narration**: High-quality speech using Azure Text-to-Speech
- **Background Music**: Real-time music generation using Google Gemini Lyria RealTime
- **Interactive UI**: Modern React frontend with Shadcn UI components
- **RESTful API**: FastAPI backend with async support

## Technology Stack

### Backend
- **Framework**: FastAPI
- **AI Services**: Google Gemini, Azure TTS, Gemini Lyria RealTime
- **Workflow**: LangGraph
- **Database**: SQLite + SQLAlchemy
- **Audio**: PyDub
- **Python**: 3.10+

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Shadcn UI + Radix UI
- **Styling**: Tailwind CSS
- **State Management**: TanStack Query (React Query)
- **Routing**: React Router v6

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm
- FFmpeg (for audio processing)

### 1. Clone the Repository

```bash
git clone git@github.com-personal:vaibhav-rokde/Ai_kids_stories.git
cd Ai_kids_stories
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

**Required API Keys:**
- `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- `AZURE_SPEECH_KEY` & `AZURE_SPEECH_REGION`: Get from [Azure Portal](https://portal.azure.com)

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Start All Services

From the project root:

```bash
./start-all.sh
```

This will start:
- **Backend**: http://localhost:8000
  - API Docs: http://localhost:8000/api/docs
- **Frontend**: http://localhost:5173

### 5. Stop All Services

```bash
./stop-all.sh
```

## Manual Start (Optional)

### Start Backend Manually

```bash
cd backend
source venv/bin/activate
python app/main.py
```

Or:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Manually

```bash
cd frontend
npm run dev
```

## Scripts

### start-all.sh
Starts both backend and frontend services in the background.

**Features:**
- Checks for virtual environment and dependencies
- Auto-installs frontend dependencies if needed
- Logs output to `backend.log` and `frontend.log`
- Creates PID files for process management
- Detects if services are already running

**Usage:**
```bash
./start-all.sh
```

### stop-all.sh
Stops all running services gracefully.

**Features:**
- Graceful shutdown with 5-second timeout
- Force kills if processes don't stop
- Cleans up PID files
- Safety cleanup for stray processes

**Usage:**
```bash
./stop-all.sh
```

## View Logs

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log
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

### List Stories
```
GET /api/v1/stories/?skip=0&limit=20
```

See full API documentation at http://localhost:8000/api/docs

## Project Structure

```
Ai_kids_stories/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── core/            # Config and database
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── stories/             # Generated audio files
│   ├── venv/                # Python virtual environment
│   ├── requirements.txt
│   └── README.md
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── pages/          # Page components
│   │   └── App.tsx         # Main app
│   ├── public/
│   ├── package.json
│   └── README.md
├── start-all.sh            # Start all services
├── stop-all.sh             # Stop all services
└── README.md               # This file
```

## Cost Estimation (100K Stories)

- **Gemini API**: $650 (story generation) + FREE (Lyria music during preview)
- **Azure TTS**: $4,320
- **Total**: ~$4,970 ($0.05 per story)

**86% cost reduction** compared to commercial music APIs!

## Development

### Backend Testing
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Build
```bash
cd frontend
npm run build
```

### Code Linting
```bash
# Backend
cd backend
black app/
flake8 app/

# Frontend
cd frontend
npm run lint
```

## Troubleshooting

### FFmpeg Not Found
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Check installation
ffmpeg -version
```

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

### Services Not Stopping
```bash
# Force stop everything
./stop-all.sh

# Manual cleanup
pkill -f "uvicorn.*app.main:app"
pkill -f "vite"
```

## Research & Documentation

See `backend/research_phase1.md` for:
- Detailed AI service comparison
- Cost analysis and optimization strategies
- Technical architecture decisions

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please create an issue in the GitHub repository.

---

Built with ❤️ using Google Gemini, Azure TTS, and Gemini Lyria RealTime
