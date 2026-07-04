from fastapi import APIRouter
from fastapi import HTTPException
from app.db.mysql import SessionLocal
from app.models.user import User

from app.schemas.user import UserCreate

from app.auth.password import (
    hash_password
)
from app.schemas.user import UserLogin

from app.auth.password import (
    verify_password
)

from app.auth.jwt_handler import (
    create_access_token
)
from fastapi import Depends

from app.auth.dependencies import (
    get_current_user
)

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    existing_user = (
        db.query(User)
          .filter(
              User.username == user.username
          )
          .first()
    )

    if existing_user:

        db.close()

        raise HTTPException(
        status_code=401,
        detail="User already exists"
    )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    db.close()

    return {
        "message":
        "User registered successfully",
        "user_id":
        new_user.user_id
    }


@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    db_user = (
        db.query(User)
        .filter(
            User.username == user.username
        )
        .first()
    )

    if not db_user:

        db.close()

        raise HTTPException(
        status_code=401,
        detail="Invalid username"
    )
    if not verify_password(
        user.password,
        db_user.password_hash
    ):

        db.close()

        raise HTTPException(
        status_code=401,
        detail="Invalid password"
    )
    token = create_access_token(
        {
            "user_id":
            db_user.user_id
        }
    )

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }    

@router.get("/me")
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "user_id":
        current_user.user_id,

        "username":
        current_user.username,

        "email":
        current_user.email
    }