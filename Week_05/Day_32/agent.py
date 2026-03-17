import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

#Agent 1
def classifier_agent(ticket:str) ->dict:
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a support ticket classifier.
Respond in exactly this format:
CATEGORY: BILLING or TECHNICAL or DELIVERY or COMPLAINT or GENERAL
PRIORITY: HIGH or MEDIUM or LOW
EMOTION: ANGRY or FRUSTRATED or NEUTRAL or SATISFIED
SUMMARY: <one sentence summary of the issue>"""
            },
            {"role": "user", "content": f"Classify: {ticket}"}
        ]
    )

    raw = response.choices[0].message.content.strip()
    result = {}
    for field, pattern in [
        ('category', r'CATEGORY:\s*(\w+)'),
        ('priority', r'PRIORITY:\s*(\w+)'),
        ('emotion', r'EMOTION:\s*(\w+)'),
        ('summary', r'SUMMARY:\s*(.+?)$')
    ]:
        match = re.search(pattern, raw, re.MULTILINE)
        if match:
            result[field] = match.group(1).strip()
        result['ticket'] = ticket
        return result
    
    #Agent 2
def reply_agent(classification: dict) ->str:
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a customer support specialist.
Write a professional, empathetic reply to the customer.
-If emotion is ANGRY or FRUSTRATED: start with sincere apology
-If priority is HIGH: promise immediate action
-Always end with next steps
-Sound humman, not robotic"""
            },
            {
                "role": "user",
                "content": f"""Write a reply for this ticket:
Ticket: {classification['ticket']}
Category: {classification.get('category')}
Priority: {classification.get('priority')}
Customer emotion: {classification.get('emotion')}
Summary: {classification.get('summary')}"""    
            }
        ]
    )
    return response.choices[0].message.content.strip()
    
#Agent 3 Escalation Decision Maker
def escalation_agent(classification: dict) ->dict:
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an escalation manager.
Decide if this ticket needs escalation.
Respond in exactly this format:
ESCALATE: YES or NO
REASON: <one sentence>
ASSIGN_TO: BILLING_TEAM or TECH_TEAM or DELIVERY_TEAM or MANAGER or FRONTLINE
SLA_HOURS: <number of hours to resolve>"""
            },
            {
                "role": "user",
                "content": f"""Should this be escalated?
Category: {classification.get('category')}
Priority: {classification.get('priority')}
Emotion: {classification.get('emotion')}
Ticket: {classification['ticket']}"""
            }
        ]
    )
    raw = response.choices[0].message.content.strip()
    result = {}
    for field, pattern in [
        ('escalate', r'ESCALATE:\s*(\w+)'),
        ('reason', r'REASON:\s*(.+?)$'),
        ('assign_to', r'ASSIGN_TO:\s*(\w+)'),
        ('sla_hours', r'SLA_HOURS:\s*(\d+)')
    ]:
        match = re.search(pattern, raw, re.MULTILINE)
        if match:
            result[field] = match.group(1).strip()
    return result

#Orchestrator - runs all 3 agents
def process_ticket(ticket: str) -> dict:
    # Step 1: Classify
    classification = classifier_agent(ticket)
    
    # Step 2: Draft reply
    reply = reply_agent(classification)
    
    # Step 3: Escalation decision
    escalation = escalation_agent(classification)

    return {
        "ticket": ticket,
        "classification": classification,
        "reply": reply,
        "escalation": escalation
    }
