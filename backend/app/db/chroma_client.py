import chromadb
from pathlib import Path
import uuid

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "chroma_db"
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="documents"
)

def add_chunks(
    chunks,
    embeddings,
    metadata
):
    ids = [
    str(uuid.uuid4())
    for _ in chunks
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )
def search(
    query_embedding,
    document_id=None,
    n_results=5
):
    if document_id:
        return collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=n_results,
            where={
                "document_id": document_id
            }
        )
    else :
        return collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=n_results
        )