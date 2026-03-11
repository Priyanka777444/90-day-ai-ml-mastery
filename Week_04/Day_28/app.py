import streamlit as st
import tempfile
import os
from pypdf import PdfReader
from rag import build_vectorstore, ask_question

st.set_page_config(
    page_title="PDF Q&A System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Q&A System")
st.markdown("Upload any PDF and ask questions about it")

# Sidebar
st.sidebar.title("📂 Upload PDF")
uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type=['pdf']
)

if uploaded_file:
    # Extract text from PDF
    with st.spinner("Reading PDF..."):
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        total_pages = len(reader.pages)
        total_chars = len(text)
    
    st.sidebar.success(f"✅ PDF loaded: {total_pages} pages")
    st.sidebar.info(f"📊 {total_chars} characters extracted")

    build_btn = st.sidebar.button("🔨 Build Knowledge Base", type="primary")

    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'pdf_name' not in st.session_state:
        st.session_state.pdf_name = None

    if build_btn:
        with st.spinner("Building knowledge base from PDF..."):
            st.session_state.vectorstore = build_vectorstore([text])
            st.session_state.pdf_name = uploaded_file.name
        st.sidebar.success("✅ Knowledge base ready!")

    if st.session_state.vectorstore:
        st.markdown(f"### 💬 Ask questions about: `{st.session_state.pdf_name}`")

        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Question input
        question = st.text_input(
            "Type your question:",
            placeholder="What is this document about?"
        )

        ask_btn = st.button("🔍 Ask", type="primary")

        if ask_btn and question:
            with st.spinner("Searching PDF..."):
                result = ask_question(st.session_state.vectorstore, question)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "question": question,
                "answer": result['answer'],
                "sources": result['sources']
            })

        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 📜 Conversation")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                st.markdown(f"**Q: {chat['question']}**")
                st.success(chat['answer'])
                
                with st.expander("📎 Source chunks"):
                    for j, source in enumerate(chat['sources']):
                        st.text(f"Chunk {j+1}: {source}")
                
                st.markdown("---")

        # Clear history button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear conversation"):
                st.session_state.chat_history = []
                st.rerun()

    else:
        st.info("👈 Upload a PDF and click 'Build Knowledge Base' to start")

else:
    st.info("👈 Upload a PDF file from the sidebar to begin")
    
    # Show example use cases
    st.markdown("### 💡 What can you do with this?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📋 Business Documents**
        - Company policies
        - Employee handbooks
        - Legal contracts
        """)
    with col2:
        st.markdown("""
        **📚 Research Papers**
        - Academic papers
        - Technical reports
        - Market research
        """)
    with col3:
        st.markdown("""
        **🛍️ Product Docs**
        - User manuals
        - Technical specs
        - FAQs
        """)