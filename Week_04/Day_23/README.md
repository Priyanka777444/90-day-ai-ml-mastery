# Day 23 - FastAPI Backend

## What I Built
REST API for customer support ticket classification.
Separated ML logic into reusable module (classifier.py).

## What I Learned
- FastAPI auto-generates /docs documentation
- GET = read data, POST = send data for processing
- Separation of concerns: classifier.py vs main.py
- load_dotenv() needs () — without parentheses it does nothing
- Client initialization inside function, not module level
- Pydantic models validate request/response automatically

## Endpoints
GET  /           → API info
GET  /health     → Health check
POST /classify   → Classify single ticket
POST /classify/batch → Classify multiple tickets

## Result
API running on localhost:8000
POST /classify returns category, priority, emotion, action

## Tech Used
Python, FastAPI, Uvicorn, Groq API, Pydantic