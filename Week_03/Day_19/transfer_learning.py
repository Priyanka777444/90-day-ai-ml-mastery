import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API"))

# Sentiment analysis function
def analyze_sentiment(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a sentiment analyzer. 
                Analyze the sentiment of the given text.
                Respond in exactly this format:
                SENTIMENT: POSITIVE or NEGATIVE
                CONFIDENCE: HIGH or MEDIUM or LOW
                REASON: one sentence explanation"""
            },
            {
                "role": "user",
                "content": f"Analyze this: {text}"
            }
        ]
    )
    return response.choices[0].message.content

# Test sentences
test_sentences = [
    "I love this product, it is amazing",
    "This is terrible, waste of money",
    "Outstanding quality, highly recommend",
    "Broken on arrival, very frustrated",
    "decent product, nothing special",
    "Best purchase I made this year",
    "Complete garbage, avoid this"
]

print("=" * 60)
print("SENTIMENT ANALYSIS USING LLAMA3 + GROQ")
print("=" * 60)

for sentence in test_sentences:
    print(f"\nText: '{sentence}'")
    print("-" * 40)
    result = analyze_sentiment(sentence)
    print(result)

print("\n" + "=" * 60)

# Batch analysis with summary
print("\nQUICK SUMMARY TABLE")
print("=" * 60)

def quick_sentiment(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Respond with only one word: POSITIVE or NEGATIVE"
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response.choices[0].message.content.strip()

results = []
for sentence in test_sentences:
    sentiment = quick_sentiment(sentence)
    results.append((sentence, sentiment))
    print(f"{'POSITIVE ✅' if 'POSITIVE' in sentiment else 'NEGATIVE ❌'} | {sentence}")

positive = sum(1 for _, s in results if 'POSITIVE' in s)
negative = sum(1 for _, s in results if 'NEGATIVE' in s)
print(f"\nTotal: {positive} Positive, {negative} Negative")