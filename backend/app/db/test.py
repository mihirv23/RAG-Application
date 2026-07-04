from app.rag.embeddings import generate_embedding
from app.db.chroma_client import search

query = generate_embedding(
    "What is cpu virtualization?"
)

results = search(query)

for i, doc in enumerate(results["documents"][0]):
    print(f"\n--- Chunk {i+1} ---\n")
    print(doc[:500])