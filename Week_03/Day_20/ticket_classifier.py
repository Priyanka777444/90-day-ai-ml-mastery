#imports
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Customer support tickets (real world examples)
tickets = [
    "My payment failed but money was deducted from my account",
    "I can't login to my account, password reset not working",
    "Where is my order? It's been 2 weeks since I ordered",
    "The product I received is completely different from what I ordered",
    "How do I cancel my subscription?",
    "App keeps crashing every time I open it on iPhone",
    "I want a refund for my last purchase",
    "Your customer service is absolutely terrible",
    "Can you explain what features are included in premium plan?",
    "I was charged twice for the same order",
    "The website is down, I cannot access my account",
    "Product quality is very poor, broke after one day",
    "How do I upgrade my plan?",
    "I never received my confirmation email",
    "This is the worst service I have ever used"
]

#categories
CATEGORIES = [
    "BILLING",      # payment, refund, charges
    "TECHNICAL",    # bugs, crashes, login issues
    "DELIVERY",     # shipping, tracking, orders
    "COMPLAINT",    # angry customers, poor quality
    "GENERAL"       # questions, information
]

def classify_ticket(ticket):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":  f"""You are a customer support ticket classifier.
                Classify the ticket into exactly ONE of these categories:
                {', '.join(CATEGORIES)}
                
                Also detect:
                - PRIORITY: HIGH, MEDIUM, or LOW
                - EMOTION: ANGRY, FRUSTRATED, NEUTRAL, or SATISFIED
                
                Respond in exactly this format:
                CATEGORY: <category>
                PRIORITY: <priority>
                EMOTION: <emotion>
                ACTION: <one sentence on what support team should do>"""
            },
            {
                "role": "user",
                "content": f"Classify this ticket: {ticket}"
            }
        ]
    )
    return response.choices[0].message.content.strip()

def parse_response(response):
    lines = response.split('\n')
    result = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()]= value.strip()
    return result

#process all tickets
print("=" * 70)
print("CUSTOMER SUPPORT TICKET CLASSIFIER")
print("=" * 70)

result = []
for i,ticket in enumerate(tickets,1):
    print(f"\nTickets #{i}: '{ticket}")
    print("-" * 50)
    raw_response = classify_ticket(ticket)
    parsed = parse_response(raw_response)
    result.append(parsed)

    category = parsed.get('CATEGORY', 'UNKNOWN')
    priority = parsed.get('PRIORITY', 'UNKNOWN')
    emotion = parsed.get('EMOTION', 'UNKNOWN')
    action = parsed.get('ACTION', 'UNKNOWN')  

    print(f"Category : {category}")
    print(f"Priority : {priority}")
    print(f"Emotion  : {emotion}")
    print(f"Action   : {action}")

# Summary Dashboard
print("\n" + "=" * 70)
print("SUMMARY DASHBOARD")
print("=" * 70)

# Count by category
category_counts = {}
priority_counts = {}
emotion_counts = {}

for r in result:
    cat = r.get('CATEGORY', 'UNKNOWN')
    pri = r.get('PRIORITY', 'UNKNOWN')
    emo = r.get('EMOTION', 'UNKNOWN')
    
    category_counts[cat] = category_counts.get(cat, 0) + 1
    priority_counts[pri] = priority_counts.get(pri, 0) + 1
    emotion_counts[emo] = emotion_counts.get(emo, 0) + 1


print("\nBy Category:")
for cat, count in sorted(category_counts.items()):
    bar = "█" * count
    print(f"  {cat:<12} {bar} ({count})")

print("\nBy Priority:")
for pri, count in sorted(priority_counts.items()):
    bar = "█" * count
    print(f"  {pri:<12} {bar} ({count})")

print("\nBy Emotion:")
for emo, count in sorted(emotion_counts.items()):
    bar = "█" * count
    print(f"  {emo:<12} {bar} ({count})")

high_priority = [tickets[i] for i, r in enumerate(result) 
                 if r.get('PRIORITY') == 'HIGH']
print(f"\n⚠️  HIGH PRIORITY TICKETS ({len(high_priority)}):")
for t in high_priority:
    print(f"  → {t}")    
