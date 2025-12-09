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

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Stopping StoryMagic Application${NC}"
echo -e "${BLUE}========================================${NC}\n"

STOPPED_COUNT=0

# Stop Backend
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")

    if kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${YELLOW}Stopping Backend (PID: $BACKEND_PID)...${NC}"
        kill "$BACKEND_PID" 2>/dev/null

        # Wait for graceful shutdown (max 5 seconds)
        for i in {1..5}; do
            if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done

        # Force kill if still running
        if kill -0 "$BACKEND_PID" 2>/dev/null; then
            echo -e "${YELLOW}Force stopping Backend...${NC}"
            kill -9 "$BACKEND_PID" 2>/dev/null
        fi

        echo -e "${GREEN}✓ Backend stopped${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    else
        echo -e "${YELLOW}Backend process not running (stale PID file)${NC}"
    fi

    rm -f "$BACKEND_PID_FILE"
else
    echo -e "${YELLOW}Backend not running (no PID file found)${NC}"
fi

echo ""

# Stop Frontend
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")

    if kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${YELLOW}Stopping Frontend (PID: $FRONTEND_PID)...${NC}"

        # Kill the main process and any child processes (Vite spawns multiple processes)
        pkill -P "$FRONTEND_PID" 2>/dev/null
        kill "$FRONTEND_PID" 2>/dev/null

        # Wait for graceful shutdown (max 5 seconds)
        for i in {1..5}; do
            if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done

        # Force kill if still running
        if kill -0 "$FRONTEND_PID" 2>/dev/null; then
            echo -e "${YELLOW}Force stopping Frontend...${NC}"
            kill -9 "$FRONTEND_PID" 2>/dev/null
        fi

        echo -e "${GREEN}✓ Frontend stopped${NC}"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    else
        echo -e "${YELLOW}Frontend process not running (stale PID file)${NC}"
    fi

    rm -f "$FRONTEND_PID_FILE"
else
    echo -e "${YELLOW}Frontend not running (no PID file found)${NC}"
fi

echo ""

# Also kill any remaining node/vite processes (safety cleanup)
VITE_PIDS=$(pgrep -f "vite" 2>/dev/null)
if [ ! -z "$VITE_PIDS" ]; then
    echo -e "${YELLOW}Cleaning up remaining Vite processes...${NC}"
    pkill -f "vite" 2>/dev/null
fi

# Kill any remaining uvicorn processes (safety cleanup)
UVICORN_PIDS=$(pgrep -f "uvicorn.*app.main:app" 2>/dev/null)
if [ ! -z "$UVICORN_PIDS" ]; then
    echo -e "${YELLOW}Cleaning up remaining Uvicorn processes...${NC}"
    pkill -f "uvicorn.*app.main:app" 2>/dev/null
fi

echo -e "${BLUE}========================================${NC}"
if [ $STOPPED_COUNT -gt 0 ]; then
    echo -e "${GREEN}✓ All services stopped successfully!${NC}"
else
    echo -e "${YELLOW}No services were running${NC}"
fi
echo -e "${BLUE}========================================${NC}\n"

echo -e "${YELLOW}To start all services again, run:${NC}"
echo -e "  ./start-all.sh\n"
