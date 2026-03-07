import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import plotly.express as px
import re

load_dotenv()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="AI Support Analyzer", page_icon="🎯", layout="wide")
st.title("🎯 AI Support Analyzer")
st.markdown("Powered by Llama 3.3 70B via Groq")

CATEGORIES = ["BILLING", "TECHNICAL", "DELIVERY", "COMPLAINT", "GENERAL"]

def classify_ticket(ticket):
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
    return response.choices[0].message.content.strip()

def parse_response(response):
    result = {}
    category = re.search(r'CATEGORY:\s*(\w+)', response)
    priority = re.search(r'PRIORITY:\s*(\w+)', response)
    emotion = re.search(r'EMOTION:\s*(\w+)', response)
    action = re.search(r'ACTION:\s*(.+?)$', response, re.MULTILINE)
    
    if category: result['CATEGORY'] = category.group(1).strip()
    if priority: result['PRIORITY'] = priority.group(1).strip()
    if emotion: result['EMOTION'] = emotion.group(1).strip()
    if action: result['ACTION'] = action.group(1).strip()
    return result

# Sidebar
st.sidebar.title("📋 Input Tickets")
input_method = st.sidebar.radio("Choose input method:", ["Paste Tickets", "Use Sample Data"])

if input_method == "Use Sample Data":
    tickets_text = """My payment failed but money was deducted
I can't login, password reset not working
Where is my order? It's been 2 weeks
App keeps crashing on iPhone
I want a refund for my last purchase
Your customer service is absolutely terrible
I was charged twice for the same order
Product quality is very poor, broke after one day
How do I upgrade my plan?
This is the worst service I have ever used"""
else:
    tickets_text = st.sidebar.text_area(
        "Paste tickets (one per line):",
        height=200,
        placeholder="Enter customer tickets here..."
    )

analyze_btn = st.sidebar.button("🚀 Analyze Tickets", type="primary")

if analyze_btn and tickets_text:

    with st.spinner("AI is analyzing support tickets..."):
        tickets = [t.strip() for t in tickets_text.split('\n') if t.strip()]

        st.markdown(f"### Analyzing {len(tickets)} tickets...")
        progress = st.progress(0)
    status = st.empty()

    results = []
    for i, ticket in enumerate(tickets):
        status.text(f"Processing ticket {i+1}/{len(tickets)}...")
        raw = classify_ticket(ticket)
        parsed = parse_response(raw)
        parsed['ticket'] = ticket
        results.append(parsed)
        progress.progress((i+1)/len(tickets))

    status.text("Analysis complete! ✅")
    df = pd.DataFrame(results)

    # KPI Row - use ORIGINAL column names before rename
    st.markdown("---")
    st.markdown("## 📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", len(tickets))
    with col2:
        high = len(df[df['PRIORITY'] == 'HIGH'])
        st.metric("🔴 High Priority", high)
    with col3:
        angry = len(df[df['EMOTION'].isin(['ANGRY', 'FRUSTRATED'])])
        st.metric("😤 Unhappy Customers", angry)
    with col4:
        billing = len(df[df['CATEGORY'] == 'BILLING'])
        st.metric("💳 Billing Issues", billing)

    # Charts - use ORIGINAL column names
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = px.pie(df, names='CATEGORY', title='By Category')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(
            df['PRIORITY'].value_counts().reset_index(),
            x='PRIORITY', y='count',
            title='By Priority',
            color='PRIORITY',
            color_discrete_map={'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green'}
        )
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = px.pie(df, names='EMOTION', title='Customer Emotions')
        st.plotly_chart(fig, use_container_width=True)

    # High Priority Alert
    st.markdown("---")
    high_priority = df[df['PRIORITY'] == 'HIGH']  # ← square brackets
    if len(high_priority) > 0:
        st.error(f"⚠️ {len(high_priority)} HIGH PRIORITY tickets need immediate attention!")
        for _, row in high_priority.iterrows():  # ← iterrows()
            with st.expander(f"🔴 {row['ticket'][:50]}..."):  # ← bracket outside
                st.write(f"**Category:** {row['CATEGORY']}")
                st.write(f"**Emotion:** {row['EMOTION']}")
                st.write(f"**Action:** {row['ACTION']}")

    # Rename only for final table display
    df_display = df.rename(columns={
        'CATEGORY': 'Category',
        'PRIORITY': 'Priority',
        'EMOTION': 'Emotion',
        'ACTION': 'Recommended Action',
        'ticket': 'Ticket'
    })

    st.markdown("---")
    st.markdown("### 📋 All Tickets")
    st.dataframe(df_display, use_container_width=True)

    csv = df_display.to_csv(index=False)
    st.download_button(
        label="📥 Download Report (CSV)",
        data=csv,
        file_name="support_analysis.csv",
        mime="text/csv"
    )

elif analyze_btn:
    st.warning("Please enter some tickets first!")
else:
    st.info("👈 Add tickets in the sidebar and click Analyze!")