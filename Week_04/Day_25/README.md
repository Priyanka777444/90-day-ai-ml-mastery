# Day 25 - Database Integration

## What I Built
Added SQLite database to store all classified tickets permanently.
Tickets survive server restarts. Historical data queryable via API.

## What I Learned
- SQLAlchemy ORM maps Python classes to database tables
- db.close() releases connection back to pool
- RAM = temporary, Disk = permanent
- GET /history returns all past tickets
- GET /stats returns aggregate counts

## New Endpoints
GET /history → all saved tickets
GET /stats   → category/priority/emotion counts

## Tech Used
Python, FastAPI, SQLAlchemy, SQLite