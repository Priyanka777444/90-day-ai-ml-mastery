import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_email(email_type: str, context: dict) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompts = {
        "cold_outreach": f"""Write a short cold outreach LinkedIn message.
Sender: {context['sender_name']}, {context['sender_role']}
Recipient: {context['recipient_name']}, {context['recipient_company']}
Industry: {context['industry']}
Product/Service: {context['product']}
Tone: Professional but friendly, Indian business culture, use 'Sir/Ma'am'
Length: Maximum 5 lines
Goal: Get a reply or demo call""",

        "follow_up": f"""Write a follow up message.
Sender: {context['sender_name']}
Recipient: {context['recipient_name']} Sir/Ma'am
Last interaction: {context['last_interaction']}
Days since: {context['days_since']} days
Tone: Polite, not pushy, respectful
Length: Maximum 3 lines""",

        "proposal": f"""Write a project proposal message.
Client: {context['client_name']}, {context['client_company']}
Project: {context['project_description']}
Timeline: {context['timeline']}
Price: {context['price']}
Tone: Professional, confident, value-focused
Length: Maximum 8 lines""",

        "thank_you": f"""Write a thank you message after a call.
Recipient: {context['recipient_name']} Sir/Ma'am
Company: {context['company']}
Call topic: {context['call_topic']}
Next step: {context['next_step']}
Tone: Warm, professional, grateful
Length: Maximum 4 lines"""
    }
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional business communication expert. Write concise, effective messages."
            },
            {
                "role": "user",
                "content": prompts[email_type]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="✉️",
    layout="wide"
)

st.title("✉️ AI Email Assistant")
st.markdown("Generate professional messages instantly")

email_type = st.selectbox(
    "What do you need to write?",
    [
        "cold_outreach",
        "follow_up", 
        "proposal",
        "thank_you"
    ],
    format_func=lambda x: {
        "cold_outreach": "🎯 Cold Outreach Message",
        "follow_up": "🔄 Follow Up Message",
        "proposal": "📋 Project Proposal",
        "thank_you": "🙏 Thank You After Call"
    }[x]
)

st.markdown("---")

context = {}

if email_type == "cold_outreach":
    col1, col2 = st.columns(2)
    with col1:
        context['sender_name'] = st.text_input("Your name:", value="Priyanka Late")
        context['sender_role'] = st.text_input("Your role:", value="AI/ML Developer")
        context['product'] = st.text_input("What you're offering:", 
                                           value="AI customer support automation tool")
    with col2:
        context['recipient_name'] = st.text_input("Recipient name:")
        context['recipient_company'] = st.text_input("Their company:")
        context['industry'] = st.text_input("Their industry:", value="Ecommerce")

elif email_type == "follow_up":
    col1, col2 = st.columns(2)
    with col1:
        context['sender_name'] = st.text_input("Your name:", value="Priyanka Late")
        context['recipient_name'] = st.text_input("Recipient name:")
    with col2:
        context['last_interaction'] = st.text_input(
            "Last interaction:", 
            value="Shared demo link on WhatsApp"
        )
        context['days_since'] = st.number_input("Days since last message:", 
                                                 value=2, min_value=1)

elif email_type == "proposal":
    col1, col2 = st.columns(2)
    with col1:
        context['sender_name'] = st.text_input("Your name:", value="Priyanka Late")
        context['client_name'] = st.text_input("Client name:")
        context['client_company'] = st.text_input("Client company:")
    with col2:
        context['project_description'] = st.text_area("Project description:", height=100)
        context['timeline'] = st.text_input("Timeline:", value="2-3 weeks")
        context['price'] = st.text_input("Price:", value="₹15,000")

elif email_type == "thank_you":
    col1, col2 = st.columns(2)
    with col1:
        context['sender_name'] = st.text_input("Your name:", value="Priyanka Late")
        context['recipient_name'] = st.text_input("Recipient name:")
        context['company'] = st.text_input("Their company:")
    with col2:
        context['call_topic'] = st.text_input("What was the call about?")
        context['next_step'] = st.text_input("What's the next step?")

generate_btn = st.button("✨ Generate Message", type="primary")

if generate_btn:
    # Set defaults for missing fields
    defaults = {
        'sender_name': 'Priyanka Late',
        'sender_role': 'AI/ML Developer',
        'product': 'AI customer support tool',
        'recipient_name': 'Client',
        'recipient_company': 'Company',
        'industry': 'Ecommerce',
        'last_interaction': 'Connected on LinkedIn',
        'days_since': 2,
        'client_name': 'Client',
        'client_company': 'Company',
        'project_description': 'AI tool',
        'timeline': '2-3 weeks',
        'price': '₹15,000',
        'company': 'Company',
        'call_topic': 'AI solution',
        'next_step': 'Follow up call'
    }
    for key, val in defaults.items():
        if key not in context:
            context[key] = val

    if not all(context.values()):
        st.warning("Please fill all fields!")
    else:
        with st.spinner("Writing your message..."):
            message = generate_email(email_type, context)
        
        st.markdown("---")
        st.markdown("### ✉️ Your Message:")
        st.success(message)
        
        st.text_area(
            "Copy from here:",
            value=message,
            height=200
        )
        
        st.caption("👆 Select all text and copy")