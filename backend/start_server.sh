#!/bin/bash
cd /home/hp/projects/Ai_kids_stories/backend
./venv/bin/python -m uvicorn app.main:app --reload --port 8000
