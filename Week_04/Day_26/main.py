from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from classifier import classify_ticket, classify_batch
from database import init_db, save_ticket, get_all_tickets, get_stats
from auth import authenticate_user, create_access_token, verify_token

init_db()
app = FastAPI(
    title="AI Support Ticket Classifier",
    description="Secure with API",
    version="3.0.0"
)

security = HTTPBearer()

#response model
class TicketRequest(BaseModel):
    ticket: str

class BatchRequest(BaseModel):
    tickets: List[str]

class LoginRequest(BaseModel):
    username: str
    password: str

#auth dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return username

#public riutes
@app.get("/")
def root():
    return {"message": "AI Support Classifier API v3.0 - JWT Protected"}

@app.get("/health")
def health():
    return { "status": "healthy"}

@app.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token = create_access_token(request.username)
    return {
        "access_toekn": token,
        "token_type": "bearer",
        "message": f"Welcome{request.username}"
    }

# Protected routes (require JWT token)
@app.post("/classify")
def classify_single(
    request: TicketRequest,
    current_user: str = Depends(get_current_user)
):
    if not request.ticket.strip():
        raise HTTPException(status_code=400, detail="Ticket cannot be empty")
    
    result = classify_ticket(request.ticket)
    result['ticket'] =request.ticket
    request['classified_by'] = current_user
    record_id = save_ticket(result)
    result['id'] = record_id
    return result

@app.post("/classify/batch")
def classify_batch(
    request: BatchRequest,
    current_user: str = Depends(get_current_user)
):
    if not request.tickets():
        raise HTTPException(status_code=400, detail="Tickets List cannot be empty")
    
    results = classify_batch(request.tickets)
    for r in results:
        save_ticket(r)

    high_priority = sum(1 for r in results if r.get('priority')=='HIGH')
    unhappy = sum(1 for r in results if r.get('emotion') in ['ANGRY', 'FRUSTRATED'])

    return {
        "total": len(results),
        "high_priority_count": high_priority,
        "unhappy_customers": unhappy,
        "classified_by": current_user,
        "results": results
    }

@app.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    tickets = get_all_tickets()
    return {
        "total": len(tickets),
        "requested_by": current_user,
        "tickets": [
            {
                "id": t.id,
                "ticket": t.ticket,
                "category": t.category,
                "priority": t.priority,
                "emotion": t.emotion,
                "created_at": str(t.created_at)
            }
            for t in tickets
        ]
    }
    
@app.get("/stats")
def get_statistics(current_user: str = Depends(get_current_user)):
    stats = get_stats()
    stats['requested_by'] = current_user
    return stats
