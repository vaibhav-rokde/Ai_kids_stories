#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# PID file locations
BACKEND_PID_FILE="$SCRIPT_DIR/.backend.pid"
FRONTEND_PID_FILE="$SCRIPT_DIR/.frontend.pid"

# Log file locations
BACKEND_LOG="$SCRIPT_DIR/backend.log"
FRONTEND_LOG="$SCRIPT_DIR/frontend.log"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Starting StoryMagic Application${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if already running
if [ -f "$BACKEND_PID_FILE" ] && kill -0 $(cat "$BACKEND_PID_FILE") 2>/dev/null; then
    echo -e "${YELLOW}Backend is already running (PID: $(cat "$BACKEND_PID_FILE"))${NC}"
else
    # Start Backend
    echo -e "${GREEN}[1/2] Starting Backend...${NC}"

    cd "$SCRIPT_DIR/backend"

    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}Warning: backend/.env file not found. Copy .env.example to .env and configure it.${NC}"
    fi

    # Activate virtual environment and start backend
    if [ -d "venv" ]; then
        source venv/bin/activate

        # Start backend using uvicorn in background
        nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$BACKEND_LOG" 2>&1 &
        BACKEND_PID=$!
        echo $BACKEND_PID > "$BACKEND_PID_FILE"

        # Wait a moment for backend to start
        sleep 2

        echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
        echo -e "  Log: $BACKEND_LOG"
        echo -e "  URL: http://localhost:8000"
        echo -e "  API Docs: http://localhost:8000/api/docs\n"
    else
        echo -e "${RED}Error: Backend virtual environment not found!${NC}"
        echo -e "${YELLOW}Run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
        exit 1
    fi

    cd "$SCRIPT_DIR"
fi

# Check if frontend already running
if [ -f "$FRONTEND_PID_FILE" ] && kill -0 $(cat "$FRONTEND_PID_FILE") 2>/dev/null; then
    echo -e "${YELLOW}Frontend is already running (PID: $(cat "$FRONTEND_PID_FILE"))${NC}"
else
    # Start Frontend
    echo -e "${GREEN}[2/2] Starting Frontend...${NC}"

    cd "$SCRIPT_DIR/frontend"

    # Check if node_modules exists, if not install dependencies
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        npm install
    fi

    # Start frontend in background
    nohup npm run dev > "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

    # Wait a moment for Vite to start
    sleep 3

    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo -e "  Log: $FRONTEND_LOG"
    echo -e "  Check frontend.log for the actual URL (usually http://localhost:5173 or http://localhost:8080)\n"

    cd "$SCRIPT_DIR"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ All services started successfully!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${YELLOW}To stop all services, run:${NC}"
echo -e "  ./stop-all.sh\n"

echo -e "${YELLOW}To view logs:${NC}"
echo -e "  tail -f backend.log"
echo -e "  tail -f frontend.log\n"
