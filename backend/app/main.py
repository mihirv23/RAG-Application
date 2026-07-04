from fastapi import FastAPI
from app.routes import upload
from app.routes import debug
from app.routes.query import router as query_router
from app.routes import auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(upload.router)
app.include_router(query_router)
app.include_router(debug.router)
app.include_router(auth.router)
#check diff in above 2 syntax

origins = ["http://localhost:5173"]
app.add_middleware(CORSMiddleware,allow_origins = origins,allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.get("/")
def home():
    return {"message": "RAG Backend Running"}