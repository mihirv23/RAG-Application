# from fastapi import APIRouter, UploadFile, File

# router = APIRouter()

# @router.post("/upload")
# async def upload_pdf(file: UploadFile = File(...)):
#     return {
#         "filename": file.filename,
#         "content_type": file.content_type
#     }

from fastapi import APIRouter, UploadFile, File
from app.services.pdf_parser import extract_text
from app.rag.chunking import chunk_text
from app.services.text_cleaner import clean_text
from app.rag.embeddings import generate_embeddings
from app.db.chroma_client import add_chunks
import uuid
from fastapi import Depends
from app.models.document import Document
from app.db.mysql import SessionLocal
from app.models.user import User

from app.auth.dependencies import (
    get_current_user
)

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)
    ,current_user: User = Depends(
        get_current_user
    )): 

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text, pages = extract_text(file_path)
    text = clean_text(text)
    chunks = chunk_text(text)
    document_id = str(uuid.uuid4())
    embeddings = generate_embeddings(chunks)

    new_document = Document(
    document_id=document_id,
    filename=file.filename,
    user_id=current_user.user_id
    # user_id = 2
    #this has been hardcoded for now later with react it will be restored
)

    db = SessionLocal()
    db.add(new_document)

    db.commit()

    db.refresh(new_document)
    db.close()
    
    metadata = [
    {
        "filename": file.filename,
        "user_id": current_user.user_id,
        # "user_id":2,
        "document_id": document_id
    }
    for _ in chunks
]
    add_chunks(
    chunks,
    embeddings,
    metadata
)
    print(metadata[0])

    return {
    "filename": file.filename,
    "document_id": document_id,
    "chunks": len(chunks),
    "stored": True
}

@router.get("/documents")
def get_documents(
    current_user: User = Depends(
        get_current_user
    )
):
    db = SessionLocal()
    documents = (
    db.query(Document)
      .filter(
          Document.user_id
          == current_user.user_id
        # Document.user_id
        #   == 1
      )
      .all()

)
    return [
    {
        "document_id":
        doc.document_id,

        "filename":
        doc.filename
    }
    for doc in documents
]

