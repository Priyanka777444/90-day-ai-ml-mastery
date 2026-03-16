import streamlit as st
from pypdf import PdfReader
from vectordb import (
    add_documents, ask_question,
    list_collections, delete_collection,
    get_collection_count
)

st.set_page_config(
    page_title="Persistent Knowledge Base",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Persistent Knowledge Base")
st.markdown("Documents survive restarts — powered by ChromaDB")

# Sidebar
st.sidebar.title("📚 Knowledge Base")

# Show existing collections
existing = list_collections()
if existing:
    st.sidebar.markdown("**Existing collections:**")
    for col in existing:
        count = get_collection_count(col)
        st.sidebar.markdown(f"📁 `{col}` — {count} chunks")

st.sidebar.markdown("---")

# Create or select collection
collection_name = st.sidebar.text_input(
    "Collection name:",
    placeholder="e.g. company_docs"
)

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs to collection:",
    type=['pdf'],
    accept_multiple_files=True
)

add_btn = st.sidebar.button("➕ Add to Knowledge Base", type="primary")

if add_btn and collection_name and uploaded_files:
    with st.spinner("Adding documents to knowledge base..."):
        total_chunks = 0
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            chunks = add_documents(
                collection_name,
                [text],
                uploaded_file.name
            )
            total_chunks += chunks
            st.sidebar.success(f"✅ {uploaded_file.name}: {chunks} chunks")
    
    st.sidebar.success(f"✅ Added {total_chunks} total chunks!")
    st.rerun()

st.sidebar.markdown("---")

# Delete collection
if existing:
    del_collection = st.sidebar.selectbox(
        "Delete a collection:",
        [""] + existing
    )
    if st.sidebar.button("🗑️ Delete", key="delete_btn"):
        if del_collection:
            delete_collection(del_collection)
            st.rerun()

# Main chat area
st.markdown("### 💬 Chat with your Knowledge Base")

if not existing:
    st.info("👈 Create a collection and add PDFs to start")
else:
    selected_collection = st.selectbox(
        "Choose collection to chat with:",
        existing
    )

    if selected_collection:
        count = get_collection_count(selected_collection)
        st.markdown(f"📁 `{selected_collection}` — {count} chunks stored")
        st.markdown("---")

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_collection' not in st.session_state:
            st.session_state.current_collection = None

        # Reset history if collection changes
        if st.session_state.current_collection != selected_collection:
            st.session_state.chat_history = []
            st.session_state.current_collection = selected_collection

        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['question'])
            with st.chat_message("assistant"):
                st.write(chat['answer'])
                with st.expander("📎 Sources"):
                    for i, (source, meta) in enumerate(
                        zip(chat['sources'], chat['metadatas'])
                    ):
                        st.markdown(f"**Source:** `{meta['source']}`")
                        st.text(source[:150])

        # Chat input
        question = st.chat_input("Ask anything from your knowledge base...")

        if question:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Searching knowledge base..."):
                    result = ask_question(
                        selected_collection,
                        question,
                        st.session_state.chat_history
                    )
                st.write(result['answer'])
                with st.expander("📎 Sources"):
                    for i, (source, meta) in enumerate(
                        zip(result['sources'], result['metadatas'])
                    ):
                        st.markdown(f"**Source:** `{meta['source']}`")
                        st.text(source[:150])

            st.session_state.chat_history.append(result)

        if st.session_state.chat_history:
            if st.sidebar.button("🗑️ Clear Chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()