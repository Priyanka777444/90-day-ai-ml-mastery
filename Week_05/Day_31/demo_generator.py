import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_sample_data(business_name: str, industry: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Generate realistic sample data for a business called "{business_name}" 
in the {industry} industry. 

Return ONLY a JSON object with exactly this structure:
{{
    "faq": "10 realistic FAQ questions and answers for this business",
    "tickets": ["ticket1", "ticket2", "ticket3", "ticket4", "ticket5"],
    "policy": "A realistic refund/service policy for this business (200 words)"
}}

Make it specific to {industry}. No extra text, just JSON."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    import json
    text = response.choices[0].message.content.strip()
    # Remove markdown if present
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def classify_ticket(ticket: str, business_name: str, industry: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a support classifier for {business_name}, 
a {industry} business.
Respond in exactly this format:
CATEGORY: BILLING or TECHNICAL or DELIVERY or COMPLAINT or GENERAL
PRIORITY: HIGH or MEDIUM or LOW
EMOTION: ANGRY or FRUSTRATED or NEUTRAL or SATISFIED
ACTION: <one sentence>"""
            },
            {
                "role": "user", 
                "content": f"Classify: {ticket}"
            }
        ]
    )
    
    import re
    raw = response.choices[0].message.content.strip()
    result = {}
    
    for field, pattern in [
        ('category', r'CATEGORY:\s*(\w+)'),
        ('priority', r'PRIORITY:\s*(\w+)'),
        ('emotion', r'EMOTION:\s*(\w+)'),
        ('action', r'ACTION:\s*(.+?)$')
    ]:
        match = re.search(pattern, raw, re.MULTILINE)
        if match:
            result[field] = match.group(1).strip()
    
    result['ticket'] = ticket
    return result