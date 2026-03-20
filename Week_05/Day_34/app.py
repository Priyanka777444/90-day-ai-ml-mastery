import streamlit as st
import pandas as pd
import plotly.express as px
import os
from groq import Groq
from dotenv import load_dotenv
import io

load_dotenv()

def analyze_data(df: pd.DataFrame, question: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Prepare data summary for LLM
    summary = f"""
Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns
Columns: {list(df.columns)}
Data types: {df.dtypes.to_dict()}
Sample data (first 5 rows):
{df.head().to_string()}
Basic statistics:
{df.describe().to_string()}
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a data analyst expert.
Analyze the given dataset and answer questions about it.
Give clear, actionable business insights.
Use simple language — no technical jargon.
Format your answer with bullet points where needed."""
            },
            {
                "role": "user",
                "content": f"""Dataset info:
{summary}

Question: {question}

Give specific insights based on the actual data."""
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def auto_visualize(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    charts = []
    
    # Chart 1 — Distribution of first numeric column
    if numeric_cols:
        fig = px.histogram(
            df, x=numeric_cols[0],
            title=f"Distribution of {numeric_cols[0]}"
        )
        charts.append(fig)
    
    # Chart 2 — If categorical + numeric exist
    if categorical_cols and numeric_cols:
        fig = px.bar(
            df.groupby(categorical_cols[0])[numeric_cols[0]].mean().reset_index(),
            x=categorical_cols[0],
            y=numeric_cols[0],
            title=f"Average {numeric_cols[0]} by {categorical_cols[0]}"
        )
        charts.append(fig)
    
    # Chart 3 — Correlation if multiple numeric
    if len(numeric_cols) >= 2:
        fig = px.scatter(
            df, x=numeric_cols[0], y=numeric_cols[1],
            title=f"{numeric_cols[0]} vs {numeric_cols[1]}"
        )
        charts.append(fig)
    
    return charts

# App
st.set_page_config(
    page_title="AI Data Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyzer")
st.markdown("Upload any CSV — get instant insights and visualizations")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file:", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str)
    df = df.convert_dtypes()
    
    st.success(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Data preview
    with st.expander("👀 Preview Data"):
        st.dataframe(df.head(10).astype(str), use_container_width=True)
    
    with st.expander("📈 Basic Statistics"):
        st.dataframe(df.describe().astype(str), use_container_width=True)
    
    st.markdown("---")
    
    # Auto visualizations
    st.markdown("### 📊 Auto-Generated Charts")
    charts = auto_visualize(df)
    
    if charts:
        cols = st.columns(min(len(charts), 3))
        for i, chart in enumerate(charts):
            with cols[i % 3]:
                st.plotly_chart(chart, use_container_width=True)
    
    st.markdown("---")
    
    # AI Q&A
    st.markdown("### 🤖 Ask AI About Your Data")
    
    # Sample questions
    st.markdown("**Try these:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("What are the key insights?", key="q1"):
            st.session_state.question = "What are the key insights from this dataset?"
    with col2:
        if st.button("Any anomalies or outliers?", key="q2"):
            st.session_state.question = "Are there any anomalies or outliers in this data?"
    with col3:
        if st.button("Business recommendations?", key="q3"):
            st.session_state.question = "What business recommendations can you make from this data?"
    
    question = st.text_input(
        "Or ask your own question:",
        value=st.session_state.get('question', '')
    )
    
    if question:
        with st.spinner("AI is analyzing your data..."):
            answer = analyze_data(df, question)
        
        st.markdown("### 💡 AI Insights:")
        st.success(answer)
    
    st.markdown("---")
    
    # Download cleaned data
    csv = df.to_csv(index=False)
    st.download_button(
        "📥 Download Data",
        data=csv,
        file_name="analyzed_data.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Upload a CSV file to begin")
    
    st.markdown("### 💡 What this tool does:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **📊 Auto Charts**
        - Distributions
        - Comparisons
        - Correlations
        """)
    with col2:
        st.markdown("""
        **🤖 AI Analysis**
        - Key insights
        - Anomaly detection
        - Trends
        """)
    with col3:
        st.markdown("""
        **💼 Business Value**
        - Actionable recommendations
        - Plain English explanations
        - No data science needed
        """)