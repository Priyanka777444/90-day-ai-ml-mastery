import streamlit as st
from rag import build_vectorstore, ask_question

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Document Q&A System")
st.markdown("Upload a document and ask questions about it")

# Sample document for testing
SAMPLE_DOC = """
ACME Company Refund Policy

1. Refund Eligibility
Customers may request a refund within 30 days of purchase.
Digital products are non-refundable after download.
Physical products must be returned in original condition.

2. Refund Process
Submit refund request to support@acme.com with order number.
Refunds are processed within 5-7 business days.
Refunds are issued to the original payment method only.

3. Shipping Policy
Free shipping on orders above $50.
Standard shipping takes 3-5 business days.
Express shipping takes 1-2 business days and costs $15.

4. Customer Support
Support hours: Monday to Friday, 9AM to 6PM EST.
Email: support@acme.com
Phone: 1-800-ACME-123

5. Privacy Policy
We never sell customer data to third parties.
Data is encrypted using industry standard AES-256.
Customers can request data deletion at any time.
"""

# Sidebar
st.sidebar.title("📄 Document Input")
input_method = st.sidebar.radio(
    "Choose input:",
    ["Use Sample Document", "Paste Your Text"]
)

if input_method == "Use Sample Document":
    document_text = SAMPLE_DOC
    st.sidebar.success("✅ Sample document loaded")
else:
    document_text = st.sidebar.text_area(
        "Paste your document:",
        height=300,
        placeholder="Paste any text document here..."
    )

build_btn = st.sidebar.button("🔨 Build Knowledge Base", type="primary")

# Session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None

if build_btn and document_text:
    with st.spinner("Building knowledge base..."):
        st.session_state.vectorstore = build_vectorstore([document_text])
    st.sidebar.success("✅ Knowledge base ready!")

# Main area
if st.session_state.vectorstore:
    st.markdown("### 💬 Ask Questions")
    
    # Example questions
    st.markdown("**Try these:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("What is the refund policy?"):
            st.session_state.question = "What is the refund policy?"
    with col2:
        if st.button("How long does shipping take?"):
            st.session_state.question = "How long does shipping take?"
    with col3:
        if st.button("Is customer data sold?"):
            st.session_state.question = "Is customer data sold?"

    question = st.text_input(
        "Or type your question:",
        value=st.session_state.get('question', '')
    )

    if question:
        with st.spinner("Searching knowledge base..."):
            result = ask_question(st.session_state.vectorstore, question)
        
        st.markdown("### 🎯 Answer")
        st.success(result['answer'])
        
        with st.expander("📎 Source chunks used"):
            for i, source in enumerate(result['sources']):
                st.markdown(f"**Chunk {i+1}:**")
                st.text(source)
else:
    st.info("👈 Load a document and click 'Build Knowledge Base' to start")