import streamlit as st
from pypdf import PdfReader
from rag import build_vectorstore, ask_with_memory

st.set_page_config(
    page_title="Multi-PDF Chat",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-PDF Chat System")
st.markdown("Upload multiple PDFs and chat across all of them")

# Sidebar
st.sidebar.title("📂 Upload PDFs")
uploaded_files = st.sidebar.file_uploader(
    "Choose PDF files",
    type=['pdf'],
    accept_multiple_files=True
)

if uploaded_files:
    st.sidebar.success(f"✅ {len(uploaded_files)} PDF(s) loaded")
    
    for f in uploaded_files:
        reader = PdfReader(f)
        st.sidebar.markdown(f"📄 {f.name} — {len(reader.pages)} pages")

    build_btn = st.sidebar.button("🔨 Build Knowledge Base", type="primary")

    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'doc_names' not in st.session_state:
        st.session_state.doc_names = []

    if build_btn:
        with st.spinner("Reading all PDFs and building knowledge base..."):
            all_texts = []
            doc_names = []
            
            for uploaded_file in uploaded_files:
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                all_texts.append(text)
                doc_names.append(uploaded_file.name)
            
            st.session_state.vectorstore = build_vectorstore(all_texts)
            st.session_state.doc_names = doc_names
            st.session_state.chat_history = []

        st.sidebar.success("✅ Knowledge base ready!")

    # Main chat area
    if st.session_state.vectorstore:
        st.markdown(f"### 💬 Chatting across {len(st.session_state.doc_names)} document(s):")
        for name in st.session_state.doc_names:
            st.markdown(f"- 📄 `{name}`")

        st.markdown("---")

        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['question'])
            with st.chat_message("assistant"):
                st.write(chat['answer'])
                with st.expander("📎 Sources"):
                    for i, source in enumerate(chat['sources']):
                        st.text(f"Chunk {i+1}: {source}")

        # Chat input
        question = st.chat_input("Ask anything about your documents...")

        if question:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Searching documents..."):
                    result = ask_with_memory(
                        st.session_state.vectorstore,
                        question,
                        st.session_state.chat_history
                    )
                st.write(result['answer'])
                with st.expander("📎 Sources"):
                    for i, source in enumerate(result['sources']):
                        st.text(f"Chunk {i+1}: {source}")

            st.session_state.chat_history.append(result)

        # Clear button
        if st.session_state.chat_history:
            if st.sidebar.button("🗑️ Clear Chat", key="clear"):
                st.session_state.chat_history = []
                st.rerun()

    else:
        st.info("👈 Upload PDFs and click 'Build Knowledge Base'")

else:
    st.info("👈 Upload one or more PDF files to begin")
    
    st.markdown("### 💡 Use cases:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **For businesses:**
        - Chat with all company policies at once
        - Search across multiple contracts
        - Q&A across product manuals
        """)
    with col2:
        st.markdown("""
        **For students:**
        - Chat with multiple research papers
        - Ask questions across textbook chapters
        - Summarize multiple documents
        """)