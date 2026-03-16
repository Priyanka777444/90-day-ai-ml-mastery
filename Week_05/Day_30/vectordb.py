import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

#oersistent chromadn client
client = chromadb.PersistentClient(path="./chroma_db")

#embedding function
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def get_or_create_collection(collection_name: str):
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )

def add_documents(collection_name: str, texts: list, doc_name: str):
    collection = get_or_create_collection(collection_name)

    #split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap=50
    )
    chunks = splitter.create_documents(texts)
    chunks = [c for c in chunks if c.page_content.strip()]

    #add to chromadb
    collection.add(
        documents=[c.page_content for c in chunks],
        ids=[f"{doc_name}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": doc_name, "chunk": i} for i in range(len(chunks))]
    )

    return len(chunks)

def query_collection(collection_name: str, question: str, n_results: int = 3):
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    return {
        "documents": results['documents'][0],
        "metadatas": results['metadatas'][0]
    }

def ask_question(collection_name: str, question: str, chat_history: list = []) -> dict:
    #get relevant chunks
    results = query_collection(collection_name, question)
    context ="\n\n".join(results['documents'])

    #build history
    history_text = ""
    for turn in chat_history[-3:]:
        history_text +=f"Human: {turn['question']}\n Assistant: {turn['answer']}\n\n"

    prompt = f""" you are helpful assistant answering questions from documents.

Previous conversation:
{history_text}

Document context:
{context}

Question: {question}

Answer based only on the document context:"""
    
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content.strip(),
        "sources": results['documents'],
        "metadatas": results['metadatas']
    }

def list_collections():
    return [c.name for c in client.list_collections()]

def delete_collection(collection_name: str):
    client.delete_collection(collection_name)

def get_collection_count(collection_name: str):
    collection = get_or_create_collection(collection_name)
    return collection.count()