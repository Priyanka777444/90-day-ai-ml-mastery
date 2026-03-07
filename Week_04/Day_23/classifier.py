import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CATEGORIES = ["BILLING", "TECHNICAL", "DELIVERY", "COMPLAINT", "GENERAL"]

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_ticket(ticket: str) -> dict:
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   
        messages=[
            {
                "role": "system",
                "content": f"""You are a customer support ticket classifier.
                Classify into ONE of: {', '.join(CATEGORIES)}
                Respond in exactly this format:
                CATEGORY: <category>
                PRIORITY: HIGH or MEDIUM or LOW
                EMOTION: ANGRY or FRUSTRATED or NEUTRAL or SATISFIED
                ACTION: <one sentence action>"""
            },
            {
                "role": "user",
                "content": f"Classify: {ticket}"
            }
        ]
    )
    raw = response.choices[0].message.content.strip()
    return parse_response(raw)

def parse_response(response: str) -> dict:
    result = {}
    category = re.search(r'CATEGORY:\s*(\w+)', response)
    priority = re.search(r'PRIORITY:\s*(\w+)', response)
    emotion = re.search(r'EMOTION:\s*(\w+)', response)
    action = re.search(r'ACTION:\s*(.+?)$', response, re.MULTILINE)

    if category: result['category'] = category.group(1).strip()
    if priority: result['priority'] = priority.group(1).strip()
    if emotion: result['emotion'] = emotion.group(1).strip()
    if action: result['action'] = action.group(1).strip()
    return result

def classify_batch(tickets: list) -> list:
    return [
        {**classify_ticket(ticket), 'ticket': ticket}
        for ticket in tickets
    ]