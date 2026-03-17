import streamlit as st
import pandas as pd
from agent import process_ticket

st.set_page_config(
    page_title="Multi-Agent Support System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent Customer Support System")
st.markdown("3 AI agents working together — Classifier → Reply Drafter → Escalation Manager")

# Show agent pipeline
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Agent 1 — Classifier**\nAnalyzes ticket category, priority, emotion")
with col2:
    st.info("**Agent 2 — Reply Drafter**\nWrites empathetic customer reply")
with col3:
    st.info("**Agent 3 — Escalation Manager**\nDecides routing and SLA")

st.markdown("---")

# Input
st.markdown("### 🎫 Submit a Ticket")
input_method = st.radio(
    "Input method:",
    ["Type a ticket", "Use sample tickets"],
    horizontal=True
)

if input_method == "Use sample tickets":
    ticket_input = st.selectbox(
        "Choose a sample ticket:",
        [
            "My payment failed but money was deducted from my account",
            "I've been waiting 3 weeks for my order. This is unacceptable!",
            "App keeps crashing every time I try to checkout",
            "I was charged twice for the same order. I want a refund NOW",
            "How do I upgrade my subscription plan?"
        ]
    )
else:
    ticket_input = st.text_area(
        "Enter ticket:",
        height=100,
        placeholder="Describe the customer issue..."
    )

process_btn = st.button("🚀 Process with AI Agents", type="primary")

if process_btn and ticket_input:
    st.markdown("---")
    st.markdown("### 🔄 Agent Pipeline Running...")

    # Show live progress
    with st.status("Processing ticket through 3 agents...", expanded=True) as status:
        st.write("🤖 Agent 1: Classifying ticket...")
        
        result = process_ticket(ticket_input)
        
        st.write("✅ Agent 1: Classification complete")
        st.write("✍️ Agent 2: Drafting customer reply...")
        st.write("✅ Agent 2: Reply drafted")
        st.write("📊 Agent 3: Making escalation decision...")
        st.write("✅ Agent 3: Escalation decision made")
        status.update(label="✅ All agents complete!", state="complete")

    st.markdown("---")
    st.markdown("## 📊 Results")

    # Agent 1 Results
    st.markdown("### 🤖 Agent 1 — Classification")
    col1, col2, col3, col4 = st.columns(4)
    clf = result['classification']
    
    with col1:
        st.metric("Category", clf.get('category', 'N/A'))
    with col2:
        priority = clf.get('priority', 'N/A')
        st.metric("Priority", priority)
    with col3:
        st.metric("Emotion", clf.get('emotion', 'N/A'))
    with col4:
        escalate = result['escalation'].get('escalate', 'N/A')
        st.metric("Escalate?", escalate)

    st.info(f"**Summary:** {clf.get('summary', 'N/A')}")

    # Agent 2 Results
    st.markdown("### ✍️ Agent 2 — Customer Reply")
    st.success(result['reply'])

    # Copy button hint
    st.caption("👆 Copy this reply and send directly to customer")

    # Agent 3 Results
    st.markdown("### 📊 Agent 3 — Escalation Decision")
    esc = result['escalation']
    
    col1, col2 = st.columns(2)
    with col1:
        if esc.get('escalate') == 'YES':
            st.error(f"⚠️ ESCALATE to: **{esc.get('assign_to', 'N/A')}**")
        else:
            st.success("✅ No escalation needed — handle at frontline")
        
        st.metric("SLA", f"{esc.get('sla_hours', 'N/A')} hours")
    with col2:
        st.info(f"**Reason:** {esc.get('reason', 'N/A')}")

    # Full summary
    st.markdown("---")
    st.markdown("### 📋 Complete Ticket Summary")
    summary_data = {
        "Field": ["Ticket", "Category", "Priority", 
                  "Emotion", "Escalate", "Assign To", "SLA"],
        "Value": [
            ticket_input[:50] + "...",
            clf.get('category', 'N/A'),
            clf.get('priority', 'N/A'),
            clf.get('emotion', 'N/A'),
            esc.get('escalate', 'N/A'),
            esc.get('assign_to', 'N/A'),
            f"{esc.get('sla_hours', 'N/A')} hours"
        ]
    }
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

elif process_btn:
    st.warning("Please enter a ticket first!")
else:
    st.info("👆 Enter a ticket and click Process to see all 3 agents work together")