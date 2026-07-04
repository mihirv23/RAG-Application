from app.db.mysql import engine
from app.models.user import User
from app.models.document import Document
from app.db.mysql import Base

Base.metadata.create_all(bind=engine)