import streamlit as st
import pandas as pd
import plotly.express as px
from demo_generator import generate_sample_data, classify_ticket

st.set_page_config(
    page_title="AI Demo Generator",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Solutions Demo")
st.markdown("See how AI can transform YOUR business support")

# Input section
st.markdown("### 👇 Enter your business details")
col1, col2 = st.columns(2)

with col1:
    business_name = st.text_input(
        "Business name:",
        placeholder="e.g. Shopperbeats"
    )
with col2:
    industry = st.selectbox(
        "Industry:",
        [
            "Ecommerce",
            "Legal Services",
            "Healthcare",
            "Education",
            "Real Estate",
            "Restaurant",
            "SaaS/Technology",
            "Retail",
            "Logistics"
        ]
    )

generate_btn = st.button(
    "🚀 Generate My Custom Demo",
    type="primary",
    use_container_width=True
)

if generate_btn and business_name:
    # Step 1: Generate sample data
    with st.spinner(f"Generating sample data for {business_name}..."):
        try:
            data = generate_sample_data(business_name, industry)
        except Exception as e:
            st.error(f"Error generating data: {e}")
            st.stop()

    st.success(f"✅ Generated sample data for {business_name}!")
    st.markdown("---")

    # Step 2: Show FAQ
    st.markdown(f"## 📋 {business_name} — Sample FAQ")
    st.text_area("Generated FAQ:", data.get('faq', ''), height=200)

    # Step 3: Classify sample tickets
    st.markdown("---")
    st.markdown(f"## 🎫 AI Ticket Classification for {business_name}")

    tickets = data.get('tickets', [])
    
    with st.spinner("Classifying sample tickets..."):
        results = []
        progress = st.progress(0)
        for i, ticket in enumerate(tickets):
            result = classify_ticket(ticket, business_name, industry)
            results.append(result)
            progress.progress((i+1)/len(tickets))

    df = pd.DataFrame(results)

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tickets", len(df))
    with col2:
        high = len(df[df['priority'] == 'HIGH'])
        st.metric("🔴 High Priority", high)
    with col3:
        angry = len(df[df['emotion'].isin(['ANGRY', 'FRUSTRATED'])])
        st.metric("😤 Unhappy Customers", angry)

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='category', title='Tickets by Category')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(
            df['priority'].value_counts().reset_index(),
            x='priority', y='count',
            color='priority',
            color_discrete_map={
                'HIGH': 'red',
                'MEDIUM': 'orange',
                'LOW': 'green'
            },
            title='Tickets by Priority'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Ticket table
    st.markdown("### 📊 Classified Tickets")
    st.dataframe(df, use_container_width=True)

    # Policy section
    st.markdown("---")
    st.markdown(f"## 📜 {business_name} — AI-Generated Policy Summary")
    st.info(data.get('policy', ''))

    # CTA
    st.markdown("---")
    st.success(f"""
    ✅ This is what AI can do for {business_name}:
    
    → Classify every support ticket automatically
    → Detect angry customers before they escalate  
    → Prioritize HIGH urgency issues instantly
    → Save 3-4 hours of manual triage daily
    
    **Want this built for your real data? Let's talk.**
    """)

elif generate_btn:
    st.warning("Please enter your business name!")
else:
    st.info("👆 Enter your business details above to see a live AI demo")