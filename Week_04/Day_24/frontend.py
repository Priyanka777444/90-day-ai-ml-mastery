import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# FastAPI backend URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Support Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Support Analyzer")
st.markdown("Frontend → FastAPI Backend → Llama 3.3 70B")

# Health check
def check_backend():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

# Classify single ticket
def classify_ticket(ticket):
    response = requests.post(
        f"{API_URL}/classify",
        json={"ticket": ticket},
        timeout=30
    )
    return response.json()

# Classify batch
def classify_batch(tickets):
    response = requests.post(
        f"{API_URL}/classify/batch",
        json={"tickets": tickets},
        timeout=120
    )
    return response.json()

# Backend status
if check_backend():
    st.sidebar.success("✅ Backend Connected")
else:
    st.sidebar.error("❌ Backend Offline - Start FastAPI first!")
    st.error("Start your FastAPI backend: python -m uvicorn main:app --reload")
    st.stop()

# Sidebar
st.sidebar.title("📋 Input Tickets")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Paste Tickets", "Use Sample Data"]
)

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
    tickets = [t.strip() for t in tickets_text.strip().split('\n') if t.strip()]

    with st.spinner(f"Analyzing {len(tickets)} tickets via API..."):
        data = classify_batch(tickets)

    results = data['results']
    df = pd.DataFrame(results)

    # KPI Row
    st.markdown("---")
    st.markdown("## 📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", data['total'])
    with col2:
        st.metric("🔴 High Priority", data['high_priority_count'])
    with col3:
        st.metric("😤 Unhappy Customers", data['unhappy_customers'])
    with col4:
        billing = len(df[df['category'] == 'BILLING'])
        st.metric("💳 Billing Issues", billing)

    # Charts
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = px.pie(df, names='category', title='By Category')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(
            df['priority'].value_counts().reset_index(),
            x='priority', y='count',
            title='By Priority',
            color='priority',
            color_discrete_map={'HIGH':'red','MEDIUM':'orange','LOW':'green'}
        )
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        fig = px.pie(df, names='emotion', title='Customer Emotions')
        st.plotly_chart(fig, use_container_width=True)

    # High Priority Alert
    st.markdown("---")
    high_priority = df[df['priority'] == 'HIGH']
    if len(high_priority) > 0:
        st.error(f"⚠️ {len(high_priority)} HIGH PRIORITY tickets!")
        for _, row in high_priority.iterrows():
            with st.expander(f"🔴 {row['ticket'][:50]}..."):
                st.write(f"**Category:** {row['category']}")
                st.write(f"**Emotion:** {row['emotion']}")
                st.write(f"**Action:** {row['action']}")

    # Table
    st.markdown("---")
    st.markdown("### 📋 All Tickets")
    st.dataframe(df, use_container_width=True)

    # Download
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="support_analysis.csv",
        mime="text/csv"
    )

elif analyze_btn:
    st.warning("Please enter some tickets first!")
else:
    st.info("👈 Add tickets in the sidebar and click Analyze!")