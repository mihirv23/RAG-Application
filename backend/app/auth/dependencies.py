from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import (
    OAuth2PasswordBearer
)

from app.auth.jwt_handler import (
    verify_token
)

from app.db.mysql import SessionLocal

from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):
    payload = verify_token(
        token
    )

    user_id = payload.get(
        "user_id"
    )

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )

    db.close()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    return user