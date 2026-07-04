from app.db.mysql import SessionLocal
from app.models.user import User

db = SessionLocal()

new_user = User(
    username="mihir",
    email="mihir@test.com",
    password_hash="dummy"
)

db.add(new_user)

db.commit()

db.refresh(new_user)

print(new_user.user_id)
#---------------------------------------

user = (
    db.query(User)
      .filter(User.username == "mihir")
      .first()
)

print(user.username)
#------------------------------------------
#retrieval also works fine



db.close()