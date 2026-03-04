# Day 20 - Customer Support Ticket Classifier

## What I Built
AI-powered customer support ticket classifier using Groq + Llama 3.3 70B.
Automatically categorizes, prioritizes and detects customer emotion.

## What I Learned
- Prompt engineering for structured output
- Parsing LLM responses programmatically
- split('\n') vs split() — one character, completely different behavior
- Building summary dashboards from AI output
- Real business application: saves hours of manual ticket sorting

## Result
15 tickets classified:
- BILLING: 5, TECHNICAL: 4, COMPLAINT: 3, DELIVERY: 2, GENERAL: 1
- HIGH priority: 10 tickets flagged automatically
- ANGRY + FRUSTRATED: 12/15 customers detected

## Business Value
500 tickets/day → 0 manual sorting needed
Instant priority flagging → faster response to angry customers

## Tech Used
Python, Groq API, Llama 3.3 70B, python-dotenv

## Key Concept
Structured prompting = predictable parseable LLM output