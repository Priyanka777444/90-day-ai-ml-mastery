from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from classifier import classify_ticket, classify_batch

app = FastAPI(
    title="AI Support Ticket Classifier",
    description="Classify customer support tickets using Llama 3.3 70B",
    version="1.0.0"
)

#request model
class TicketRequest(BaseModel):
    ticket : str
class BatchRequest(BaseModel):
    tickets: List[str]

#Routes
@app.get("/")
def root():
    return{
        "message": "AI Support Classifier API",
        "version": "1.0.0",
        "endpoints": ["/classify", "/classify/batch", "/health"]
    }

@app.get("/health")
def health():
    return{"status": "healthy"}

@app.post("/classify")
def Classify_single(request:TicketRequest):
    if not request.ticket.strip():
        raise HTTPException(status_code=400, detail="Ticket cannot be empty")
    
    result = classify_ticket(request.ticket)
    result['ticket']= request.ticket
    return result

@app.post("/classify/batch")
def classify_batch_endpoint(request:BatchRequest):
    if not request.tickets:
        raise HTTPException(status_code=400, detail="Tickets List cannot be empty")
    if len(request.tickets)>50:
        raise HTTPException(status_code=400, detail="Maximum 50 tickets per batch")
    
    results = classify_batch(request.tickets)

    #summary
    high_priority = sum(1 for r in results if r.get('priority')=='High')
    unhappy = sum(1 for r in results if r.get('emotion') in ['Angry', 'Frustrated'])

    return {
        "total": len(results),
        "high_priority_count": high_priority,
        "unhappy_customers": unhappy,
        "results": results
    }


