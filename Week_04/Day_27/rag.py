import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.language_models.llms import LLM
from groq import Groq
from dotenv import load_dotenv
from typing import Optional, List, Any

load_dotenv()

class GroqLLM(LLM):
    model: str = "llama-3.3-70b-versatile"

    @property
    def _llm_type(self) -> str:
        return "groq"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

def build_vectorstore(texts: list) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.create_documents(texts)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def ask_question(vectorstore: FAISS, question: str) -> dict:
    # Retrieve relevant chunks
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Build prompt manually
    prompt = f"""Use the following context to answer the question.
If the answer is not in the context, say "I don't know based on the provided document."

Context:
{context}

Question: {question}

Answer:"""

    llm = GroqLLM()
    answer = llm._call(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources": [doc.page_content[:100] for doc in docs]
    }