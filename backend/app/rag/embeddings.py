from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

EMBEDDING_DIM = 384

def generate_embedding(text: str):
    return model.encode(text)

def generate_embeddings(chunks):
    return model.encode(chunks)