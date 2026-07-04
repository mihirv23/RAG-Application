from pydantic import BaseModel

class UserCreate(BaseModel):

    username: str
    email: str
    password: str

# why did we do this 
#Because FastAPI likes receiving JSON through Pydantic models.

class UserLogin(BaseModel):

    username: str
    password: str