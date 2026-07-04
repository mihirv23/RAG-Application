from fastapi import APIRouter
from app.db.chroma_client import collection
router = APIRouter()


@router.get("/debug")
def debug():

    data = collection.get(
        include=["metadatas"]
    )

    return {
        "count": len(data["metadatas"]),
        "sample": data["metadatas"][-10:]
    }