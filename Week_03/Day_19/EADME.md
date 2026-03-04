# Day 19 - Sentiment Analysis with LLM + Groq API

## What I Built
Sentiment analyzer using Llama 3.3 70B via Groq API.
Two modes: detailed analysis + quick batch summary.

## What I Learned
- Always use .env for API keys, never hardcode
- .gitignore protects sensitive files from GitHub
- Groq API = free, fast alternative to OpenAI
- Prompt engineering controls output format precisely
- LLMs understand nuanced sentiment better than basic models
- "decent product, nothing special" → NEGATIVE (subtle detection)

## Result
7 sentences analyzed
3 Positive, 4 Negative
Detected subtle negativity in "decent product, nothing special"

## Tech Used
Python, Groq API, Llama 3.3 70B, python-dotenv

## Key Concept
System prompt = controls how LLM behaves
User prompt = the actual input
Together = powerful, controllable AI pipeline