from pathlib import Path
from dotenv import load_dotenv
import os
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# --------------------------
# Load environment variables
# --------------------------
BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --------------------------
# FastAPI app
# --------------------------
app = FastAPI(title="Legal QA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# Load FAISS vectorstore
# --------------------------
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

INDEX_PATH = BASE / "legal_faiss_index"
vectorstore = FAISS.load_local(
    str(INDEX_PATH),
    embeddings_model,
    allow_dangerous_deserialization=True,
)

# --------------------------
# Setup QA retrieval (context)
# --------------------------
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# --------------------------
# API request model
# --------------------------
class QuestionRequest(BaseModel):
    question: str

# --------------------------
# Gemini 2.5 Flash API
# --------------------------
def ask_gemini(question: str, context: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    )

    headers = {"Content-Type": "application/json"}

    system_instructions = """
You are a Legal Assistant specializing in Indian Law.

Always follow these formatting rules:
1. Answer ONLY in Markdown.
2. Start with a 1–2 line summary.
3. Use **bold headings** for sections (e.g., **Legal Basis**, **Steps to Follow**).
4. Use numbered lists for step-by-step procedures.
5. Use bullet points for rights, conditions, or important notes.
6. Keep paragraphs short (2–3 sentences).
7. Clearly state that you are NOT a substitute for a licensed advocate.
"""

    user_prompt = f"""
Context (legal provisions and sections):
{context}

User question:
{question}

Now generate a well-structured Markdown answer following the rules above.
"""

    data = {
        "contents": [
            {"parts": [{"text": system_instructions}]},
            {"parts": [{"text": user_prompt}]},
        ]
    }

    params = {"key": GEMINI_API_KEY}
    response = requests.post(url, headers=headers, params=params, json=data)

    if response.status_code == 200:
        try:
            return (
                response.json()["candidates"][0]["content"]["parts"][0]["text"]
                .strip()
            )
        except (KeyError, IndexError):
            return "Sorry, I could not generate a response due to an unexpected API format."
    else:
        return f"Error: {response.status_code} {response.text}"

# --------------------------
# API endpoints
# --------------------------
@app.post("/ask")
def ask_question(req: QuestionRequest):
    # Retrieve relevant context chunks from FAISS
    docs = retriever.get_relevant_documents(req.question)

    # Trim each chunk a bit so the LLM is forced to summarise instead of pasting walls of text
    context_parts = []
    for doc in docs:
        text = doc.page_content.strip()
        context_parts.append(text[:800])  # first 800 chars of each chunk

    context = "\n\n---\n\n".join(context_parts)

    answer = ask_gemini(req.question, context)
    return {"question": req.question, "answer": answer}

@app.get("/")
def root():
    return {"message": "Legal QA API is running."}
