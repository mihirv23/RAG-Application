from fastapi import APIRouter
from typing import Optional
from app.rag.embeddings import generate_embedding
from app.db.chroma_client import search
from app.rag.prompt_builder import build_prompt
from app.services.llm_service import generate_response

router = APIRouter()

@router.post("/query")
async def query_document(   
    question: str,
    document_id: Optional[str] = None
):
    #this check can be done using pydantic models too
    query_embedding = generate_embedding(
        question
    )

    results = search(query_embedding,document_id)

    chunks = results["documents"][0]

    prompt = build_prompt(
        question,
        chunks
    )

    answer = generate_response(
        prompt
    )

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": chunks
    }